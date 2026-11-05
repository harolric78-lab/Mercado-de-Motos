#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe publico, las metricas y los graficos del mercado.

Lee `data/processed/anuncios_limpios.json` y `data/processed/cortes/`, y escribe:
  - reports/informe_mercado.md
  - reports/metricas/resumen_mercado.json
  - reports/metricas/resumen_mercado.csv
  - reports/graficos/*.png

Uso:
    python src/analisis/generar_reporte.py
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BASE = Path(__file__).resolve().parents[2]
CLEAN = BASE / "data" / "processed"
REPORTS = BASE / "reports"
GRAFICOS = REPORTS / "graficos"
METRICAS = REPORTS / "metricas"

CATEGORIAS = {
    "motos_combustion": "Motos de Combustión",
    "motos_electricas": "Motos Eléctricas",
    "bicicletas_electricas": "Bicicletas Eléctricas",
    "patinetes": "Patinetes",
}
COLORES = {
    "motos_combustion": "#c0392b",
    "motos_electricas": "#2471a3",
    "bicicletas_electricas": "#1e8449",
    "patinetes": "#b9770e",
}
MARCAS = (
    "Topmaq", "JMD", "Mountain", "Challenger", "Yoazaky", "Vedca", "Bucatti",
    "Motico", "Mishozuki", "MAF", "Kvitova", "Italy", "Katzu", "Krathos",
    "Mikazuki", "Unison", "Xmotors", "Motorstreck", "Haojiang", "Lifan",
    "Trek", "Torvan", "Bevomecon", "Protenzza", "Halcón", "Rali", "OneBot",
    "Fly Racing", "Delta", "Jin", "Acorazada", "Trapper", "Suzuki", "Honda",
    "Yamaha", "Cz", "Etz", "GN", "AX", "CBR",
)


def norm(texto) -> str:
    texto = unicodedata.normalize("NFKD", str(texto or ""))
    texto = "".join(c for c in texto if not unicodedata.combining(c)).lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def cargar_json(ruta: Path, clave: str = "registros"):
    payload = json.loads(ruta.read_text(encoding="utf-8"))
    return payload, payload.get(clave, [])


def precios(registros):
    return [
        float(registro["precio_usd"])
        for registro in registros
        if registro.get("moneda") == "USD"
        and registro.get("precio_usd") is not None
        and registro.get("precio_valido")
    ]


def resumen_precios(registros):
    valores = precios(registros)
    if not valores:
        return {"n": 0, "min": None, "p25": None, "mediana": None, "p75": None, "max": None, "promedio": None, "desviacion": None}
    valores.sort()
    cuartiles = statistics.quantiles(valores, n=4) if len(valores) >= 2 else [valores[0], valores[0], valores[0]]
    return {
        "n": len(valores),
        "min": round(valores[0], 2),
        "p25": round(cuartiles[0], 2),
        "mediana": round(statistics.median(valores), 2),
        "p75": round(cuartiles[2], 2),
        "max": round(valores[-1], 2),
        "promedio": round(statistics.mean(valores), 2),
        "desviacion": round(statistics.pstdev(valores), 2) if len(valores) > 1 else 0.0,
    }


def demanda(registros):
    vistas = [int(registro.get("vistas") or 0) for registro in registros]
    return {
        "anuncios": len(registros),
        "vistas_totales": sum(vistas),
        "vistas_medianas": round(statistics.median(vistas), 1) if vistas else 0,
        "vistas_promedio": round(statistics.mean(vistas), 1) if vistas else 0,
    }


def marcas(registros):
    conteo = Counter()
    for registro in registros:
        texto = norm(registro.get("titulo"))
        for marca in MARCAS:
            if re.search(rf"(?<![0-9a-z]){re.escape(norm(marca))}(?![0-9a-z])", texto):
                conteo[marca] += 1
                break
    return conteo.most_common(10)


def metricas_categoria(registros):
    return {
        "total": len(registros),
        "precios": resumen_precios(registros),
        "demanda": demanda(registros),
    }


def guardar_graficos(por_categoria, metricas, top_marcas):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    claves = list(CATEGORIAS)
    nombres = [CATEGORIAS[clave] for clave in claves]

    fig, ax = plt.subplots(figsize=(9, 5))
    valores = [por_categoria[clave]["total"] for clave in claves]
    ax.barh(nombres, valores, color=[COLORES[clave] for clave in claves])
    for i, valor in enumerate(valores):
        ax.text(valor, i, f" {valor:,}", va="center", fontsize=9)
    ax.set_xlabel("Anuncios")
    ax.set_title("Composición del mercado depurado")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAFICOS / "01_composicion.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    medianas = [por_categoria[clave]["precios"]["mediana"] or 0 for clave in claves]
    p25 = [por_categoria[clave]["precios"]["p25"] or 0 for clave in claves]
    p75 = [por_categoria[clave]["precios"]["p75"] or 0 for clave in claves]
    errores = [[max(0, m - a) for m, a in zip(medianas, p25)], [max(0, b - m) for m, b in zip(medianas, p75)]]
    ax.bar(nombres, medianas, yerr=errores, capsize=6, color=[COLORES[clave] for clave in claves])
    ax.set_ylabel("USD")
    ax.set_title("Precio mediano por categoría (rango intercuartílico)")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "02_precios.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    vistas = [por_categoria[clave]["demanda"]["vistas_medianas"] for clave in claves]
    ax.bar(nombres, vistas, color=[COLORES[clave] for clave in claves])
    ax.set_ylabel("Vistas medianas")
    ax.set_title("Demanda relativa por categoría")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "03_demanda.png", dpi=150)
    plt.close(fig)

    if top_marcas:
        fig, ax = plt.subplots(figsize=(9, 5))
        etiquetas = [marca for marca, _ in top_marcas]
        valores = [valor for _, valor in top_marcas]
        ax.bar(etiquetas, valores, color="#5d6d7e")
        ax.set_ylabel("Anuncios")
        ax.set_title("Marcas más anunciadas")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        fig.savefig(GRAFICOS / "05_marcas.png", dpi=150)
        plt.close(fig)


def guardar_cortes(cortes):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    if not cortes:
        return
    claves = list(CATEGORIAS)
    etiquetas = sorted(cortes)
    ancho = 0.2
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, clave in enumerate(claves):
        valores = [cortes[etiqueta]["categorias"].get(clave, 0) for etiqueta in etiquetas]
        posiciones = [x + i * ancho for x in range(len(etiquetas))]
        ax.bar(posiciones, valores, width=ancho, label=CATEGORIAS[clave], color=COLORES[clave])
    ax.set_xticks([x + 1.5 * ancho for x in range(len(etiquetas))])
    ax.set_xticklabels(etiquetas)
    ax.set_ylabel("Anuncios")
    ax.set_title("Últimos cortes")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "04_evolucion.png", dpi=150)
    plt.close(fig)


def main() -> int:
    payload, registros = cargar_json(CLEAN / "anuncios_limpios.json")
    por_categoria = {}
    for clave in CATEGORIAS:
        subset = [registro for registro in registros if registro.get("categoria") == clave]
        por_categoria[clave] = metricas_categoria(subset)

    top_marcas = marcas(registros)
    cortes = {}
    for ruta in sorted((CLEAN / "cortes").glob("corte_*.json")):
        corte, datos = cargar_json(ruta)
        cortes[corte.get("corte", ruta.stem)] = {
            "total": corte.get("total", len(datos)),
            "categorias": dict(Counter(registro.get("categoria") for registro in datos)),
        }

    REPORTS.mkdir(parents=True, exist_ok=True)
    METRICAS.mkdir(parents=True, exist_ok=True)
    GRAFICOS.mkdir(parents=True, exist_ok=True)

    metricas = {
        "generado": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "total": len(registros),
        "categorias": por_categoria,
        "marcas": top_marcas,
        "cortes": cortes,
    }
    (METRICAS / "resumen_mercado.json").write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (METRICAS / "resumen_mercado.csv").open("w", encoding="utf-8", newline="") as handle:
        escritor = csv.writer(handle)
        escritor.writerow(["categoria", "anuncios", "precio_mediano_usd", "precio_p25_usd", "precio_p75_usd", "vistas_medianas"])
        for clave, nombre in CATEGORIAS.items():
            datos = por_categoria[clave]
            escritor.writerow([
                nombre,
                datos["total"],
                datos["precios"]["mediana"],
                datos["precios"]["p25"],
                datos["precios"]["p75"],
                datos["demanda"]["vistas_medianas"],
            ])

    guardar_graficos(por_categoria, metricas, top_marcas)
    guardar_cortes(cortes)

    lineas = [
        "# Mercado de motos en Cuba",
        "",
        f"Informe generado el {metricas['generado'][:10]} a partir de {len(registros):,} anuncios depurados.",
        "",
        "El dataset público contiene únicamente las cuatro categorías oficiales del proyecto.",
        "",
        "## Composición",
        "",
        "| Categoría | Anuncios | Precio mediano USD | P25 USD | P75 USD | Vistas medianas |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for clave, nombre in CATEGORIAS.items():
        datos = por_categoria[clave]
        precios_datos = datos["precios"]
        lineas.append(
            f"| {nombre} | {datos['total']:,} | {precios_datos['mediana'] or '—'} | "
            f"{precios_datos['p25'] or '—'} | {precios_datos['p75'] or '—'} | {datos['demanda']['vistas_medianas']} |"
        )

    lineas += [
        "",
        "![Composición](graficos/01_composicion.png)",
        "",
        "## Precios",
        "",
        "![Precios](graficos/02_precios.png)",
        "",
        "## Demanda",
        "",
        "![Demanda](graficos/03_demanda.png)",
        "",
        "## Últimos cortes",
        "",
        "| Corte | Anuncios | Motos de Combustión | Motos Eléctricas | Bicicletas Eléctricas | Patinetes |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for etiqueta in sorted(cortes):
        datos = cortes[etiqueta]
        cats = datos["categorias"]
        lineas.append(
            f"| {etiqueta} | {datos['total']:,} | {cats.get('motos_combustion', 0)} | "
            f"{cats.get('motos_electricas', 0)} | {cats.get('bicicletas_electricas', 0)} | {cats.get('patinetes', 0)} |"
        )

    lineas += [
        "",
        "![Evolución](graficos/04_evolucion.png)",
        "",
        "## Marcas",
        "",
        "| Marca | Anuncios |",
        "|---|---:|",
    ]
    for marca, valor in top_marcas:
        lineas.append(f"| {marca} | {valor} |")
    lineas += [
        "",
        "![Marcas](graficos/05_marcas.png)",
        "",
        "## Fuentes y método",
        "",
        "- Fuente: anuncios públicos de Revolico (La Habana).",
        "- Moneda de los precios: USD; los anuncios en CUP se conservan para conteo, pero no entran en las estadísticas de precio.",
        "- La clasificación usa las cuatro categorías oficiales y un proceso de deduplicación por identificador y por repetición exacta.",
        "- Los datos se publican en `data/processed/`; los crudos depurados están en `data/raw/revolico/`.",
    ]
    (REPORTS / "informe_mercado.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print(f"Informe: {REPORTS / 'informe_mercado.md'}")
    print(f"Métricas: {METRICAS}")
    print(f"Gráficos: {GRAFICOS}")
    print(f"Total: {len(registros)}")
    for clave, nombre in CATEGORIAS.items():
        print(f"  {nombre}: {por_categoria[clave]['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
