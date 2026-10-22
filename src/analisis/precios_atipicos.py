#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deteccion de precios anormalmente altos (outliers) en el mercado de motos
=========================================================================

Toma los datos LIMPIOS de Revolico (La Habana) y detecta anuncios con precios
fuera de lo normal dentro de su propio grupo, usando dos metodos:

    1. Regla del rango intercuartilico (IQR / Tukey):
           atipico si  precio > Q3 + 1.5 * IQR   (o < Q1 - 1.5 * IQR)
    2. Puntaje Z (Z-score):
           atipico si  |precio - media| / desviacion_tipica > 3

El grupo es la CATEGORIA (motos electricas / motos de combustion) y, dentro de
ella, el TIPO de vehiculo.

Genera un informe Markdown y un CSV en `docs/informes/`.

Uso:
    python precios_atipicos.py
    python precios_atipicos.py --umbral-z 2.5 --factor-iqr 3
"""

import argparse
import csv
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ_HABANA = ZoneInfo("America/Havana")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATOS_LIMPIOS = REPO_ROOT / "datos" / "limpios"
DATOS_CRUDOS = REPO_ROOT / "datos" / "revolico"
INFORMES = REPO_ROOT / "docs" / "informes"

# Etiquetas amigables por tipo de vehiculo
ETIQUETAS = {
    "combustion": "Motos de combustion",
    "combustion_scooter": "Scooters de combustion",
    "combustion_deportiva": "Motos deportivas de combustion",
    "moto_electrica": "Motos electricas",
    "bicicleta_electrica": "Bicicletas electricas",
    "bicimoto_electrica": "Bicimotos electricas",
    "patinete_electrico": "Patinetes electricos",
    "electrico_sin_clasificar": "Electricas sin clasificar",
}


def cargar_registros():
    """Carga la ultima limpieza (o limpia al vuelo si no existe)."""
    limpios = sorted(DATOS_LIMPIOS.glob("revolico_limpio_*.json"))
    if limpios:
        datos = json.loads(limpios[-1].read_text(encoding="utf-8"))
        return datos["registros"], limpios[-1].name

    # Fallback: limpiar los crudos con el modulo de limpieza
    import sys
    sys.path.insert(0, str(REPO_ROOT / "src" / "limpieza_datos"))
    import limpiar_revolico as lr
    crudo = sorted(DATOS_CRUDOS.glob("anuncios_revolico_*.json"))[-1]
    datos = json.loads(crudo.read_text(encoding="utf-8"))
    return lr.limpiar(datos["anuncios"]), crudo.name


def grupos_de(registros):
    """Agrupa por (categoria, tipo_vehiculo) los registros con precio valido."""
    grupos = defaultdict(list)
    for r in registros:
        if not r.get("precio_valido"):
            continue
        clave = (r.get("categoria", ""), r.get("tipo_vehiculo", ""))
        grupos[clave].append(r)
    return grupos


def detectar(lista, factor_iqr, umbral_z):
    """Detecta atipicos en una lista de precios. Devuelve (outliers, stats)."""
    precios = [float(r["precio"]) for r in lista]
    if len(precios) < 4:  # muy pocos datos para estadistica robusta
        return [], None

    q1, q3 = statistics.quantiles(precios, n=4)[0], statistics.quantiles(precios, n=4)[2]
    iqr = q3 - q1
    limite_sup = q3 + factor_iqr * iqr
    limite_inf = q1 - factor_iqr * iqr

    media = statistics.mean(precios)
    desv = statistics.stdev(precios) if len(precios) > 1 else 0.0

    stats = {
        "n": len(precios),
        "min": min(precios),
        "mediana": statistics.median(precios),
        "media": media,
        "max": max(precios),
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "limite_sup": limite_sup,
        "limite_inf": limite_inf,
        "desv": desv,
    }

    outliers = []
    for r in lista:
        p = float(r["precio"])
        z = ((p - media) / desv) if desv else 0.0
        por_iqr = p > limite_sup or p < limite_inf
        por_z = abs(z) > umbral_z
        if por_iqr or por_z:
            r = dict(r)
            r["z_score"] = round(z, 2)
            r["por_iqr"] = por_iqr
            r["por_z"] = por_z
            outliers.append(r)

    outliers.sort(key=lambda x: x["precio"], reverse=True)
    return outliers, stats


def escapar(t):
    return (t or "").replace("|", "\\|")


def main():
    parser = argparse.ArgumentParser(description="Deteccion de precios atipicos")
    parser.add_argument("--factor-iqr", type=float, default=1.5,
                        help="Factor del rango intercuartilico (por defecto 1.5)")
    parser.add_argument("--umbral-z", type=float, default=3.0,
                        help="Umbral absoluto del puntaje Z (por defecto 3.0)")
    args = parser.parse_args()

    registros, origen = cargar_registros()
    grupos = grupos_de(registros)
    ahora = datetime.now(TZ_HABANA)

    lineas = [
        "# Precios anormalmente altos (outliers) - Revolico, La Habana",
        "",
        f"- **Datos de origen:** `{origen}`",
        f"- **Generado (La Habana):** {ahora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Metodos:** IQR (factor {args.factor_iqr}) y Z-score (umbral {args.umbral_z})",
        "",
    ]

    resumen = []
    filas_csv = []

    lineas.append("## Resumen por grupo")
    lineas.append("")
    lineas.append("| Grupo | Anuncios con precio | Mediana | Límite IQR (sup.) | Atípicos |")
    lineas.append("|-------|--------------------:|--------:|------------------:|---------:|")

    for (categoria, tipo), lista in sorted(grupos.items(), key=lambda kv: len(kv[1]), reverse=True):
        outliers, stats = detectar(lista, args.factor_iqr, args.umbral_z)
        if not stats:
            continue
        etiqueta = ETIQUETAS.get(tipo, tipo)
        lineas.append(
            f"| {escapar(etiqueta)} | {stats['n']} | {stats['mediana']:.0f} | "
            f"{stats['limite_sup']:.0f} | {len(outliers)} |"
        )
        resumen.append((etiqueta, stats, outliers))
        for o in outliers:
            filas_csv.append(
                {
                    "categoria": categoria,
                    "tipo_vehiculo": tipo,
                    "grupo": etiqueta,
                    "marca": o.get("marca", ""),
                    "titulo": o.get("titulo", ""),
                    "precio": o.get("precio"),
                    "mediana_grupo": round(stats["mediana"]),
                    "limite_iqr": round(stats["limite_sup"]),
                    "z_score": o.get("z_score"),
                    "por_iqr": o.get("por_iqr"),
                    "por_z": o.get("por_z"),
                    "url": o.get("url", ""),
                }
            )
    lineas.append("")

    # Detalle de los atipicos mas extremos
    lineas.append("## Atípicos más extremos (por encima del límite)")
    lineas.append("")
    lineas.append("| Grupo | Marca | Título | Precio (USD) | Mediana del grupo | Z-score | Enlace |")
    lineas.append("|-------|-------|--------|-------------:|------------------:|--------:|--------|")
    todos = sorted(filas_csv, key=lambda x: float(x["precio"]), reverse=True)
    for o in todos[:40]:
        lineas.append(
            f"| {escapar(o['grupo'])} | {escapar(o['marca'])} | {escapar(o['titulo'])[:60]} | "
            f"{o['precio']} | {o['mediana_grupo']} | {o['z_score']} | [ver]({o['url']}) |"
        )
    lineas.append("")

    INFORMES.mkdir(parents=True, exist_ok=True)
    sello = ahora.strftime("%Y%m%d_%H%M")
    ruta_md = INFORMES / f"precios_atipicos_{sello}.md"
    ruta_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    ruta_csv = INFORMES / f"precios_atipicos_{sello}.csv"
    if filas_csv:
        with ruta_csv.open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas_csv[0].keys()))
            w.writeheader()
            w.writerows(filas_csv)
    else:
        ruta_csv = None

    # Resumen en consola
    print("\n".join(lineas))
    print(f"\nTotal de atipicos detectados: {len(filas_csv)}")
    print(f"Informe guardado en: {ruta_md}")
    if ruta_csv:
        print(f"CSV guardado en: {ruta_csv}")


if __name__ == "__main__":
    main()
