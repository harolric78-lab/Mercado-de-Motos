#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 4 del pipeline: metricas de precios por categoria.

Calcula, por separado para motos de combustion, motos electricas y patinetes
electricos:

  - cantidad de anuncios
  - precio minimo, maximo, promedio, mediana y desviacion estandar
  - distribucion por rango de precios

Genera:
  - datos/processed/metricas_revolico_<sello>.json / .csv
  - docs/informes/precios_categorias_<sello>.md

Uso:
    python analyze.py
    python analyze.py --archivo datos/processed/revolico_processed_XXXX.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    Logger,
    ahora_habana,
    guardar_csv,
    guardar_json,
    paths,
    sello,
)

CATEGORIAS = ("combustion", "electrica", "patinete")
ETIQUETAS = {
    "combustion": "Motos de combustion",
    "electrica": "Motos electricas",
    "patinete": "Patinetes electricos",
}
# Rangos de precio en USD para la distribucion
RANGOS = [
    (0, 500, "0-500"),
    (500, 1000, "500-1000"),
    (1000, 2000, "1000-2000"),
    (2000, 3000, "2000-3000"),
    (3000, 5000, "3000-5000"),
    (5000, 10000, "5000-10000"),
    (10000, float("inf"), "+10000"),
]


def metricas(precios):
    if not precios:
        return {
            "anuncios": 0, "precio_min": None, "precio_max": None,
            "precio_promedio": None, "mediana": None, "desviacion_estandar": None,
        }
    return {
        "anuncios": len(precios),
        "precio_min": round(min(precios), 2),
        "precio_max": round(max(precios), 2),
        "precio_promedio": round(statistics.mean(precios), 2),
        "mediana": round(statistics.median(precios), 2),
        "desviacion_estandar": round(statistics.stdev(precios), 2) if len(precios) > 1 else 0.0,
    }


def distribucion(precios):
    conteo = {etiqueta: 0 for _a, _b, etiqueta in RANGOS}
    for p in precios:
        for a, b, etiqueta in RANGOS:
            if a <= p < b:
                conteo[etiqueta] += 1
                break
    return conteo


def analizar(registros):
    """Devuelve el diccionario de metricas por categoria."""
    salida = {}
    for cat in CATEGORIAS:
        grupo = [r for r in registros if r.get("categoria") == cat]
        validos = [float(r["precio"]) for r in grupo if r.get("precio_valido")]
        m = metricas(validos)
        m["distribucion_precios"] = distribucion(validos)
        m["monedas"] = dict(Counter(r.get("moneda", "") for r in grupo))
        m["atipicos"] = sum(1 for r in grupo if r.get("es_outlier"))
        m["sin_precio"] = sum(1 for r in grupo if not r.get("precio_valido"))
        salida[cat] = m

    todos_validos = [
        float(r["precio"]) for r in registros if r.get("precio_valido")
    ]
    total = metricas(todos_validos)
    total["distribucion_precios"] = distribucion(todos_validos)
    total["monedas"] = dict(Counter(r.get("moneda", "") for r in registros))
    total["atipicos"] = sum(1 for r in registros if r.get("es_outlier"))
    salida["total"] = total
    return salida


def filas_metricas(metricas_):
    filas = []
    for cat in list(CATEGORIAS) + ["total"]:
        m = metricas_[cat]
        fila = {
            "categoria": cat,
            "etiqueta": ETIQUETAS.get(cat, "Total"),
            "anuncios": m["anuncios"],
            "precio_min": m["precio_min"],
            "precio_max": m["precio_max"],
            "precio_promedio": m["precio_promedio"],
            "mediana": m["mediana"],
            "desviacion_estandar": m["desviacion_estandar"],
            "atipicos": m.get("atipicos", 0),
        }
        for etiqueta in [r[2] for r in RANGOS]:
            fila[f"rango_{etiqueta}"] = m["distribucion_precios"].get(etiqueta, 0)
        filas.append(fila)
    return filas


def informe_markdown(metricas_, registros, origen):
    ahora = ahora_habana()
    lineas = [
        "# Precios de motos en Cuba (Revolico, La Habana)",
        "",
        f"- **Generado (La Habana):** {ahora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Origen de los datos:** {origen}",
        f"- **Anuncios analizados:** {len(registros)}",
        "",
        "## Metricas por categoria",
        "",
        "| Categoria | Anuncios | Min | Max | Promedio | Mediana | Desv. estandar |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for cat in list(CATEGORIAS) + ["total"]:
        m = metricas_[cat]
        etiqueta = ETIQUETAS.get(cat, "Total")
        def f(x):
            return f"{x:,.0f}" if isinstance(x, (int, float)) else "-"
        lineas.append(
            f"| {etiqueta} | {m['anuncios']} | {f(m['precio_min'])} | {f(m['precio_max'])} | "
            f"{f(m['precio_promedio'])} | {f(m['mediana'])} | {f(m['desviacion_estandar'])} |"
        )

    lineas += ["", "## Distribucion por rango de precios", ""]
    encabezado = "| Rango | " + " | ".join(
        ETIQUETAS.get(c, "Total") for c in list(CATEGORIAS) + ["total"]
    ) + " |"
    lineas += [encabezado, "|---" * (len(CATEGORIAS) + 2) + "|"]
    for _a, _b, etiqueta in RANGOS:
        celdas = [str(metricas_[c]["distribucion_precios"].get(etiqueta, 0)) for c in CATEGORIAS]
        celdas.append(str(metricas_["total"]["distribucion_precios"].get(etiqueta, 0)))
        lineas.append(f"| {etiqueta} | " + " | ".join(celdas) + " |")

    atipicos = [r for r in registros if r.get("es_outlier")]
    lineas += ["", "## Anuncios con precio atipico", ""]
    if atipicos:
        lineas += ["| Categoria | Titulo | Precio | Metodo | Z |", "|---|---|---:|---|---:|"]
        for r in atipicos:
            titulo = r["titulo"][:70].replace("|", "/")
            lineas.append(
                f"| {r['categoria']} | {titulo} | {r['precio']:,.0f} | "
                f"{r.get('outlier_metodo','')} | {r.get('outlier_zscore','')} |"
            )
    else:
        lineas.append("Sin precios atipicos detectados.")

    lineas += ["", "## Monedas", ""]
    for moneda, n in sorted(metricas_["total"]["monedas"].items(), key=lambda x: -x[1]):
        lineas.append(f"- {moneda or 'SIN MONEDA'}: {n}")

    return "\n".join(lineas) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Metricas de precios de Revolico")
    ap.add_argument("--archivo", default=None, help="JSON procesado de entrada")
    ap.add_argument("--proyecto", default=None, help="Ruta raiz del proyecto")
    ap.add_argument("--entrada", default=None, help="Carpeta datos/processed")
    ap.add_argument("--salida", default=None, help="Carpeta de salida de metricas")
    args = ap.parse_args()

    p = paths(Path(args.proyecto) if args.proyecto else None)
    entrada = Path(args.entrada) if args.entrada else p["processed"]
    salida = Path(args.salida) if args.salida else p["processed"]
    informes = p["informes"]

    if args.archivo:
        origen = Path(args.archivo)
    else:
        archivos = sorted(entrada.glob("revolico_processed_*.json"))
        if not archivos:
            raise SystemExit(f"No hay datos procesados en {entrada}")
        origen = archivos[-1]

    log = Logger(p["logs"] / f"revolico_{sello()}.log")
    log(f"=== Analisis de precios - {ahora_habana().isoformat()} ===")
    log(f"Origen: {origen}")

    datos = json.loads(origen.read_text(encoding="utf-8"))
    registros = datos.get("registros", [])
    metricas_ = analizar(registros)

    est = sello()
    salida.mkdir(parents=True, exist_ok=True)
    ruta_json = guardar_json(
        salida / f"metricas_revolico_{est}.json",
        {
            "generado_habana": ahora_habana().isoformat(),
            "origen": origen.name,
            "metricas": metricas_,
        },
    )
    filas = filas_metricas(metricas_)
    ruta_csv = guardar_csv(salida / f"metricas_revolico_{est}.csv", filas, list(filas[0].keys()))

    informes.mkdir(parents=True, exist_ok=True)
    ruta_md = informes / f"precios_categorias_{est}.md"
    ruta_md.write_text(informe_markdown(metricas_, registros, origen.name), encoding="utf-8")

    log.log("")
    for cat in list(CATEGORIAS) + ["total"]:
        m = metricas_[cat]
        log.log(
            f"{ETIQUETAS.get(cat,'Total'):<24} n={m['anuncios']:<4} "
            f"min={m['precio_min']} max={m['precio_max']} "
            f"prom={m['precio_promedio']} med={m['mediana']} desv={m['desviacion_estandar']}"
        )
    log.log("")
    log.log(f"Metricas: {ruta_json}")
    log.log(f"Metricas CSV: {ruta_csv}")
    log.log(f"Informe: {ruta_md}")
    log.cerrar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
