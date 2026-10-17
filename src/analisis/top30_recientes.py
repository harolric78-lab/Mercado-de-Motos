#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tabla de los 30 anuncios mas recientes de Revolico (La Habana).

Toma el JSON de datos crudos mas reciente de `datos/revolico/` y genera una
tabla organizada con:

    - Tipo de vehiculo
    - Precio
    - Enlace (URL) de Revolico

Para:
    - Motos de Combustion
    - Motos Electricas (bicicletas/motos electricas, sin triciclos)

Genera un informe Markdown y un CSV en `docs/informes/`.

Uso:
    python top30_recientes.py
    python top30_recientes.py --archivo datos/revolico/anuncios_revolico_XXXX.json
"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ_HABANA = ZoneInfo("America/Havana")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATOS_DIR = REPO_ROOT / "datos" / "revolico"
INFORMES_DIR = REPO_ROOT / "docs" / "informes"
TOP = 30

GRUPOS = {
    "motos_combustion": "Motos de Combustion",
    "motos_electricas": "Motos Electricas (sin triciclos)",
}


def json_mas_reciente():
    archivos = sorted(DATOS_DIR.glob("anuncios_revolico_*.json"))
    if not archivos:
        raise SystemExit("No hay archivos de datos en datos/revolico/")
    return archivos[-1]


def tipo_vehiculo(anuncio):
    """Clasifica el tipo de vehiculo a partir del titulo y la categoria."""
    t = (anuncio.get("titulo") or "").lower()
    cat = anuncio.get("categoria_clave")

    if cat == "motos_combustion":
        if "scooter" in t or "vespa" in t:
            return "Moto de combustion (scooter)"
        if "deportiva" in t or "ninja" in t:
            return "Moto de combustion (deportiva)"
        return "Moto de combustion"

    # Categoria electricas
    if (
        "bicicleta" in t
        or "bici electrica" in t
        or "bici eléctrica" in t
        or "ebike" in t
        or "e-bike" in t
    ):
        return "Bicicleta electrica"
    if "bicimoto" in t:
        return "Bicimoto electrica"
    if "motico" in t or "moto" in t or "scooter" in t:
        return "Moto electrica"
    return "Vehiculo electrico (sin clasificar)"


def fecha_corta(iso):
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso).astimezone(TZ_HABANA)
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso


def escapar(texto):
    return (texto or "").replace("|", "\\|")


def main():
    parser = argparse.ArgumentParser(description="Tabla de los 30 anuncios mas recientes")
    parser.add_argument("--archivo", default=None, help="Ruta al JSON de datos")
    args = parser.parse_args()

    ruta = Path(args.archivo) if args.archivo else json_mas_reciente()
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    anuncios = datos["anuncios"]
    ahora = datetime.now(TZ_HABANA)

    # Reunir los 30 mas recientes de cada grupo
    filas = []
    for clave, nombre in GRUPOS.items():
        grupo = [a for a in anuncios if a.get("categoria_clave") == clave]
        grupo = sorted(grupo, key=lambda x: x.get("fecha_utc", ""), reverse=True)[:TOP]
        for a in grupo:
            filas.append(
                {
                    "grupo": nombre,
                    "tipo_vehiculo": tipo_vehiculo(a),
                    "titulo": a["titulo"],
                    "precio": a["precio"],
                    "moneda": a["moneda"],
                    "fecha_habana": fecha_corta(a["fecha_utc"]),
                    "url": a["url"],
                }
            )

    lineas = [
        "# Tabla: 30 anuncios mas recientes de Revolico (La Habana)",
        "",
        f"- **Fuente de datos:** `{ruta.name}`",
        f"- **Generado (La Habana):** {ahora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Filas:** {len(filas)} (30 por grupo)",
        "",
        "| # | Grupo | Tipo de vehiculo | Titulo | Precio | Moneda | Fecha (La Habana) | Enlace |",
        "|--:|-------|------------------|--------|-------:|--------|-------------------|--------|",
    ]
    for i, f in enumerate(filas, 1):
        lineas.append(
            f"| {i} | {escapar(f['grupo'])} | {escapar(f['tipo_vehiculo'])} | "
            f"{escapar(f['titulo'])} | {f['precio']} | {f['moneda']} | "
            f"{f['fecha_habana']} | [ver]({f['url']}) |"
        )
    lineas.append("")

    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    sello = ahora.strftime("%Y%m%d_%H%M")
    ruta_md = INFORMES_DIR / f"tabla_top30_{sello}.md"
    ruta_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    ruta_csv = INFORMES_DIR / f"tabla_top30_{sello}.csv"
    with ruta_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "grupo", "tipo_vehiculo", "titulo", "precio", "moneda",
                "fecha_habana", "url",
            ],
            extrasaction="ignore",
        )
        w.writeheader()
        w.writerows(filas)

    print("\n".join(lineas))
    print(f"\nInforme guardado en: {ruta_md}\nCSV guardado en: {ruta_csv}")


if __name__ == "__main__":
    main()
