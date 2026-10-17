#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper de anuncios de Revolico (Cuba) - Mercado de Motos en Cuba
=================================================================

Extrae los anuncios mas recientes de Revolico para la provincia La Habana.

Por defecto extrae DOS categorias (juntas):
    - Motos de Combustion          (vehiculos-motos-de-combustion)
    - Motos Electricas             (vehiculos-motos-electricas-y-triciclos)

De la categoria de motos electricas se EXCLUYEN los triciclos.

Opcionalmente se puede anadir la categoria de bicicletas:
    - Bicicletas                   (vehiculos-bicicletas)

Filtra por fecha de publicacion/actualizacion desde los ultimos dias
(por defecto 7) hasta hoy, en hora de La Habana.

Los datos crudos se guardan en `datos/revolico/` en formato CSV y JSON.

Uso:
    python scraper_revolico.py                     # motos de combustion + electricas (sin triciclos)
    python scraper_revolico.py --dias 14           # ultimos 14 dias
    python scraper_revolico.py --categorias motos  # solo motos de combustion
    python scraper_revolico.py --categorias motos,electricas,bicicletas
    python scraper_revolico.py --sin-imagenes      # incluir anuncios sin foto
    python scraper_revolico.py --max-paginas 5     # limitar paginas por categoria
"""

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# ---------------------------------------------------------------------------
# Configuracion general
# ---------------------------------------------------------------------------
BASE_URL = "https://www.revolico.com"
TZ_HABANA = ZoneInfo("America/Havana")
PROVINCIA = "la-habana"
CATEGORY = "vehiculos"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "es-CU,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Categorias disponibles
CATEGORIAS = {
    "motos": {
        "clave": "motos_combustion",
        "nombre": "Motos de Combustion",
        "subcategory": "vehiculos-motos-de-combustion",
    },
    "electricas": {
        "clave": "motos_electricas",
        "nombre": "Motos Electricas",
        "subcategory": "vehiculos-motos-electricas-y-triciclos",
    },
    "bicicletas": {
        "clave": "bicicletas",
        "nombre": "Bicicletas",
        "subcategory": "vehiculos-bicicletas",
    },
}
CATEGORIAS_POR_DEFECTO = ["motos", "electricas"]

# Palabras clave para detectar motos/bicicletas electricas
CLAVES_ELECTRICAS = (
    "electric", "electrica", "electrico", "eléctrica", "eléctrico", "eléctric",
    "litio", "lithium", "bateria", "batería", "ebike", "e-bike", "ev ",
)

# Palabras clave para EXCLUIR triciclos
CLAVES_TRICICLO = ("triciclo", "triciclos", "trimoto", "trimotos")

PAGE_LENGTH = 100
PAUSA_ENTRE_PAGINAS = 1.0  # segundos (buena practica / no saturar el sitio)

# Carpeta de salida: <repo>/datos/revolico
REPO_ROOT = Path(__file__).resolve().parent.parent
SALIDA_DIR = REPO_ROOT / "datos" / "revolico"


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def log(msg):
    print(msg, flush=True)


def parse_fecha(iso_str):
    """Convierte '2026-10-17T10:44:44.879Z' a datetime UTC con zona."""
    if not iso_str:
        return None
    try:
        limpio = iso_str.replace("Z", "+00:00")
        return datetime.fromisoformat(limpio)
    except ValueError:
        return None


def es_electrica(titulo):
    t = (titulo or "").lower()
    return any(c in t for c in CLAVES_ELECTRICAS)


def es_triciclo(titulo):
    t = (titulo or "").lower()
    return any(c in t for c in CLAVES_TRICICLO)


def obtener_next_data(session, subcategory, page, con_imagenes):
    """Descarga una pagina de resultados y devuelve el JSON de __NEXT_DATA__."""
    url = f"{BASE_URL}/search"
    params = {
        "category": CATEGORY,
        "subcategory": subcategory,
        "province": PROVINCIA,
        "page": page,
    }
    if con_imagenes:
        params["images"] = "on"
    resp = session.get(url, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        resp.text,
        re.S,
    )
    if not m:
        raise RuntimeError("No se encontro __NEXT_DATA__ en la respuesta")
    return json.loads(m.group(1))


def extraer_anuncios(apollo, categoria):
    """Extrae la lista de anuncios (sin telefonos, direcciones ni triciclos)."""
    anuncios = []
    for clave, valor in apollo.items():
        if not clave.startswith("AdType:"):
            continue
        titulo = (valor.get("title") or "").strip()
        # Excluir triciclos
        if es_triciclo(titulo):
            continue
        fecha_utc = parse_fecha(valor.get("updatedOnToOrder"))
        fecha_hab = fecha_utc.astimezone(TZ_HABANA) if fecha_utc else None
        permalink = valor.get("permalink", "")
        anuncios.append(
            {
                "id": valor.get("id", ""),
                "categoria": categoria["nombre"],
                "categoria_clave": categoria["clave"],
                "titulo": titulo,
                "precio": valor.get("price", ""),
                "moneda": valor.get("currency", ""),
                "es_electrica": es_electrica(titulo),
                "url": f"{BASE_URL}{permalink}" if permalink else "",
                "fecha_utc": fecha_utc.isoformat() if fecha_utc else "",
                "fecha_habana": fecha_hab.isoformat() if fecha_hab else "",
                "imagenes": valor.get("imagesCount", 0),
                "vistas": valor.get("viewCount", 0),
                "promocionado": bool(valor.get("isPromoted", False)),
            }
        )
    return anuncios


# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------
def scrape_categoria(session, categoria, corte, max_paginas, con_imagenes):
    """Recorre las paginas de una categoria hasta superar la fecha de corte."""
    log(f"\n=== {categoria['nombre']} ({categoria['subcategory']}) ===")
    encontrados = []
    page = 1
    while True:
        if max_paginas and page > max_paginas:
            log(f"  Limite de {max_paginas} paginas alcanzado.")
            break
        try:
            data = obtener_next_data(
                session, categoria["subcategory"], page, con_imagenes
            )
        except Exception as e:
            log(f"  Error en pagina {page}: {e}")
            break

        apollo = data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})
        anuncios = extraer_anuncios(apollo, categoria)
        if not anuncios:
            log(f"  Pagina {page}: sin anuncios. Fin.")
            break

        dentro = 0
        mas_antiguo = None
        for a in anuncios:
            f = parse_fecha(a["fecha_utc"])
            if f is None:
                continue
            if mas_antiguo is None or f < mas_antiguo:
                mas_antiguo = f
            if f >= corte:
                encontrados.append(a)
                dentro += 1

        log(f"  Pagina {page}: {len(anuncios)} anuncios, {dentro} dentro del rango.")

        # Como la lista viene ordenada por fecha desc, si el mas antiguo de la
        # pagina ya es anterior al corte, no hace falta seguir.
        if mas_antiguo is not None and mas_antiguo < corte:
            log("  Se alcanzo la fecha de corte. Fin de la categoria.")
            break

        page += 1
        time.sleep(PAUSA_ENTRE_PAGINAS)

    log(f"  Total en rango: {len(encontrados)}")
    return encontrados


# ---------------------------------------------------------------------------
# Guardado de datos crudos
# ---------------------------------------------------------------------------
def guardar(anuncios, dias, con_imagenes, nombres_categorias):
    SALIDA_DIR.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now(TZ_HABANA)
    sello = ahora.strftime("%Y%m%d_%H%M")

    # JSON crudo
    ruta_json = SALIDA_DIR / f"anuncios_revolico_{sello}.json"
    meta = {
        "fuente": "Revolico",
        "provincia": "La Habana",
        "categorias": nombres_categorias,
        "dias": dias,
        "solo_con_imagen": con_imagenes,
        "generado_habana": ahora.isoformat(),
        "total": len(anuncios),
        "anuncios": anuncios,
    }
    ruta_json.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # CSV (utf-8-sig para Excel)
    ruta_csv = SALIDA_DIR / f"anuncios_revolico_{sello}.csv"
    columnas = [
        "id", "categoria", "categoria_clave", "titulo", "precio", "moneda",
        "es_electrica", "url", "fecha_utc", "fecha_habana", "imagenes",
        "vistas", "promocionado",
    ]
    with ruta_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(anuncios)

    log(f"\nDatos guardados:\n  - {ruta_csv}\n  - {ruta_json}")
    return ruta_csv, ruta_json


def resumen_tabla(anuncios):
    """Genera y muestra un resumen tabulado por categoria, y guarda un .md."""
    from collections import defaultdict

    grupos = defaultdict(list)
    for a in anuncios:
        grupos[a["categoria"]].append(a)

    def _num(x):
        return x if isinstance(x, (int, float)) else None

    filas = []
    for cat in sorted(grupos):
        lista = grupos[cat]
        precios = [_num(a["precio"]) for a in lista]
        precios = [p for p in precios if p is not None]
        n = len(lista)
        minimo = min(precios) if precios else 0
        maximo = max(precios) if precios else 0
        promedio = (sum(precios) / len(precios)) if precios else 0
        elec = sum(1 for a in lista if a["es_electrica"])
        filas.append((cat, n, elec, minimo, maximo, promedio))

    # Tabla en consola
    encabezado = f"{'Categoria':<20}{'Anuncios':>9}{'Electricas':>12}{'Min':>8}{'Max':>8}{'Promedio':>10}"
    log("\n" + encabezado)
    log("-" * len(encabezado))
    for cat, n, elec, minimo, maximo, promedio in filas:
        log(f"{cat:<20}{n:>9}{elec:>12}{minimo:>8.0f}{maximo:>8.0f}{promedio:>10.0f}")
    total = sum(f[1] for f in filas)
    log("-" * len(encabezado))
    log(f"{'TOTAL':<20}{total:>9}")

    # Resumen en Markdown
    ahora = datetime.now(TZ_HABANA)
    ruta_md = SALIDA_DIR / f"resumen_revolico_{ahora.strftime('%Y%m%d_%H%M')}.md"
    lineas = [
        "# Resumen de anuncios de Revolico - La Habana",
        "",
        f"- **Generado (La Habana):** {ahora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Total de anuncios:** {total}",
        "",
        "| Categoria | Anuncios | Electricas | Precio min | Precio max | Precio promedio |",
        "|-----------|---------:|-----------:|-----------:|-----------:|----------------:|",
    ]
    for cat, n, elec, minimo, maximo, promedio in filas:
        lineas.append(
            f"| {cat} | {n} | {elec} | {minimo:.0f} | {maximo:.0f} | {promedio:.0f} |"
        )
    ruta_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    log(f"\nResumen tabulado guardado en:\n  - {ruta_md}")


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Scraper de anuncios de Revolico (La Habana)"
    )
    parser.add_argument(
        "--dias", type=int, default=7, help="Dias hacia atras (por defecto 7)"
    )
    parser.add_argument(
        "--categorias",
        default=",".join(CATEGORIAS_POR_DEFECTO),
        help="Categorias separadas por coma: motos, electricas, bicicletas "
        "(por defecto: motos,electricas)",
    )
    parser.add_argument(
        "--sin-imagenes",
        action="store_true",
        help="Incluir anuncios sin imagen (por defecto solo con imagen)",
    )
    parser.add_argument(
        "--max-paginas",
        type=int,
        default=0,
        help="Maximo de paginas por categoria (0 = sin limite)",
    )
    args = parser.parse_args()

    con_imagenes = not args.sin_imagenes

    claves = [c.strip() for c in args.categorias.split(",") if c.strip()]
    seleccion = {}
    for clave in claves:
        if clave in CATEGORIAS:
            seleccion[clave] = CATEGORIAS[clave]
        else:
            log(f"Aviso: categoria desconocida '{clave}' (ignorada)")
    if not seleccion:
        log("No hay categorias validas. Usa: motos, electricas, bicicletas")
        sys.exit(1)

    ahora = datetime.now(TZ_HABANA)
    corte = ahora - timedelta(days=args.dias)
    log(f"Zona horaria: America/Havana ({ahora.strftime('%Y-%m-%d %H:%M')})")
    log(f"Rango: desde {corte.strftime('%Y-%m-%d %H:%M')} hasta {ahora.strftime('%Y-%m-%d %H:%M')}")
    log(f"Categorias: {', '.join(v['nombre'] for v in seleccion.values())}")
    log(f"Solo con imagen: {con_imagenes}")

    session = requests.Session()
    todos = []
    for clave, categoria in seleccion.items():
        todos.extend(
            scrape_categoria(
                session, categoria, corte, args.max_paginas, con_imagenes
            )
        )

    # Eliminar duplicados por id
    unicos = {}
    for a in todos:
        unicos[a["id"]] = a
    todos = sorted(unicos.values(), key=lambda x: x["fecha_utc"], reverse=True)

    log(f"\nTotal de anuncios unicos en rango: {len(todos)}")
    if todos:
        guardar(
            todos,
            args.dias,
            con_imagenes,
            [v["nombre"] for v in seleccion.values()],
        )
        resumen_tabla(todos)
    else:
        log("No se encontraron anuncios en el rango indicado.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nInterrumpido por el usuario.")
        sys.exit(1)
