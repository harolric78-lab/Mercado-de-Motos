#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisis de los 30 anuncios mas recientes de Revolico (La Habana).

Toma el JSON de datos crudos mas reciente de `datos/revolico/` y genera un
informe con los 30 anuncios mas recientes de:

    - Motos de Combustion
    - Motos Electricas (bicicletas/motos electricas, sin triciclos)

Uso:
    python top30_recientes.py
    python top30_recientes.py --archivo datos/revolico/anuncios_revolico_XXXX.json
"""

import argparse
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
    "motos_electricas": "Motos Electricas (bicicletas/motos electricas, sin triciclos)",
}


def json_mas_reciente():
    archivos = sorted(DATOS_DIR.glob("anuncios_revolico_*.json"))
    if not archivos:
        raise SystemExit("No hay archivos de datos en datos/revolico/")
    return archivos[-1]


def num(precio):
    return precio if isinstance(precio, (int, float)) else None


def estadisticas(anuncios):
    precios = [num(a["precio"]) for a in anuncios]
    precios = [p for p in precios if p is not None]
    monedas = {}
    for a in anuncios:
        monedas[a["moneda"]] = monedas.get(a["moneda"], 0) + 1
    return {
        "total": len(anuncios),
        "min": min(precios) if precios else 0,
        "max": max(precios) if precios else 0,
        "prom": (sum(precios) / len(precios)) if precios else 0,
        "monedas": monedas,
    }


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
    parser = argparse.ArgumentParser(description="Analisis de los 30 anuncios mas recientes")
    parser.add_argument("--archivo", default=None, help="Ruta al JSON de datos")
    args = parser.parse_args()

    ruta = Path(args.archivo) if args.archivo else json_mas_reciente()
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    anuncios = datos["anuncios"]

    ahora = datetime.now(TZ_HABANA)
    lineas = [
        "# Analisis: 30 anuncios mas recientes de Revolico (La Habana)",
        "",
        f"- **Fuente de datos:** `{ruta.name}`",
        f"- **Generado (La Habana):** {ahora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Total en el dataset:** {len(anuncios)} anuncios",
        "",
    ]

    for clave, nombre in GRUPOS.items():
        grupo = [a for a in anuncios if a.get("categoria_clave") == clave]
        grupo = sorted(grupo, key=lambda x: x.get("fecha_utc", ""), reverse=True)[:TOP]
        st = estadisticas(grupo)

        lineas += [
            f"## {nombre}",
            "",
            f"- **Anuncios (top {TOP}):** {st['total']}",
            f"- **Precio min / prom / max:** {st['min']:.0f} / {st['prom']:.0f} / {st['max']:.0f}",
            f"- **Monedas:** {', '.join(f'{k}: {v}' for k, v in st['monedas'].items())}",
            "",
            "| # | Titulo | Precio | Moneda | Fecha (La Habana) | Enlace |",
            "|--:|--------|-------:|--------|-------------------|--------|",
        ]
        for i, a in enumerate(grupo, 1):
            lineas.append(
                f"| {i} | {escapar(a['titulo'])} | {a['precio']} | {a['moneda']} | "
                f"{fecha_corta(a['fecha_utc'])} | [ver]({a['url']}) |"
            )
        lineas.append("")

    INFORMES_DIR.mkdir(parents=True, exist_ok=True)
    ruta_md = INFORMES_DIR / f"analisis_top30_{ahora.strftime('%Y%m%d_%H%M')}.md"
    ruta_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print("\n".join(lineas))
    print(f"\nInforme guardado en: {ruta_md}")


if __name__ == "__main__":
    main()
