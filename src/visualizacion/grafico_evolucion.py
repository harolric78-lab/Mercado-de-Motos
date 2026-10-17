#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grafico de evolucion 2024-2026 (por anio de modelo en el titulo).

Genera un SVG (sin dependencias externas) comparando la cantidad de anuncios
de motos ELECTRICAS frente a las de COMBUSTION segun el anio de modelo que
aparece en el titulo del anuncio de Revolico.

Fuente: el JSON de datos crudos mas reciente en `datos/revolico/`.

Uso:
    python grafico_evolucion.py
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATOS_DIR = REPO_ROOT / "datos" / "revolico"
GRAFICOS_DIR = REPO_ROOT / "graficos"

ANIOS = [2024, 2025, 2026]
ELECTRICAS = "motos_electricas"
COMBUSTION = "motos_combustion"

COLOR_ELECTRICAS = "#2E86DE"
COLOR_COMBUSTION = "#E67E22"
COLOR_EJE = "#555555"
COLOR_TEXTO = "#222222"


def json_mas_reciente():
    archivos = sorted(DATOS_DIR.glob("anuncios_revolico_*.json"))
    if not archivos:
        raise SystemExit("No hay archivos JSON en datos/revolico/")
    return archivos[-1]


def anio_modelo(titulo):
    for y in re.findall(r"\b(20[2-9]\d)\b", titulo or ""):
        return int(y)
    return None


def contar():
    datos = json.loads(json_mas_reciente().read_text(encoding="utf-8"))
    conteo = defaultdict(Counter)
    for a in datos["anuncios"]:
        t = (a.get("titulo") or "").lower()
        if re.search(r"triciclo|trimoto|tricimoto", t):
            continue
        y = anio_modelo(a.get("titulo"))
        if y in ANIOS:
            conteo[a["categoria_clave"]][y] += 1
    return conteo


def svg(conteo):
    ancho, alto = 760, 460
    izq, der, sup, inf = 90, 720, 80, 380
    ancho_plot = der - izq
    alto_plot = inf - sup

    valores = [conteo[ELECTRICAS][y] for y in ANIOS] + [
        conteo[COMBUSTION][y] for y in ANIOS
    ]
    y_max = max(valores) if valores else 1

    # Escala del eje Y redondeada hacia arriba (multiplo de 100)
    paso = 200 if y_max > 400 else 50
    y_max_eje = (int(y_max / paso) + 1) * paso

    def y(v):
        return inf - v / y_max_eje * alto_plot

    paso_grupo = ancho_plot / len(ANIOS)
    ancho_barra = 52
    separacion = 8

    partes = []
    partes.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
        f'viewBox="0 0 {ancho} {alto}" font-family="Segoe UI, Arial, sans-serif">'
    )
    partes.append(f'<rect width="{ancho}" height="{alto}" fill="#ffffff"/>')

    # Titulo
    partes.append(
        f'<text x="{ancho/2}" y="34" text-anchor="middle" font-size="20" '
        f'font-weight="bold" fill="{COLOR_TEXTO}">'
        f"Evolucion del mercado de motos 2024-2026 (La Habana)</text>"
    )
    partes.append(
        f'<text x="{ancho/2}" y="58" text-anchor="middle" font-size="13" '
        f'fill="#666">Anuncios en Revolico segun anio de modelo</text>'
    )

    # Ejes / lineas guia
    v = 0
    while v <= y_max_eje:
        yy = y(v)
        partes.append(
            f'<line x1="{izq}" y1="{yy:.1f}" x2="{der}" y2="{yy:.1f}" '
            f'stroke="#e5e5e5" stroke-width="1"/>'
        )
        partes.append(
            f'<text x="{izq-10}" y="{yy+4:.1f}" text-anchor="end" font-size="12" '
            f'fill="#777">{v}</text>'
        )
        v += paso

    # Ejes principales
    partes.append(
        f'<line x1="{izq}" y1="{inf}" x2="{der}" y2="{inf}" '
        f'stroke="{COLOR_EJE}" stroke-width="1.5"/>'
    )

    for i, anio in enumerate(ANIOS):
        centro = izq + paso_grupo * (i + 0.5)
        x_elec = centro - ancho_barra - separacion / 2
        x_comb = centro + separacion / 2

        for x, valor, color in (
            (x_elec, conteo[ELECTRICAS][anio], COLOR_ELECTRICAS),
            (x_comb, conteo[COMBUSTION][anio], COLOR_COMBUSTION),
        ):
            y_top = y(valor)
            altura = inf - y_top
            partes.append(
                f'<rect x="{x:.1f}" y="{y_top:.1f}" width="{ancho_barra}" '
                f'height="{max(altura,0):.1f}" fill="{color}" rx="3"/>'
            )
            partes.append(
                f'<text x="{x+ancho_barra/2:.1f}" y="{y_top-6:.1f}" '
                f'text-anchor="middle" font-size="12" font-weight="bold" '
                f'fill="{COLOR_TEXTO}">{valor}</text>'
            )

        # Anio bajo el grupo
        partes.append(
            f'<text x="{centro:.1f}" y="{inf+24}" text-anchor="middle" '
            f'font-size="15" font-weight="bold" fill="{COLOR_TEXTO}">{anio}</text>'
        )

    # Etiqueta eje X
    partes.append(
        f'<text x="{(izq+der)/2}" y="{inf+52}" text-anchor="middle" '
        f'font-size="13" fill="#666">Anio de modelo</text>'
    )

    # Leyenda
    lx, ly = izq, 20
    partes.append(f'<rect x="{lx}" y="{ly-11}" width="14" height="14" fill="{COLOR_ELECTRICAS}" rx="2"/>')
    partes.append(f'<text x="{lx+20}" y="{ly+1}" font-size="13" fill="{COLOR_TEXTO}">Motos electricas</text>')
    lx2 = lx + 170
    partes.append(f'<rect x="{lx2}" y="{ly-11}" width="14" height="14" fill="{COLOR_COMBUSTION}" rx="2"/>')
    partes.append(f'<text x="{lx2+20}" y="{ly+1}" font-size="13" fill="{COLOR_TEXTO}">Motos de combustion</text>')

    partes.append("</svg>")
    return "\n".join(partes)


def main():
    conteo = contar()
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = GRAFICOS_DIR / "evolucion_motos_2024_2026.svg"
    ruta.write_text(svg(conteo), encoding="utf-8")

    print("Anio | Electricas | Combustion")
    for anio in ANIOS:
        print(f"{anio} | {conteo[ELECTRICAS][anio]:>10} | {conteo[COMBUSTION][anio]:>10}")
    print(f"\nGrafico guardado en: {ruta}")


if __name__ == "__main__":
    main()
