#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL del mercado de motos en La Habana.

Lee los datos crudos de Revolico (y Telegram cuando exista), los normaliza,
elimina duplicados y escribe el dataset limpio en data/clean/.

Uso:
    python src/analisis/etl_mercado.py
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contactos import sanear_contactos  # noqa: E402

BASE = Path(__file__).resolve().parents[2]
RAW_REVOLICO = BASE / "data" / "raw" / "revolico"
RAW_TELEGRAM = BASE / "data" / "raw" / "telegram"
CLEAN = BASE / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Normalizacion de texto
# ---------------------------------------------------------------------------
def sin_acentos(texto: str) -> str:
    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def norm(texto) -> str:
    texto = sin_acentos(str(texto or "")).lower()
    texto = re.sub(r"[^a-z0-9$.,]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


# ---------------------------------------------------------------------------
# Marcas (alias -> nombre canonico)
# ---------------------------------------------------------------------------
ALIAS_MARCAS = {
    "TOPMAQ": ["topmaq", "top maq", "topmac", "topmack"],
    "JMD": ["jmd"],
    "MOUNTAIN": ["mountain"],
    "CHALLENGER": ["challenger"],
    "YOAZAKY": ["yoazaki", "yoazaky", "yoazki", "yoazaky"],
    "VEDCA": ["vedca"],
    "BUCATTI": ["bucatti", "bucati", "bucatti"],
    "MOTICO": ["motico"],
    "MISHOZUKI": ["mishozuki", "mishosuki", "mishozuky", "mishozuki"],
    "MAF": ["maf"],
    "KVITOVA": ["kvitova"],
    "ITALY": ["italy", "italia"],
    "KATZU": ["katzu"],
    "KRATHOS": ["krathos"],
    "MIKAZUKI": ["mikazuki", "mikazuky"],
    "UNISON": ["unison"],
    "XMOTORS": ["xmotors", "x motors"],
    "MOTORSTRECK": ["motorstreck", "motor treck", "motorstreck"],
    "HAOJIANG": ["haojiang"],
    "LIFAN": ["lifan"],
    "TREK": ["trek"],
    "TORVAN": ["torvan"],
    "BEVOMECON": ["bevomecon"],
    "PROTENZZA": ["protenzza"],
    "MRK": ["mrk"],
    "OKDAY": ["okday"],
    "OUPES": ["oupes"],
    "YESELF": ["yeself"],
    "TREVALIX": ["trevalix"],
    "MIDHA": ["midha"],
    "OWAY": ["oway"],
    "LAZER": ["lazer"],
    "VESPA": ["vespa"],
    "SK8": ["sk8"],
    "KAWASAKI": ["kawasaki"],
    "SIERRA": ["sierra"],
    "XIAOMI": ["xiaomi"],
    "SUZUKI": ["suzuki"],
    "YAMAHA": ["yamaha"],
    "HONDA": ["honda"],
    "YAMAKI": ["yamaki"],
    "YADEA": ["yadea"],
    "YATI": ["yati"],
    "DAYI": ["dayi"],
    "JINCHENG": ["jincheng"],
    "JIN": ["jin"],
    "LONCIN": ["loncin"],
    "ZONGSHEN": ["zongshen"],
    "AVA": ["ava"],
    "ONEBOT": ["onebot", "one bot"],
    "MATECH": ["matech"],
    "XMOX": ["xmox"],
    "WYS": ["wys"],
    "UNIZUKI": ["unizuki"],
    "MAOX": ["maox"],
    "VOLTA": ["volta"],
    "ESKUTE": ["eskute"],
    "PROEFIX": ["proefix"],
    "LAITUNING": ["laituning"],
}

_ALIAS_ORDENADOS = sorted(
    ((alias, marca) for marca, alias in ALIAS_MARCAS.items() for alias in alias),
    key=lambda par: -len(par[0]),
)


def detectar_marca(titulo_norm: str) -> str:
    for alias, marca in _ALIAS_ORDENADOS:
        if re.search(rf"\b{re.escape(alias)}\b", titulo_norm):
            return marca
    return ""


# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------
def detectar_modelo(titulo_norm: str, marca: str, categoria: str) -> str:
    # Motos de combustion: codigos conocidos
    patrones_comb = [
        (r"\bgn[ -]?125\b", "GN125"),
        (r"\bgn[ -]?150\b", "GN150"),
        (r"\bax[ -]?100\b", "AX100"),
        (r"\ben[ -]?125\b", "EN125"),
        (r"\bgz[ -]?125\b", "GZ125"),
        (r"\bcgl[ -]?125\b", "CGL125"),
        (r"\bcg[ -]?125\b", "CG125"),
        (r"\brx[ -]?combat\b", "RX Combat"),
        (r"\bcombat\b", "RX Combat"),
        (r"\blifan[ -]?(125|150|200)\b", "Lifan"),
        (r"\bvespa\b", "Vespa"),
    ]
    if categoria == "combustion":
        for patron, modelo in patrones_comb:
            if re.search(patron, titulo_norm):
                if modelo == "Lifan":
                    m = re.search(r"\blifan[ -]?(125|150|200)\b", titulo_norm)
                    return f"Lifan {m.group(1)}" if m else "Lifan"
                return modelo
        m = re.search(r"\b(\d{2,3})\s*(?:cc|cm3)\b", titulo_norm)
        if m and 50 <= int(m.group(1)) <= 400:
            return f"{m.group(1)}cc"
        if re.search(r"\bscooter\b", titulo_norm):
            return "Scooter"
        return ""

    # Vehiculos electricos: codigos cortos conocidos
    codigos = {
        "TANK", "F1", "F2", "F3", "F5", "T3", "T5", "T6", "G5",
        "E5", "E6", "E8", "M3", "S3", "X5", "X6", "X7", "GT",
    }
    for palabra in re.findall(r"\b[a-z0-9]{1,5}\b", titulo_norm):
        if palabra.upper() in codigos:
            return palabra.upper()
    return ""


# ---------------------------------------------------------------------------
# Clasificacion
# ---------------------------------------------------------------------------
EXCLUIR = (
    "triciclo", "trimoto", "motocarro", "mototaxi", "cuatrimoto",
    "cuatriciclo", "repuesto", "repuestos", "despiece", "se vende por parte",
    "se vende por partes", "solo bateria", "vendo bateria", "casco",
    "accesorio", "accesorios",
)


def clasificar(titulo: str, descripcion: str, categoria_sitio: str):
    t = norm(titulo)
    d = norm(descripcion)
    texto = f"{t} {d}"

    if any(x in texto for x in EXCLUIR):
        return None

    if re.search(r"\bpatinetas?\b|\bmonopatin\b|\bhoverboard\b", t):
        return "patinete"
    if re.search(r"\bbicimotos?\b|\bbici[ -]?moto\b", t):
        return "bicimoto"
    if re.search(r"\bbicicletas?\b|\be[ -]?bike\b|\bebike\b", t):
        return "bicicleta_electrica"

    if categoria_sitio == "Motos de Combustion":
        if re.search(r"\bmoto\s+electrica\b|\b100\s*%\s*electrica\b", t):
            return "moto_electrica"
        return "combustion"

    if categoria_sitio == "Motos Electricas":
        return "moto_electrica"

    # Sin categoria de sitio: heuristica por palabras clave
    if re.search(r"\b(?:[0-9]{2,3}\s*(?:cc|cm3)|gasolina|combustion|4t|2t)\b", texto):
        return "combustion"
    if re.search(r"\b(?:litio|electric[oa]s?|[0-9]{2,3}\s*v|[0-9]{3,4}\s*w)\b", texto):
        return "moto_electrica"
    return None


# ---------------------------------------------------------------------------
# Precios y moneda
# ---------------------------------------------------------------------------
def parsear_precio(valor):
    if isinstance(valor, (int, float)):
        return float(valor) if valor > 0 else None
    if isinstance(valor, str):
        limpio = valor.replace(" ", "").replace(",", ".")
        m = re.search(r"(\d+(?:\.\d+)?)", limpio)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                return None
    return None


def normalizar_moneda(valor, titulo: str = "") -> str:
    texto = norm(f"{valor or ''} {titulo}")
    if re.search(r"\b(usd|us\$|cuc|dolar|dolares)\b", texto):
        return "USD"
    if re.search(r"\b(mlc)\b", texto):
        return "MLC"
    if re.search(r"\b(cup|mn|peso|pesos)\b", texto):
        return "CUP"
    return "USD"


# ---------------------------------------------------------------------------
# Lectura de fuentes
# ---------------------------------------------------------------------------
def _fecha(valor):
    if not valor:
        return ""
    try:
        return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except ValueError:
        return ""


def _leer_revolico(ruta: Path):
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    anuncios = datos.get("anuncios") or datos.get("registros") or []
    registros = []
    for a in anuncios:
        scraper = a.get("_scraping") or {}
        titulo = scraper.get("titulo_original") or a.get("titulo") or a.get("title") or ""
        descripcion = (
            scraper.get("descripcion")
            or a.get("descripcion")
            or a.get("description")
            or a.get("shortDescription")
            or ""
        )
        precio = parsear_precio(
            scraper.get("precio_original", a.get("precio", a.get("price")))
        )
        moneda = normalizar_moneda(
            scraper.get("moneda_original") or a.get("moneda") or a.get("currency"),
            titulo,
        )
        categoria_sitio = (
            scraper.get("categoria")
            or a.get("categoria")
            or ""
        )
        categoria_sitio = {
            "electrica": "Motos Electricas",
            "combustion": "Motos de Combustion",
            "patinete": "Motos Electricas",
        }.get(categoria_sitio, categoria_sitio)
        fecha = (
            scraper.get("fecha_publicacion")
            or a.get("fecha_habana")
            or a.get("fecha_publicacion")
            or a.get("updatedOnByUser")
            or ""
        )
        url = (
            scraper.get("url")
            or a.get("url")
            or (
                "https://www.revolico.com" + a.get("permalink", "")
                if a.get("permalink")
                else ""
            )
        )
        categoria = clasificar(titulo, descripcion, categoria_sitio)
        registros.append(
            {
                "id": str(scraper.get("id") or a.get("id") or ""),
                "fuente": "Revolico",
                "archivo_origen": ruta.name,
                "titulo": sanear_contactos(titulo.strip()),
                "descripcion": sanear_contactos(descripcion.strip()),
                "categoria": categoria,
                "categoria_sitio": categoria_sitio,
                "precio": precio,
                "moneda": moneda,
                "precio_usd": precio if (precio and moneda == "USD") else None,
                "fecha_iso": str(fecha),
                "fecha_dia": str(fecha)[:10],
                "vistas": int(a.get("vistas") or a.get("viewCount") or 0),
                "imagenes": int(a.get("imagenes") or a.get("imagesCount") or 0),
                "url": url,
                "ubicacion": "La Habana",
            }
        )
    return registros


def _leer_telegram(ruta: Path):
    """Lee exports JSON de Telegram con estructura {mensajes: [...]}."""
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    mensajes = datos.get("mensajes") or datos.get("messages") or []
    registros = []
    for m in mensajes:
        texto = m.get("texto") or m.get("text") or ""
        titulo = texto.splitlines()[0][:120] if texto else ""
        categoria = clasificar(titulo, texto, "")
        if not categoria:
            continue
        registros.append(
            {
                "id": str(m.get("id") or ""),
                "fuente": "Telegram",
                "archivo_origen": ruta.name,
                "titulo": sanear_contactos(titulo.strip()),
                "descripcion": sanear_contactos(texto.strip()),
                "categoria": categoria,
                "categoria_sitio": "",
                "precio": parsear_precio(m.get("precio")),
                "moneda": normalizar_moneda(m.get("moneda"), texto),
                "precio_usd": parsear_precio(m.get("precio")),
                "fecha_iso": str(m.get("fecha") or ""),
                "fecha_dia": str(m.get("fecha") or "")[:10],
                "vistas": int(m.get("vistas") or 0),
                "imagenes": int(m.get("imagenes") or 0),
                "url": m.get("url") or "",
                "ubicacion": m.get("ubicacion") or "La Habana",
            }
        )
    return registros


# ---------------------------------------------------------------------------
# Limpieza
# ---------------------------------------------------------------------------
def deduplicar(registros):
    por_id = {}
    sin_id = []
    for r in registros:
        if not r["id"]:
            sin_id.append(r)
            continue
        previo = por_id.get(r["id"])
        if previo is None:
            por_id[r["id"]] = r
            continue
        # Conservar el registro con mas informacion
        puntos = (
            bool(r["descripcion"]) * 2 + r["vistas"] + r["imagenes"] * 0.1
        )
        puntos_prev = (
            bool(previo["descripcion"]) * 2 + previo["vistas"] + previo["imagenes"] * 0.1
        )
        if puntos > puntos_prev:
            por_id[r["id"]] = r

    unicos = list(por_id.values()) + sin_id
    id_dupes = len(registros) - len(unicos)

    # Reposts exactos (mismo titulo especifico, precio, moneda y dia)
    vistos = {}
    finales = []
    duplicados_repost = 0
    for r in sorted(unicos, key=lambda x: (-x["vistas"], x["fecha_iso"])):
        clave_titulo = norm(r["titulo"])
        generico = len(clave_titulo) < 25 or clave_titulo in {
            "bicimoto", "moto electrica", "bicicleta electrica", "patineta electrica",
        }
        clave = (clave_titulo, r["precio"], r["moneda"], r["fecha_dia"])
        if not generico and r["precio"] and clave in vistos:
            duplicados_repost += 1
            continue
        vistos[clave] = True
        finales.append(r)
    return finales, id_dupes, duplicados_repost


def main():
    registros = []
    rutas_revolico = sorted(RAW_REVOLICO.glob("*.json")) + sorted(
        (BASE / "data" / "raw").glob("revolico_raw_*.json")
    )
    for ruta in rutas_revolico:
        registros.extend(_leer_revolico(ruta))
    for ruta in sorted(RAW_TELEGRAM.glob("*.json")):
        registros.extend(_leer_telegram(ruta))

    total_bruto = len(registros)
    for r in registros:
        r["marca"] = detectar_marca(norm(r["titulo"]))
        r["modelo"] = detectar_modelo(norm(r["titulo"]), r["marca"], r["categoria"] or "")

    excluidos = [r for r in registros if not r["categoria"]]
    validos = [r for r in registros if r["categoria"]]
    unicos, dup_id, reposts = deduplicar(validos)

    marca_por_modelo = {
        "GN125": "SUZUKI", "GN150": "SUZUKI", "AX100": "SUZUKI",
        "EN125": "SUZUKI", "GZ125": "SUZUKI", "RX Combat": "ITALY",
        "Vespa": "VESPA",
    }
    for r in unicos:
        if not r["marca"] and r["modelo"] in marca_por_modelo:
            r["marca"] = marca_por_modelo[r["modelo"]]
        if not r["marca"] and r["modelo"].startswith("Lifan"):
            r["marca"] = "LIFAN"
        r["modelo_mostrar"] = r["modelo"] or "General"
        r["marca_mostrar"] = r["marca"] or "SIN_MARCA"
        r["precio_valido"] = bool(
            r["precio_usd"] and 100 <= r["precio_usd"] <= 30000
        )
        r["precio_atipico"] = False

    # Outliers extremos por categoria (solo para estadisticas de precio)
    for categoria in {r["categoria"] for r in unicos}:
        vals = sorted(
            r["precio_usd"] for r in unicos
            if r["categoria"] == categoria and r["precio_valido"]
        )
        if len(vals) < 8:
            continue
        q1, _, q3 = statistics.quantiles(vals, n=4)
        iqr = q3 - q1
        lo, hi = q1 - 3 * iqr, q3 + 3 * iqr
        for r in unicos:
            if r["categoria"] != categoria or not r["precio_valido"]:
                continue
            if not (lo <= r["precio_usd"] <= hi):
                r["precio_valido"] = False
                r["precio_atipico"] = True

    campos = [
        "id", "fuente", "archivo_origen", "categoria", "marca", "modelo",
        "precio", "moneda", "precio_usd", "precio_valido", "precio_atipico", "titulo",
        "descripcion", "fecha_iso", "fecha_dia", "vistas", "imagenes",
        "url", "ubicacion", "categoria_sitio",
    ]
    salida = {
        "generado": datetime.now(timezone.utc).isoformat(),
        "fuentes": sorted({r["fuente"] for r in unicos}),
        "total_bruto": total_bruto,
        "total_excluidos": len(excluidos),
        "total_duplicados_id": dup_id,
        "total_duplicados_repost": reposts,
        "total_duplicados": dup_id + reposts,
        "total": len(unicos),
        "registros": unicos,
    }
    (CLEAN / "anuncios_limpios.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (CLEAN / "anuncios_limpios.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(unicos)

    print("=" * 66)
    print("ETL MERCADO — RESUMEN")
    print("=" * 66)
    print(f"  registros brutos:        {total_bruto}")
    print(f"  excluidos (no lista):    {len(excluidos)}")
    print(f"  duplicados eliminados:   {salida['total_duplicados']} "
          f"(id: {dup_id}, reposts: {reposts})")
    print(f"  registros limpios:       {len(unicos)}")
    print(f"  categorias:              {dict(Counter(r['categoria'] for r in unicos))}")
    print(f"  monedas:                 {dict(Counter(r['moneda'] for r in unicos))}")
    print(f"  con precio USD:          {sum(1 for r in unicos if r['precio_usd'])}")
    print(f"  marcas detectadas:       {sum(1 for r in unicos if r['marca'])}")
    print(f"  salida:                  {CLEAN / 'anuncios_limpios.json'}")


if __name__ == "__main__":
    main()
