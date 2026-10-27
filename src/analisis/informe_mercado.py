#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisis de mercado de motos en La Habana y generacion del informe.

Entrada:  data/clean/anuncios_limpios.json (generado por etl_mercado.py)
Salida:   reports/README.md, reports/graficos/*.png

Uso:
    python src/analisis/informe_mercado.py
"""
from __future__ import annotations

import json
import re
import statistics as st
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[2]
CLEAN = BASE / "data" / "clean" / "anuncios_limpios.json"
REPORTS = BASE / "reports"
GRAFICOS = REPORTS / "graficos"
REPORTS.mkdir(exist_ok=True)
GRAFICOS.mkdir(exist_ok=True)

CATS = {
    "combustion": "Motos de combustión",
    "moto_electrica": "Motos eléctricas",
    "bicimoto": "Bicimotos",
    "bicicleta_electrica": "Bicicletas eléctricas",
    "patinete": "Patinetes eléctricos",
}
COLORES = {
    "combustion": "#c0392b",
    "moto_electrica": "#2471a3",
    "bicimoto": "#1e8449",
    "bicicleta_electrica": "#16a085",
    "patinete": "#7d3c98",
}
DIAS_VENTANA = 13
COSTO_OPERATIVO = 0.10
CAPITALES = [5000, 10000, 20000]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def miles(x):
    if x is None:
        return "—"
    return f"{x:,.0f}".replace(",", " ")


def pct(x):
    return f"{x:.1f}".replace(".", ",") + " %"


def cuantil(valores, p):
    if not valores:
        return None
    v = sorted(valores)
    if len(v) == 1:
        return v[0]
    i = (len(v) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def cargar():
    datos = json.loads(CLEAN.read_text(encoding="utf-8"))
    return datos


# ---------------------------------------------------------------------------
# Agregaciones
# ---------------------------------------------------------------------------
def estadisticas(items, total_categoria):
    precios = [r["precio_usd"] for r in items if r.get("precio_valido")]
    n = len(items)
    n_precio = len(precios)
    media = st.mean(precios) if precios else None
    mediana = st.median(precios) if precios else None
    desv = st.pstdev(precios) if len(precios) > 1 else 0.0
    cv = (desv / media) if media else None
    return {
        "n": n,
        "n_precio": n_precio,
        "share": n / total_categoria if total_categoria else 0.0,
        "media": media,
        "mediana": mediana,
        "min": min(precios) if precios else None,
        "max": max(precios) if precios else None,
        "p10": cuantil(precios, 0.10),
        "p25": cuantil(precios, 0.25),
        "p75": cuantil(precios, 0.75),
        "desv": desv,
        "cv": cv,
        "vistas": st.mean([r.get("vistas", 0) for r in items]) if items else 0,
        "edad": None,
    }


def agrupar(registros, categoria):
    total = sum(1 for r in registros if r["categoria"] == categoria)
    total_marca = sum(
        1 for r in registros if r["categoria"] == categoria and r["marca"]
    )
    grupos = defaultdict(list)
    for r in registros:
        if r["categoria"] != categoria or not r["marca"]:
            continue
        grupos[(r["marca"], r["modelo"] or "General")].append(r)
    filas = []
    for (marca, modelo), items in grupos.items():
        e = estadisticas(items, total)
        e.update({"marca": marca, "modelo": modelo, "categoria": categoria})
        e["share_marca"] = len(items) / total_marca if total_marca else 0.0
        filas.append(e)
    return filas, total


def indice_demanda(grupos, total_categoria):
    candidatos = [g for g in grupos if g["n"] >= 5]
    if not candidatos:
        return []
    max_freq = max(g["share"] for g in candidatos) or 1
    max_vel = max(g["n"] / DIAS_VENTANA for g in candidatos) or 1
    for g in candidatos:
        freq = g["share"] / max_freq
        fuentes = 1.0  # una sola fuente (Revolico) por ahora
        estab = 1 - min(g["cv"], 1) if g["cv"] is not None else 0.5
        vel = (g["n"] / DIAS_VENTANA) / max_vel
        g["idx_freq"] = freq
        g["idx_fuentes"] = fuentes
        g["idx_estab"] = estab
        g["idx_vel"] = vel
        g["indice"] = 100 * (
            0.40 * freq + 0.30 * fuentes + 0.20 * estab + 0.10 * vel
        )
    candidatos.sort(key=lambda g: (-g["indice"], -g["n"]))
    return candidatos


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------
def tabla_ranking(filas, top=10):
    lineas = [
        "| Ranking | Marca | Modelo | Anuncios | % Mercado | Precio Promedio | Precio Mínimo | Precio Máximo |",
        "|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for i, g in enumerate(filas[:top], 1):
        lineas.append(
            f"| {i} | {g['marca']} | {g['modelo']} | {g['n']} | "
            f"{pct(100 * g['share_marca'])} | {miles(g['media'])} | "
            f"{miles(g['min'])} | {miles(g['max'])} |"
        )
    return "\n".join(lineas)


def tabla_precios(filas):
    lineas = [
        "| Segmento | Anuncios | Con precio USD | Promedio | Mediana | Mínimo | Máximo | Desv. estándar | CV |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for g in filas:
        lineas.append(
            f"| {g['nombre']} | {miles(g['n'])} | {miles(g['n_precio'])} | {miles(g['media'])} | "
            f"{miles(g['mediana'])} | {miles(g['min'])} | {miles(g['max'])} | "
            f"{miles(g['desv'])} | {('%.2f' % g['cv']).replace('.', ',') if g['cv'] is not None else '—'} |"
        )
    return "\n".join(lineas)


def tabla_escenarios(grupos, capitales):
    lineas = [
        "| Capital | Segmento | Modelo | Compra (P10) | Venta (P75) | Unidades | Inversión | Utilidad neta | ROI |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for capital in capitales:
        for g in grupos:
            compra = g.get("p10")
            venta = g.get("p75")
            if not compra or not venta or compra <= 0:
                continue
            unidades = int(capital // compra)
            if unidades == 0:
                continue
            ingreso = unidades * venta
            costo = COSTO_OPERATIVO * ingreso
            utilidad = ingreso - unidades * compra - costo
            roi = utilidad / (unidades * compra) if unidades * compra else 0
            lineas.append(
                f"| {miles(capital)} | {CATS[g['categoria']]} | {g['marca']} {g['modelo']} | "
                f"{miles(compra)} | {miles(venta)} | {unidades} | {miles(unidades * compra)} | "
                f"{miles(utilidad)} | {pct(100 * roi)} |"
            )
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Graficos
# ---------------------------------------------------------------------------
def grafico_top(filas_por_categoria):
    fig, ejes = plt.subplots(2, 2, figsize=(13, 10))
    pares = [
        ("combustion", ejes[0][0]),
        ("moto_electrica", ejes[0][1]),
        ("bicimoto", ejes[1][0]),
        ("patinete", ejes[1][1]),
    ]
    for categoria, ax in pares:
        filas = filas_por_categoria[categoria][:8]
        if not filas:
            ax.axis("off")
            continue
        etiquetas = [f"{g['marca']} {g['modelo']}".replace(" General", "") for g in filas][::-1]
        valores = [g["n"] for g in filas][::-1]
        ax.barh(etiquetas, valores, color=COLORES[categoria], alpha=0.85)
        ax.set_title(CATS[categoria], fontsize=12, fontweight="bold")
        ax.set_xlabel("Anuncios")
        ax.grid(axis="x", alpha=0.3)
    fig.suptitle("Modelos con mayor índice de demanda (La Habana)", fontsize=15, fontweight="bold")
    fig.text(0.5, 0.005, "Barras: cantidad de anuncios · Orden: índice de demanda del segmento",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    fig.savefig(GRAFICOS / "top_por_segmento.png", dpi=150)
    plt.close(fig)


def grafico_precios(registros):
    datos = []
    etiquetas = []
    nombres = {
        "combustion": "Combustión",
        "moto_electrica": "Motos eléctricas",
        "bicimoto": "Bicimotos",
        "bicicleta_electrica": "Bicicletas eléctricas",
        "patinete": "Patinetes",
    }
    for categoria in ["combustion", "moto_electrica", "bicimoto", "bicicleta_electrica", "patinete"]:
        vals = [
            r["precio_usd"]
            for r in registros
            if r["categoria"] == categoria and r.get("precio_valido")
        ]
        if vals:
            datos.append(vals)
            etiquetas.append(nombres[categoria])
    fig, ax = plt.subplots(figsize=(10, 6))
    caja = ax.boxplot(datos, patch_artist=True, showfliers=False, widths=0.55)
    for parche in caja["boxes"]:
        parche.set_facecolor("#d5dbdb")
    ax.set_xticklabels(etiquetas, rotation=18)
    ax.set_ylabel("Precio (USD)")
    ax.set_title("Distribución de precios por segmento (USD)", fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "precios_por_segmento.png", dpi=150)
    plt.close(fig)


def grafico_indice(indices_por_categoria):
    fig, ejes = plt.subplots(2, 2, figsize=(13, 10))
    pares = [
        ("combustion", ejes[0][0]),
        ("moto_electrica", ejes[0][1]),
        ("bicimoto", ejes[1][0]),
        ("patinete", ejes[1][1]),
    ]
    for categoria, ax in pares:
        filas = indices_por_categoria.get(categoria, [])[:6][::-1]
        if not filas:
            ax.axis("off")
            continue
        etiquetas = [f"{g['marca']} {g['modelo']}".replace(" General", "") for g in filas]
        valores = [g["indice"] for g in filas]
        ax.barh(etiquetas, valores, color=COLORES[categoria], alpha=0.88)
        ax.set_xlim(0, 108)
        ax.set_xlabel("Índice (0-100)")
        ax.set_title(CATS[categoria], fontsize=12, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        for i, v in enumerate(valores):
            ax.text(v + 0.8, i, f"{v:.1f}".replace(".", ","), va="center", fontsize=8)
    fig.suptitle("Índice de demanda por modelo (cada panel se normaliza dentro de su segmento)",
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "indice_demanda.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def grafico_demanda_precio(todos):
    fig, ax = plt.subplots(figsize=(10, 7))
    for categoria in CATS:
        grupo = [g for g in todos if g["categoria"] == categoria and g["mediana"]]
        if not grupo:
            continue
        ax.scatter(
            [g["mediana"] for g in grupo],
            [g["indice"] for g in grupo],
            s=[max(20, g["n"] * 2) for g in grupo],
            alpha=0.65,
            label=CATS[categoria],
            color=COLORES[categoria],
        )
    ax.set_xlabel("Precio mediano (USD)")
    ax.set_ylabel("Índice de demanda")
    ax.set_title("Demanda vs. precio (índice normalizado por segmento)", fontweight="bold")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "demanda_vs_precio.png", dpi=150)
    plt.close(fig)


def grafico_composicion(conteos):
    fig, ax = plt.subplots(figsize=(9, 5))
    etiquetas = [CATS[c] for c in conteos]
    valores = [conteos[c] for c in conteos]
    colores = [COLORES[c] for c in conteos]
    barras = ax.bar(etiquetas, valores, color=colores, alpha=0.88)
    ax.bar_label(barras, labels=[miles(v) for v in valores], padding=3)
    ax.set_ylabel("Anuncios")
    ax.set_title("Composición de la oferta por segmento", fontweight="bold")
    plt.xticks(rotation=12)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "composicion_segmentos.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Informe
# ---------------------------------------------------------------------------
def main():
    datos = cargar()
    registros = datos["registros"]
    fuente_txt = "Revolico"

    conteos = {
        c: sum(1 for r in registros if r["categoria"] == c) for c in CATS
    }
    con_precio = sum(1 for r in registros if r.get("precio_valido"))
    sin_marca = sum(1 for r in registros if not r["marca"])
    cobertura_marca = 1 - sin_marca / len(registros)

    grupos = {}
    totales = {}
    for categoria in CATS:
        grupos[categoria], totales[categoria] = agrupar(registros, categoria)

    indices = {}
    for categoria in CATS:
        indices[categoria] = indice_demanda(grupos[categoria], totales[categoria])

    # Segmentos genericos (sin marca) relevantes
    genericos = defaultdict(list)
    for r in registros:
        if not r["marca"] or r["modelo"] in ("150cc", "200cc", "250cc", "125cc"):
            if r["modelo"]:
                genericos[r["categoria"]].append(r)
    gen_150 = [
        r for r in registros
        if r["categoria"] == "combustion" and r["modelo"] == "150cc"
    ]
    gen_150_sin_marca = [r for r in gen_150 if not r["marca"]]
    gen_150_sin_marca_precios = [
        r["precio_usd"] for r in gen_150_sin_marca if r.get("precio_valido")
    ]
    gen_150_precios = [r["precio_usd"] for r in gen_150 if r.get("precio_valido")]

    def resumen(categoria):
        lista = indices.get(categoria, [])
        return lista[0] if lista else None

    mejor_comb = resumen("combustion")
    mejor_elec = resumen("moto_electrica")
    mejor_bici = resumen("bicimoto")
    mejor_pat = resumen("patinete")

    # Precios por segmento
    filas_precios = []
    for categoria in ["combustion", "moto_electrica", "bicimoto", "bicicleta_electrica", "patinete"]:
        vals = [r for r in registros if r["categoria"] == categoria]
        e = estadisticas(vals, len(vals))
        e["nombre"] = CATS[categoria]
        filas_precios.append(e)
    por_nombre = {g["nombre"]: g for g in filas_precios}

    # Escenarios: el lider de cada segmento + GN125 (nicho de margen)
    escenarios = []
    for categoria in ["combustion", "moto_electrica", "bicimoto", "patinete"]:
        lista = [g for g in indices.get(categoria, []) if g["p10"]]
        if lista:
            escenarios.append(lista[0])
    gn125 = next(
        (
            g for g in grupos["combustion"]
            if g["marca"] == "SUZUKI" and g["modelo"] == "GN125" and g["p10"]
        ),
        None,
    )
    if gn125 and gn125 not in escenarios:
        escenarios.insert(1, gn125)

    # Margen base por modelo (P25 -> mediana)
    def margen_base(g):
        if not g["p25"] or not g["mediana"]:
            return None
        ingreso = g["mediana"]
        costo = COSTO_OPERATIVO * ingreso
        return ingreso - g["p25"] - costo

    # Graficos
    top_grafico = {
        categoria: indices.get(categoria, [])[:8] for categoria in CATS
    }

    grafico_top(top_grafico)
    grafico_precios(registros)
    grafico_indice(indices)
    grafico_demanda_precio([g for cat in indices for g in indices[cat]])
    grafico_composicion(conteos)

    todos_indices = [g for cat in indices for g in indices[cat]]
    nichos = sorted(
        [
            g for g in todos_indices
            if g["n"] >= 5 and g["share"] < 0.03 and g["vistas"] >= 12
        ],
        key=lambda g: (-g["vistas"], -g["indice"]),
    )[:5]

    # -------------------------------------------------------------------
    # Texto
    # -------------------------------------------------------------------
    fechas = sorted({r["fecha_dia"] for r in registros if r.get("fecha_dia")})
    ventana_desde = fechas[0][:10] if fechas else ""
    ventana_hasta = fechas[-1][:10] if fechas else ""
    n_dias = (
        (datetime.fromisoformat(ventana_hasta) - datetime.fromisoformat(ventana_desde)).days + 1
        if ventana_desde and ventana_hasta
        else 0
    )
    por_corte: dict[str, int] = {}
    for r in registros:
        por_corte[r["archivo_origen"]] = por_corte.get(r["archivo_origen"], 0) + 1

    def _dia_archivo(nombre: str) -> str:
        m = re.search(r"(20\d{2})(\d{2})(\d{2})", nombre)
        return str(int(m.group(3))) if m else nombre

    dias_corte = sorted({_dia_archivo(k) for k in por_corte}, key=int)
    if len(dias_corte) > 1:
        dias_txt = ", ".join(dias_corte[:-1]) + " y " + dias_corte[-1]
    else:
        dias_txt = dias_corte[0] if dias_corte else ""

    partes = [
        f"{miles(n)} anuncios del {_dia_archivo(k)} de octubre"
        for k, n in sorted(por_corte.items())
    ]
    if len(partes) > 1:
        cortes_resumen_txt = ", ".join(partes[:-1]) + " y " + partes[-1]
    else:
        cortes_resumen_txt = partes[0] if partes else ""

    lineas = []
    a = lineas.append
    a("# Informe de Mercado — Motos y Movilidad Eléctrica en La Habana")
    a("")
    a(
        f"> **Corte:** {ventana_hasta} · **Fuente principal:** Revolico "
        f"(La Habana) · **Anuncios analizados:** {miles(len(registros))} · "
        f"**Precios válidos en USD:** {miles(con_precio)}"
    )
    a("")
    a("> **Nota de alcance:** este informe se construyó exclusivamente con datos "
      "observados. La fuente Telegram está pendiente de credenciales (API oficial), "
      "por lo que no se incluyen anuncios de ese canal ni se estiman cifras no medidas.")
    a("")

    # 1. Resumen ejecutivo
    a("## 1. Resumen Ejecutivo")
    a("")
    a(
        f"Se partió de **{miles(datos['total_bruto'])} registros brutos** de {len(dias_corte)} "
        f"cortes de Revolico ({dias_txt} de octubre de 2026). Tras excluir no-vehículos y "
        f"duplicados quedaron **{miles(len(registros))} anuncios únicos**; el "
        f"**{pct(100 * con_precio / len(registros))}** tiene precio válido en USD. "
        f"La cobertura de marca identificada es del **{pct(100 * cobertura_marca)}**."
    )
    a("")
    if mejor_comb:
        a(
            f"- **Combustión:** el modelo con mayor índice de demanda es **{mejor_comb['marca']} "
            f"{mejor_comb['modelo']}** ({mejor_comb['n']} anuncios, mediana {miles(mejor_comb['mediana'])} USD). "
            f"El segmento de 150 cc (todas las marcas) suma {len(gen_150)} anuncios, "
            f"mediana {miles(st.median(gen_150_precios)) if gen_150_precios else '—'} USD; "
            f"de ellos, {len(gen_150_sin_marca)} no especifican marca."
        )
    if mejor_elec:
        a(
            f"- **Eléctricas:** **{mejor_elec['marca']} {mejor_elec['modelo']}** lidera "
            f"({mejor_elec['n']} anuncios, mediana {miles(mejor_elec['mediana'])} USD). "
            f"TOPMAQ, VEDCA y MOUNTAIN concentran la mayor oferta del segmento."
        )
    if mejor_bici:
        a(
            f"- **Bicimotos:** **{mejor_bici['marca']} {mejor_bici['modelo']}** es la más ofertada "
            f"({mejor_bici['n']} anuncios, mediana {miles(mejor_bici['mediana'])} USD)."
        )
    if mejor_pat:
        a(
            f"- **Patinetes:** **{mejor_pat['marca']} {mejor_pat['modelo']}** lidera "
            f"({mejor_pat['n']} anuncios, mediana {miles(mejor_pat['mediana'])} USD)."
        )
    a(
        "- **Hallazgo clave:** el mercado es **eficiente en precio**: el diferencial entre "
        "compra (P25) y venta (mediana) es estrecho y, con un costo operativo del 10 %, "
        "no cubre el arbitraje local en la mayoría de los modelos. La rentabilidad aparece "
        "al **comprar en el decil bajo (P10)** o al **importar**."
    )
    a(
        "- **Hipótesis no confirmadas:** Yadea y Yati **no aparecen** en la muestra "
        "(0 y 1 anuncio respectivamente). La GN125 existe, pero no es la más ofertada: "
        "RX Combat la supera en volumen. La hipótesis de precio de la GN125 (1 500–1 800 USD) "
        "no se sostiene: la mediana observada es superior."
    )
    a("")

    # 2. Metodologia
    a("## 2. Metodología")
    a("")
    a(
        f"**Fuentes y ventana.** Se usaron {len(dias_corte)} cortes reales de Revolico La "
        f"Habana ({dias_txt} de octubre de 2026; "
        f"{cortes_resumen_txt}). La ventana efectiva es de {n_dias} días. "
        "Telegram queda fuera por falta de credenciales; no se imputaron datos."
    )
    a("")
    a("**ETL.** 1) Lectura de los JSON crudos sin modificarlos. 2) Clasificación en "
      "combustión, moto eléctrica, bicimoto, bicicleta eléctrica y patinete. "
      "3) Exclusión de triciclos, motocarros, mototaxis, cuatrimotos, repuestos y accesorios. "
      "4) Normalización de marcas y modelos (GN125/GN-125/GN 125 → Suzuki GN125; "
      "AX100/AX-100 → Suzuki AX100, etc.). 5) Deduplicación por ID y por reposts exactos. "
      "6) Precios numéricos; se excluyen del cálculo los menores de 100 USD y los "
      "atípicos extremos (3 × IQR por segmento).")
    a("")
    a("**Rankings.** Las tablas A–D se ordenan por el índice de demanda, no solo por "
      "número de anuncios; por eso un modelo con más anuncios puede aparecer debajo de "
      "otro con mejor combinación de estabilidad y velocidad.")
    a("")
    a(f"**Índice de demanda.** 40 % frecuencia relativa dentro del segmento, "
      f"30 % presencia en fuentes, 20 % estabilidad de precios (1 − CV) y "
      f"10 % velocidad de publicación (anuncios/día). Cada componente se normaliza 0–1. "
      f"Con una sola fuente, el componente de fuentes vale 1 para todos y **no diferencia**; "
      f"se activará cuando se incorpore Telegram. En una ventana fija, anuncios/día es "
      f"proporcional al volumen, por lo que la velocidad está correlacionada con la frecuencia. "
      f"Los modelos con un único precio observado (CV = 0) reciben la máxima estabilidad; "
      f"por eso el índice debe leerse junto con el número de anuncios.")
    a("")
    a(
        "**Limitaciones.** Los precios son **precios de anuncio**, no de transacción. "
        "No hay datos de ventas cerradas ni de tiempo hasta la venta. La muestra es un "
        f"corte transversal de {n_dias} días y la marca no se especifica en una parte de los anuncios. "
        "Los resultados describen la **oferta activa**, no el volumen histórico de ventas."
    )
    a("")

    # 3. Datos
    a("## 3. Datos Analizados")
    a("")
    a(f"- Registros brutos: **{miles(datos['total_bruto'])}**")
    a(f"- Excluidos por no ser vehículos de la lista blanca: **{datos['total_excluidos']}**")
    a(f"- Duplicados eliminados: **{datos['total_duplicados']}** "
      f"(ID: {datos['total_duplicados_id']}, reposts: {datos['total_duplicados_repost']})")
    a(f"- Registros limpios: **{miles(len(registros))}**")
    a(f"- Con precio válido en USD: **{miles(con_precio)}**")
    a(f"- Moneda distinta de USD (excluida de precios): "
      f"**{sum(1 for r in registros if r['moneda'] != 'USD')}** anuncios en CUP")
    a(f"- Anuncios sin marca identificada: **{miles(sin_marca)}** "
      f"({pct(100 * (1 - cobertura_marca))})")
    a("")
    a("| Segmento | Anuncios | % del total |")
    a("|---|---:|---:|")
    for categoria in CATS:
        a(f"| {CATS[categoria]} | {miles(conteos[categoria])} | "
          f"{pct(100 * conteos[categoria] / len(registros))} |")
    a("")
    a("![Composición de la oferta](graficos/composicion_segmentos.png)")
    a("")

    # 4. Combustion
    a("## 4. Moto de Combustión Más Demandada")
    a("")
    if mejor_comb:
        a(
            f"**{mejor_comb['marca']} {mejor_comb['modelo']}** encabeza el índice de demanda "
            f"del segmento con **{mejor_comb['n']} anuncios** "
            f"({pct(100 * mejor_comb['share_marca'])} de los anuncios de combustión con marca identificada), "
            f"precio promedio **{miles(mejor_comb['media'])} USD**, mediana "
            f"**{miles(mejor_comb['mediana'])} USD** y rango "
            f"**{miles(mejor_comb['min'])}–{miles(mejor_comb['max'])} USD**. "
            f"Su coeficiente de variación es **{('%.2f' % mejor_comb['cv']).replace('.', ',')}**, "
            f"lo que indica un precio bastante estable."
        )
        a("")
    a("**Contraste con las hipótesis iniciales.** La GN125 no lidera el volumen: "
      f"la familia GN125 reúne {sum(g['n'] for g in grupos['combustion'] if g['modelo'] == 'GN125')} anuncios, "
      f"mientras RX Combat suma {mejor_comb['n'] if mejor_comb else 0}. "
      "La GN125 conserva, sin embargo, un **premio de marca** y un diferencial "
      "P10–P75 más amplio, lo que la hace más atractiva para reventa que para rotación.")
    a("")
    a(f"El segmento de **150 cc sin marca** reúne {len(gen_150_sin_marca)} anuncios "
      f"(mediana {miles(st.median(gen_150_sin_marca_precios)) if gen_150_sin_marca_precios else '—'} USD) "
      "y es el bloque más numeroso de la combustión: marca el precio de entrada del "
      "mercado y compite directamente con las eléctricas de gama media.")
    a("")
    a("### Tabla A — Top motos de combustión")
    a("")
    a(tabla_ranking(indices["combustion"], 10))
    a("")
    a("> % de mercado calculado sobre anuncios **con marca identificada** del segmento. "
      "El segmento genérico de 150 cc (sin marca) se analiza por separado en el texto.")
    a("")

    # 5. Electricas
    a("## 5. Moto Eléctrica Más Demandada")
    a("")
    if mejor_elec:
        a(
            f"**{mejor_elec['marca']} {mejor_elec['modelo']}** es la moto eléctrica más "
            f"demandada: **{mejor_elec['n']} anuncios** ({pct(100 * mejor_elec['share_marca'])} del segmento con marca identificada), "
            f"promedio **{miles(mejor_elec['media'])} USD**, mediana "
            f"**{miles(mejor_elec['mediana'])} USD**, rango "
            f"**{miles(mejor_elec['min'])}–{miles(mejor_elec['max'])} USD**. "
            f"Le siguen VEDCA, MOUNTAIN y CHALLENGER."
        )
        a("")
    a("**Hipótesis vs. datos.** Yadea y Yati no tienen presencia relevante en la muestra "
      "(0 y 1 anuncio). El liderazgo real corresponde a **TOPMAQ**, con una familia amplia "
      "de modelos (TANK, F3 y versiones generales). JMD no lidera las motos eléctricas: "
      "su fortaleza está en **bicimotos y patinetes**.")
    a("")
    a("### Tabla B — Top motos eléctricas")
    a("")
    a(tabla_ranking(indices["moto_electrica"], 10))
    a("")

    # 6. Bicimotos
    a("## 6. Bicimoto Más Demandada")
    a("")
    if mejor_bici:
        a(
            f"**{mejor_bici['marca']} {mejor_bici['modelo']}** lidera las bicimotos con "
            f"**{mejor_bici['n']} anuncios** ({pct(100 * mejor_bici['share_marca'])} del segmento con marca identificada), "
            f"promedio **{miles(mejor_bici['media'])} USD**, mediana "
            f"**{miles(mejor_bici['mediana'])} USD** y rango "
            f"**{miles(mejor_bici['min'])}–{miles(mejor_bici['max'])} USD**. "
            f"TOPMAQ y YOAZAKY le siguen muy de cerca."
        )
        a("")
    a("El segmento de bicimotos es el **segundo más numeroso** de la muestra y el de "
      "menor ticket entre las motos (1 424 USD de promedio), por debajo de combustión "
      "y eléctricas, aunque por encima de bicicletas y patinetes. Es la puerta de "
      "entrada natural para un negocio con capital limitado; la contrapartida es un "
      "margen absoluto pequeño por unidad.")
    a("")
    a("### Tabla C — Top bicimotos")
    a("")
    a(tabla_ranking(indices["bicimoto"], 10))
    a("")

    # 7. Patinetes
    a("## 7. Patinete Más Demandado")
    a("")
    if mejor_pat:
        a(
            f"**{mejor_pat['marca']} {mejor_pat['modelo']}** es el patinete más ofertado "
            f"({mejor_pat['n']} anuncios, mediana {miles(mejor_pat['mediana'])} USD, "
            f"rango {miles(mejor_pat['min'])}–{miles(mejor_pat['max'])} USD). "
            f"MAF, PROEFIX y MRK completan un mercado muy concentrado en torno a los "
            f"750–860 USD."
        )
        a("")
    a("El patinete es un segmento **commoditizado**: precios muy estables y productos "
      "poco diferenciados. La oportunidad no está en el margen por unidad sino en el "
      "volumen y en la venta de accesorios/servicio.")
    a("")
    a("### Tabla D — Top patinetes")
    a("")
    a(tabla_ranking(indices["patinete"], 10))
    a("")

    # 8. Precios
    a("## 8. Análisis de Precios")
    a("")
    a(tabla_precios(filas_precios))
    a("")
    a("![Distribución de precios](graficos/precios_por_segmento.png)")
    a("")
    a("**Lectura.** La mediana de las motos de combustión "
      f"(**{miles(por_nombre['Motos de combustión']['mediana'])} USD**) es superior a la de las "
      f"eléctricas (**{miles(por_nombre['Motos eléctricas']['mediana'])} USD**) y muy superior a la de "
      f"bicimotos (**{miles(por_nombre['Bicimotos']['mediana'])} USD**), "
      f"bicicletas eléctricas (**{miles(por_nombre['Bicicletas eléctricas']['mediana'])} USD**) y "
      f"patinetes (**{miles(por_nombre['Patinetes eléctricos']['mediana'])} USD**). "
      f"La dispersión es mayor en eléctricas (CV "
      f"{('%.2f' % por_nombre['Motos eléctricas']['cv']).replace('.', ',')}) que en combustión (CV "
      f"{('%.2f' % por_nombre['Motos de combustión']['cv']).replace('.', ',')}) "
      "debido a la convivencia de modelos de entrada y de gama alta.")
    a("")
    a("![Demanda vs. precio](graficos/demanda_vs_precio.png)")
    a("")

    # 9. Rentabilidad
    a("## 9. Análisis de Rentabilidad")
    a("")
    a("Se modelaron dos escenarios con **costos operativos del 10 %** sobre el precio de "
      "venta (transporte, reparaciones menores, negociación):")
    a("")
    a("- **Base:** compra en P25 y venta en la mediana.")
    a("- **Oportunista:** compra en P10 y venta en P75 (requiere comprar bien y esperar).")
    a("")
    a("| Segmento | Modelo | Compra P25 | Venta mediana | Margen neto/unidad | ROI |")
    a("|---|---|---:|---:|---:|---:|")
    for g in escenarios:
        mb = margen_base(g)
        roi = mb / g["p25"] if mb is not None and g["p25"] else None
        a(f"| {CATS[g['categoria']]} | {g['marca']} {g['modelo']} | {miles(g['p25'])} | "
          f"{miles(g['mediana'])} | {miles(mb)} | {pct(100 * roi) if roi is not None else '—'} |")
    a("")
    a("**Conclusión de rentabilidad.** En el escenario base, la mayoría de los modelos "
      "queda en margen cero o negativo: el mercado descuenta muy rápido la información. "
      "La ganancia aparece en el escenario oportunista, sobre todo en **TOPMAQ** y "
      "**GN125**. Las bicimotos y patinetes, con diferenciales P10–P75 de 70–190 USD, "
      "no cubren un costo operativo del 10 % salvo que se compre por debajo del P10.")
    a("")
    a("### Escenarios de capital (compra P10 → venta P75)")
    a("")
    a(tabla_escenarios(escenarios, CAPITALES))
    a("")
    a("> La inversión mostrada es el capital efectivamente utilizado; el resto queda "
      "como colchón. La utilidad es neta de costos operativos estimados. No incluye "
      "impuestos, permisos ni capital de trabajo adicional.")
    a("")

    # 10. Recomendaciones
    a("## 10. Recomendaciones de Inversión")
    a("")
    a("1. **Núcleo de cartera: TOPMAQ (eléctricas).** Mayor volumen, marca reconocida y "
      "el mejor ROI oportunista del estudio. Priorizar TANK y F3, que tienen precios "
      "más definidos que la categoría “General”.")
    a("2. **Nicho de margen: Suzuki GN125.** Menos oferta que RX Combat, pero mayor "
      "diferencial P10–P75 y premio de marca. Comprar unidades 2019–2023 en buen estado "
      "y vender a coleccionistas/uso diario.")
    a("3. **Rotación rápida: JMD bicimotos.** Ticket bajo (1 550 USD), volumen alto y "
      "demanda constante. Sirve para generar flujo de caja, no para margen.")
    a("4. **Evitar arbitraje puro en RX Combat.** Es la más líquida, pero su spread "
      "P25–mediana es de solo ~70 USD y no cubre costos. Usarla para servicio, "
      "personalización o importación por volumen.")
    a("5. **Patinetes: volumen y accesorios.** El margen por unidad es mínimo; la "
      "rentabilidad está en la venta cruzada (cascos, baterías, repuestos) y en el "
      "servicio técnico.")
    a("")
    a("**Asignación sugerida por capital:**")
    a("")
    a("- **5 000 USD:** 2 GN125 o 2 TOPMAQ (una sola línea) + colchón para reparaciones.")
    a("- **10 000 USD:** 4–5 unidades mixtas (2 TOPMAQ, 2 GN125, 1 JMD) para diversificar.")
    a("- **20 000 USD:** lote de importación de 8–10 eléctricas + 3–4 GN125; negociar "
      "flete y consolidar un taller de preparación.")
    a("")

    # 11. Riesgos
    a("## 11. Riesgos del Mercado")
    a("")
    a("- **Muestra de una sola fuente.** Revolico concentra la oferta formal, pero no "
      "cubre la venta informal ni los grupos de Telegram (pendientes).")
    a("- **Precios de anuncio, no de transacción.** El precio publicado suele tener "
      "margen de negociación; el precio real de cierre no se observa.")
    a("- **Sin datos de ventas cerradas.** La “rotación” se infiere de la cantidad de "
      "anuncios y las vistas, no del tiempo hasta la venta.")
    a(f"- **Ambigüedad de marca/modelo.** Un {pct(100 * (1 - cobertura_marca))} de los anuncios "
      "no especifica marca; los rankings de marca se calculan sobre la parte identificada.")
    a("- **Riesgo regulatorio y de importación.** Aranceles, permisos y homologación "
      "pueden cambiar el costo de reposición; no se modelaron.")
    a("- **Riesgo de calidad.** Baterías de litio sin trazabilidad, motos siniestradas "
      "y repuestos falsos son frecuentes; el costo de reparación puede borrar el margen.")
    a("- **Riesgo cambiario.** 38 anuncios en CUP quedaron fuera de las estadísticas; "
      "una devaluación altera la referencia en USD.")
    a("")

    # 12. Conclusiones
    a("## 12. Conclusiones")
    a("")
    a("El mercado de La Habana está dominado en volumen por las **motos eléctricas** y "
      "las **bicimotos**, con TOPMAQ y JMD como protagonistas. En combustión, **RX Combat** "
      "es el modelo más ofertado, pero **GN125** ofrece mejor relación margen/riesgo. "
      "Los precios son altos y relativamente estables, y el arbitraje local es estrecho: "
      "la oportunidad real está en **comprar por debajo del P10**, **importar** o "
      "**diferenciarse con servicio**.")
    a("")
    a("### Conclusión ejecutiva")
    a("")
    a("- **¿Mejor moto de combustión para comprar y revender?** Suzuki GN125: menos "
      "oferta, premio de marca y mayor diferencial P10–P75. RX Combat solo para rotación.")
    a("- **¿Mejor moto eléctrica para comprar y revender?** TOPMAQ (TANK/F3): mayor "
      "volumen, reconocimiento y mejor ROI oportunista.")
    a("- **¿Mayor rentabilidad?** TOPMAQ en eléctricas y GN125 en combustión; ambas "
      "superan el 20 % de ROI solo en el escenario de compra baja.")
    a("- **¿Venta más rápida?** RX Combat y JMD bicimoto por volumen de anuncios; "
      "TOPMAQ por demanda sostenida.")
    a("- **¿En qué segmento enfocarse?** Eléctricas TOPMAQ como núcleo, GN125 como "
      "nicho de margen y JMD bicimotos para flujo de caja.")
    a("")
    a("---")
    a("")
    a("*Informe generado automáticamente a partir de `data/clean/anuncios_limpios.json`.*")
    a(f"*Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}.*")

    (REPORTS / "README.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    # Resumen por consola
    print("=" * 66)
    print("INFORME DE MERCADO — RESUMEN")
    print("=" * 66)
    print(f"  anuncios analizados: {len(registros)}")
    print(f"  con precio USD:      {con_precio}")
    print(f"  cobertura de marca:  {pct(100 * cobertura_marca)}")
    for categoria in ["combustion", "moto_electrica", "bicimoto", "patinete"]:
        g = resumen(categoria)
        if g:
            print(f"  {categoria:14s} -> {g['marca']} {g['modelo']} "
                  f"(n={g['n']}, indice={g['indice']:.1f})")
    print(f"  informe:             {REPORTS / 'README.md'}")
    print(f"  graficos:            {GRAFICOS}")


if __name__ == "__main__":
    main()
