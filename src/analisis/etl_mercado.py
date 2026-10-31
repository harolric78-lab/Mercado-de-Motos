#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL del mercado de motos en La Habana.

Lee los datos crudos ya depurados de `data/raw/revolico/`, normaliza los
campos, clasifica cada anuncio en una de las cuatro categorias oficiales,
elimina duplicados y escribe una salida auxiliar en `data/interim/`.
El dataset publico consolidado de `data/processed/` no se sobrescribe.

Uso:
    python src/analisis/etl_mercado.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "raw" / "revolico"
CLEAN = BASE / "data" / "interim"

CATEGORIAS = {
    "motos_combustion": "Motos de Combustión",
    "motos_electricas": "Motos Eléctricas",
    "bicicletas_electricas": "Bicicletas Eléctricas",
    "patinetes": "Patinetes",
}

PATINETE = ("patinete", "patineta", "monopatin", "patin electrico", "patin electrica")
BICICLETA = ("bicicleta", "bicicl", "bicimoto", "bicimot", "ebike", "e bike", "bici")
MOTO = ("moto", "motocicleta", "motico", "motoneta", "scooter", "vespa",
        "ciclomotor", "moped", "minimoto")
COMBUSTION = ("combustion", "combustible", "gasolina", "petroleo", "diesel",
              "cilindrada", "4 tiempo", "2 tiempo")
ELECTRICA = ("electrica", "electrico", "electric", "bateria", "litio", "lithium",
             "lifepo", "48v", "60v", "72v", "84v", "96v")


def sin_acentos(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii")


def norm(texto) -> str:
    texto = sin_acentos(str(texto or "")).lower()
    texto = re.sub(r"[^a-z0-9$.,]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def contiene(texto: str, claves) -> bool:
    return any(re.search(rf"(?<![0-9a-z]){re.escape(clave)}", texto) for clave in claves)


def clasificar(titulo: str, descripcion: str, sitio: str) -> str:
    texto = norm(f"{titulo} {descripcion}")
    if contiene(texto, PATINETE):
        return "patinetes"
    if contiene(texto, BICICLETA) and (contiene(texto, ELECTRICA) or "electric" in norm(sitio)):
        return "bicicletas_electricas"
    if contiene(texto, COMBUSTION) or "combustion" in norm(sitio):
        return "motos_combustion"
    if contiene(texto, BICICLETA):
        return "bicicletas_electricas"
    if contiene(texto, MOTO):
        return "motos_electricas"
    return "motos_electricas" if "electric" in norm(sitio) else "motos_combustion"


def precio(valor):
    if valor is None or valor == "":
        return None
    if isinstance(valor, bool):
        return None
    try:
        numero = float(str(valor).replace(",", ""))
    except ValueError:
        return None
    return round(numero, 2) if numero > 0 else None


def fecha(registro) -> str:
    for clave in ("fecha_habana", "fecha_iso", "updatedOnByUser", "fecha_publicacion"):
        valor = registro.get(clave)
        if valor:
            return str(valor)
    return ""


def titulo(registro) -> str:
    return str(registro.get("titulo") or registro.get("title") or "").strip()


def descripcion(registro) -> str:
    return str(
        registro.get("descripcion")
        or registro.get("description")
        or registro.get("shortDescription")
        or ""
    ).strip()


def url(registro) -> str:
    valor = str(registro.get("url") or registro.get("permalink") or "")
    return "https://www.revolico.com" + valor if valor.startswith("/") else valor


def cargar() -> list[dict]:
    registros = []
    for ruta in sorted(RAW.glob("*.json")):
        payload = json.loads(ruta.read_text(encoding="utf-8"))
        for registro in payload.get("anuncios", []):
            item = dict(registro)
            item["_archivo_origen"] = ruta.name
            item["_titulo"] = titulo(registro)
            item["_descripcion"] = descripcion(registro)
            item["_fecha"] = fecha(registro)
            item["_fecha_dia"] = item["_fecha"][:10]
            item["_id"] = str(registro.get("id") or "")
            item["_precio"] = precio(
                registro.get("precio") if registro.get("precio") is not None else registro.get("price")
            )
            item["_moneda"] = str(registro.get("moneda") or registro.get("currency") or "USD").upper()
            item["_vistas"] = registro.get("vistas", registro.get("viewCount", 0)) or 0
            item["_imagenes"] = registro.get("imagenes", registro.get("imagesCount", 0)) or 0
            item["_sitio"] = str(
                registro.get("categoria_sitio")
                or registro.get("categoria")
                or registro.get("_subcategoria")
                or ""
            )
            registros.append(item)
    return registros


def limpiar(registros: list[dict]) -> list[dict]:
    por_id = {}
    for registro in registros:
        if not registro["_id"]:
            continue
        anterior = por_id.get(registro["_id"])
        if anterior is None:
            por_id[registro["_id"]] = registro
            continue
        puntos = bool(registro["_descripcion"]) * 2 + registro["_vistas"] + registro["_imagenes"] * 0.1
        puntos_prev = bool(anterior["_descripcion"]) * 2 + anterior["_vistas"] + anterior["_imagenes"] * 0.1
        if puntos > puntos_prev:
            por_id[registro["_id"]] = registro

    vistos = set()
    finales = []
    genericos = {"bicimoto", "moto electrica", "bicicleta electrica", "patineta electrica"}
    for registro in sorted(
        por_id.values(),
        key=lambda item: (-item["_vistas"], item["_fecha"]),
    ):
        clave_titulo = norm(registro["_titulo"])
        generico = len(clave_titulo) < 25 or clave_titulo in genericos
        clave = (clave_titulo, registro["_precio"], registro["_moneda"], registro["_fecha_dia"])
        if not generico and registro["_precio"] and clave in vistos:
            continue
        vistos.add(clave)
        finales.append(registro)

    salida = []
    for registro in finales:
        categoria = clasificar(registro["_titulo"], registro["_descripcion"], registro["_sitio"])
        precio_valor = precio(registro.get("precio") if registro.get("precio") is not None else registro.get("price"))
        moneda = str(registro.get("moneda") or registro.get("currency") or "USD").upper()
        salida.append({
            "id": registro["_id"],
            "fuente": "Revolico",
            "archivo_origen": registro["_archivo_origen"],
            "titulo": registro["_titulo"],
            "descripcion": registro["_descripcion"],
            "categoria": categoria,
            "categoria_clave": categoria,
            "categoria_nombre": CATEGORIAS[categoria],
            "categoria_sitio": registro["_sitio"],
            "precio": precio_valor,
            "moneda": moneda,
            "precio_usd": precio_valor if moneda == "USD" else None,
            "fecha_iso": registro["_fecha"],
            "fecha_habana": registro["_fecha"],
            "fecha_dia": registro["_fecha"][:10],
            "vistas": registro.get("vistas", registro.get("viewCount", 0)),
            "imagenes": registro.get("imagenes", registro.get("imagesCount", 0)),
            "url": url(registro),
            "ubicacion": "La Habana",
            "marca": "",
            "modelo": "",
            "modelo_mostrar": "General",
            "marca_mostrar": "SIN_MARCA",
            "precio_valido": precio_valor is not None and moneda == "USD" and precio_valor >= 50,
            "precio_atipico": False,
        })
    salida.sort(key=lambda registro: (registro["fecha_habana"], registro["id"]), reverse=True)
    return salida


def escribir(registros: list[dict]) -> None:
    CLEAN.mkdir(parents=True, exist_ok=True)
    generado = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    payload = {
        "generado": generado,
        "fuentes": sorted({registro["archivo_origen"] for registro in registros}),
        "total": len(registros),
        "registros": registros,
    }
    (CLEAN / "anuncios_limpios.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    columnas = [
        "id", "titulo", "descripcion", "categoria", "categoria_clave", "categoria_nombre",
        "precio", "moneda", "precio_usd", "fecha_habana", "fecha_dia", "vistas", "imagenes",
        "url", "ubicacion", "marca", "modelo", "modelo_mostrar", "marca_mostrar",
        "precio_valido", "precio_atipico",
    ]
    with (CLEAN / "anuncios_limpios.csv").open("w", encoding="utf-8", newline="") as handle:
        escritor = csv.DictWriter(handle, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(registros)

    for clave, nombre in CATEGORIAS.items():
        carpeta = CLEAN / clave
        carpeta.mkdir(parents=True, exist_ok=True)
        subset = [registro for registro in registros if registro["categoria"] == clave]
        (carpeta / "anuncios.json").write_text(
            json.dumps({
                "generado": generado,
                "categoria": clave,
                "categoria_nombre": nombre,
                "total": len(subset),
                "registros": subset,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        with (carpeta / "anuncios.csv").open("w", encoding="utf-8", newline="") as handle:
            escritor = csv.DictWriter(handle, fieldnames=columnas, extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(subset)


def main() -> int:
    registros = limpiar(cargar())
    escribir(registros)
    conteo = Counter(registro["categoria"] for registro in registros)
    print(f"Registros limpios: {len(registros)}")
    for clave, nombre in CATEGORIAS.items():
        print(f"  {nombre}: {conteo.get(clave, 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
