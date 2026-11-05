#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 1 del pipeline: scraping de anuncios recientes de Revolico (La Habana).

Se descargan las subcategorias de motos de combustion y de motos electricas,
se recorren las paginas y se guardan las fichas de los anuncios mas recientes.
Solo se aceptan las cuatro categorias oficiales: motos de combustion, motos
electricas, bicicletas electricas y patinetes.

Salidas:
  - data/raw/revolico/revolico_raw_<sello>.json
  - data/raw/revolico/revolico_raw_<sello>.csv

El dato crudo conserva los campos originales de Revolico (se eliminan los
datos de contacto: telefono y correo) y agrega un bloque "_scraping" con
"incluido" y la categoria detectada (solo si entra).

Uso:
    python scrape.py
    python scrape.py --n 30 --max-paginas 3 --delay 1.0
    python scrape.py --proyecto "C:/ruta/Mercado-de-Motos" --salida data/raw/revolico
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from common import (  # noqa: E402
    BASE_URL,
    CATEGORIA,
    PROVINCIA,
    SUBCATEGORIAS,
    Logger,
    ahora_habana,
    clasificar_vehiculo,
    guardar_csv,
    guardar_json,
    paths,
    sello,
    url_valida,
)
from contactos import sanear_contactos  # noqa: E402

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "es-CU,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Campos de contacto que NUNCA se guardan (privacidad)
CAMPOS_PII = ("phoneInfo", "contactInfo", "email({\"mask\":true})", "email")


# ---------------------------------------------------------------------------
# Extraccion con tolerancia a fallos
# ---------------------------------------------------------------------------
def _json_de_script(html, patron):
    m = re.search(patron, html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def extraer_next_data(html):
    """
    Devuelve el JSON de __NEXT_DATA__ o None.

    Estrategia 1: <script id="__NEXT_DATA__" type="application/json">
    Estrategia 2: cualquier <script type="application/json"> con "props"
    Estrategia 3: chunks de Next.js con el estado Apollo embebido
    """
    data = _json_de_script(
        html, r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    )
    if data:
        return data
    for m in re.finditer(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.S):
        try:
            cand = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(cand, dict) and "props" in cand:
            return cand
    for m in re.finditer(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S):
        try:
            chunk = json.loads('"' + m.group(1) + '"')
        except json.JSONDecodeError:
            continue
        if "__APOLLO_STATE__" not in chunk:
            continue
        idx = chunk.find('"__APOLLO_STATE__":')
        inicio = chunk.find("{", idx) if idx >= 0 else -1
        if inicio < 0:
            continue
        depth, i = 0, inicio
        while i < len(chunk):
            if chunk[i] == "{":
                depth += 1
            elif chunk[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        try:
            apollo = json.loads(chunk[inicio:i + 1])
        except json.JSONDecodeError:
            continue
        return {"props": {"pageProps": {"__APOLLO_STATE__": apollo}}}
    return None


def apollo_state(html):
    data = extraer_next_data(html)
    if not data:
        return {}
    return data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})


def anuncios_de_estado(apollo):
    return [
        (k, v)
        for k, v in apollo.items()
        if k.startswith("AdType:") and isinstance(v, dict)
    ]


def buscar_pagina(session, subcategoria, pagina, con_imagenes=True):
    params = {
        "category": CATEGORIA,
        "subcategory": subcategoria,
        "province": PROVINCIA,
        "page": pagina,
    }
    if con_imagenes:
        params["images"] = "on"
    resp = session.get(f"{BASE_URL}/search", params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    apollo = apollo_state(resp.text)
    if not apollo:
        raise RuntimeError("No se encontro el estado de Apollo (__NEXT_DATA__)")
    return anuncios_de_estado(apollo)


def detalle_anuncio(session, ad_id, permalink):
    """Descarga la ficha y devuelve (AdType completo, estado Apollo)."""
    if not permalink:
        return None
    url = BASE_URL + permalink if permalink.startswith("/") else permalink
    resp = session.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    apollo = apollo_state(resp.text)
    if not apollo:
        return None
    directo = apollo.get(f"AdType:{ad_id}")
    if isinstance(directo, dict):
        return directo, apollo
    for k, v in apollo.items():
        if k.startswith("AdType:") and isinstance(v, dict):
            return v, apollo
    return None


def nombre_lugar(apollo, ref):
    """Resuelve ProvinceType/MunicipalityType a su nombre."""
    if not ref:
        return ""
    if isinstance(ref, str) and ":" in ref:
        obj = apollo.get(ref)
        if isinstance(obj, dict):
            return obj.get("name", "") or obj.get("slug", "")
        return ""
    if isinstance(ref, dict):
        return ref.get("name", "") or ref.get("slug", "")
    return ""


def limpiar_pii(ad):
    """Copia del anuncio sin datos de contacto (campos PII y textos)."""
    limpio = {}
    for k, v in ad.items():
        if k in CAMPOS_PII or k.startswith("email"):
            continue
        limpio[k] = sanear_contactos(v) if isinstance(v, str) else v
    return limpio


# ---------------------------------------------------------------------------
# Descarga y filtrado
# ---------------------------------------------------------------------------
def collecting_candidatos(session, log, max_paginas, delay, con_imagenes=True):
    """Recorre las subcategorias y devuelve los candidatos mas recientes."""
    candidatos, vistos = [], set()
    for nombre, subcategoria in SUBCATEGORIAS.items():
        log(f"  Buscando subcategoria '{nombre}' ({subcategoria})")
        for pagina in range(1, max_paginas + 1):
            try:
                anuncios = buscar_pagina(session, subcategoria, pagina, con_imagenes)
            except Exception as exc:
                log(f"  [error] pagina {pagina} de {nombre}: {exc}")
                break
            nuevos = 0
            for _key, ad in anuncios:
                ad_id = str(ad.get("id", ""))
                if not ad_id or ad_id in vistos:
                    continue
                vistos.add(ad_id)
                ad = dict(ad)
                ad["_subcategoria"] = nombre
                candidatos.append(ad)
                nuevos += 1
            log(f"  pagina {pagina}: {len(anuncios)} anuncios, {nuevos} nuevos")
            if not anuncios or nuevos == 0:
                break
            time.sleep(delay)
    candidatos.sort(key=lambda a: a.get("updatedOnToOrder") or "", reverse=True)
    return candidatos


def construir_registro(ad, subcategoria, ficha=None, apollo=None, categoria=""):
    """Arma el registro crudo: campos originales (sin PII) + metadatos."""
    ficha = ficha or ad
    apollo = apollo or {}
    descripcion = (
        ficha.get("description") or ficha.get("shortDescription") or ""
    ).strip()
    provincia = nombre_lugar(apollo, ficha.get("province"))
    municipio = nombre_lugar(apollo, ficha.get("municipality"))
    permalink = ficha.get("permalink") or ad.get("permalink") or ""
    url = BASE_URL + permalink if permalink.startswith("/") else permalink

    registro = limpiar_pii(ficha)
    registro["_subcategoria"] = subcategoria
    registro["_scraping"] = {
        "id": str(ficha.get("id") or ad.get("id") or ""),
        "url": url,
        "titulo_original": ficha.get("title") or ad.get("title", "") or "",
        "precio_original": ficha.get("price", ad.get("price")),
        "moneda_original": ficha.get("currency", ad.get("currency", "")) or "",
        "descripcion": descripcion,
        "provincia": provincia,
        "municipio": municipio,
        "ubicacion": " - ".join(x for x in (provincia, municipio) if x),
        "fecha_publicacion": (
            ficha.get("updatedOnToOrder") or ad.get("updatedOnToOrder", "") or ""
        ),
        "categoria": categoria,
        "incluido": bool(categoria),
    }
    return registro


def scrape(session, n_objetivo, max_paginas, delay, log,
           con_imagenes=True, max_candidatos=150):
    """
    Descarga candidatos y acepta solo las cuatro categorias oficiales hasta
    reunir `n_objetivo` anuncios. Devuelve (incluidos, descartados, errores).
    """
    log("1) Recolectando candidatos de las subcategorias...")
    candidatos = collecting_candidatos(session, log, max_paginas, delay, con_imagenes)
    log(f"  Candidatos unicos: {len(candidatos)}")

    incluidos, descartados, errores = [], [], []
    vistos = set()

    log(f"2) Leyendo fichas hasta reunir {n_objetivo} anuncios validos...")
    for ad in candidatos:
        if len(incluidos) >= n_objetivo:
            break
        if len(incluidos) + len(descartados) >= max_candidatos:
            log(f"  Limite de {max_candidatos} candidatos revisados alcanzado.")
            break

        ad_id = str(ad.get("id", ""))
        titulo = ad.get("title", "") or ""
        subcategoria = ad.get("_subcategoria", "combustion")

        # Clasificacion rapida con el titulo (evita descargar fichas inutiles)
        categoria, _motivo = clasificar_vehiculo(titulo, "", subcategoria)
        if not categoria:
            descartados.append(construir_registro(ad, subcategoria))
            continue

        # Ficha completa: descripcion, provincia y municipio
        ficha, apollo = None, {}
        try:
            detalle = detalle_anuncio(session, ad_id, ad.get("permalink", ""))
            if detalle:
                ficha, apollo = detalle
        except Exception as exc:
            errores.append({"id": ad_id, "url": ad.get("permalink", ""), "error": str(exc)})
            log(f"  [error] detalle de {ad_id}: {exc}")
            descartados.append(construir_registro(ad, subcategoria))
            continue
        if not ficha:
            errores.append({"id": ad_id, "url": ad.get("permalink", ""), "error": "sin ficha"})
            descartados.append(construir_registro(ad, subcategoria))
            continue

        descripcion = (ficha.get("description") or ficha.get("shortDescription") or "").strip()
        categoria, _motivo = clasificar_vehiculo(titulo, descripcion, subcategoria)
        registro = construir_registro(ad, subcategoria, ficha, apollo, categoria or "")
        if not categoria:
            descartados.append(registro)
            continue

        url = registro["_scraping"]["url"]
        if not url_valida(url) or ad_id in vistos:
            registro["_scraping"]["incluido"] = False
            registro["_scraping"]["categoria"] = ""
            descartados.append(registro)
            continue

        vistos.add(ad_id)
        incluidos.append(registro)
        log(f"  [ok:{categoria}] {titulo[:62]}")
        time.sleep(delay)

    return incluidos, descartados, errores


# ---------------------------------------------------------------------------
# Guardado del dato crudo
# ---------------------------------------------------------------------------
def guardar_raw(ruta_dir, incluidos, descartados, errores, meta):
    ruta_dir.mkdir(parents=True, exist_ok=True)
    est = meta["sello"]
    todos = list(incluidos)
    todos.sort(key=lambda a: a.get("_scraping", {}).get("fecha_publicacion") or "", reverse=True)

    payload = {
        "fuente": "Revolico",
        "provincia": "La Habana",
        "generado_habana": ahora_habana().isoformat(),
        "params": meta.get("params", {}),
        "total": len(todos),
        "errores": errores,
        "anuncios": todos,
    }
    ruta_json = guardar_json(ruta_dir / f"revolico_raw_{est}.json", payload)

    columnas = [
        "id", "titulo", "precio", "moneda", "fecha_publicacion", "ubicacion",
        "provincia", "municipio", "descripcion", "url", "subcategoria",
        "categoria", "incluido", "imagenes", "vistas", "promocionado",
    ]
    filas = []
    for a in todos:
        sc = a.get("_scraping", {})
        filas.append({
            "id": sc.get("id", ""),
            "titulo": sc.get("titulo_original", ""),
            "precio": sc.get("precio_original", ""),
            "moneda": sc.get("moneda_original", ""),
            "fecha_publicacion": sc.get("fecha_publicacion", ""),
            "ubicacion": sc.get("ubicacion", ""),
            "provincia": sc.get("provincia", ""),
            "municipio": sc.get("municipio", ""),
            "descripcion": sc.get("descripcion", ""),
            "url": sc.get("url", ""),
            "subcategoria": a.get("_subcategoria", ""),
            "categoria": sc.get("categoria", ""),
            "incluido": sc.get("incluido", False),
            "imagenes": a.get("imagesCount", 0),
            "vistas": a.get("viewCount", 0),
            "promocionado": a.get("isPromoted", False),
        })
    ruta_csv = guardar_csv(ruta_dir / f"revolico_raw_{est}.csv", filas, columnas)
    return ruta_json, ruta_csv


def main():
    ap = argparse.ArgumentParser(description="Scraping de anuncios de Revolico (La Habana)")
    ap.add_argument("--n", type=int, default=30, help="Anuncios validos a obtener (30 por defecto)")
    ap.add_argument("--extra", type=int, default=10, help="Anuncios extra para cubrir descartes de limpieza")
    ap.add_argument("--max-paginas", type=int, default=3, help="Paginas por subcategoria")
    ap.add_argument("--max-candidatos", type=int, default=150, help="Maximo de anuncios revisados")
    ap.add_argument("--delay", type=float, default=1.0, help="Pausa entre peticiones (s)")
    ap.add_argument("--proyecto", default=None, help="Ruta raiz del proyecto")
    ap.add_argument("--salida", default=None, help="Carpeta de salida (por defecto data/raw/revolico)")
    ap.add_argument("--sin-imagenes", action="store_true", help="Incluir anuncios sin foto")
    args = ap.parse_args()

    p = paths(Path(args.proyecto) if args.proyecto else None)
    est = sello()
    log = Logger(p["logs"] / f"revolico_{est}.log")
    log(f"=== Scraping de Revolico - {ahora_habana().isoformat()} ===")
    log(f"Proyecto: {p['root']}")

    salida = Path(args.salida) if args.salida else p["raw"]
    session = requests.Session()
    incluidos, descartados, errores = scrape(
        session, args.n + args.extra, args.max_paginas, args.delay, log,
        con_imagenes=not args.sin_imagenes,
        max_candidatos=args.max_candidatos,
    )

    log.contar("anuncios_consultados", len(incluidos) + len(descartados))
    log.contar("anuncios_validos", len(incluidos))
    log.contar("anuncios_descartados", len(descartados))
    log.contar("errores", len(errores))
    for cat in (
        "motos_combustion",
        "motos_electricas",
        "bicicletas_electricas",
        "patinetes",
    ):
        log.contar(f"validos_{cat}", sum(
            1 for a in incluidos if a.get("_scraping", {}).get("categoria") == cat
        ))
    for e in errores:
        log.log(f"  ERROR: {e.get('id')} {e.get('error')}")

    meta = {
        "sello": est,
        "params": {
            "n": args.n,
            "max_paginas": args.max_paginas,
            "max_candidatos": args.max_candidatos,
            "delay": args.delay,
            "solo_con_imagen": not args.sin_imagenes,
        },
    }
    ruta_json, ruta_csv = guardar_raw(salida, incluidos, descartados, errores, meta)
    log.log("")
    log.log(f"Dato crudo guardado en:\n  - {ruta_json}\n  - {ruta_csv}")
    log.cerrar()
    print(f"\nOK  validos={len(incluidos)}  descartados={len(descartados)}  errores={len(errores)}")
    print(f"    {ruta_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
