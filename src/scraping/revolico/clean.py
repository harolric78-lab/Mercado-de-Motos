#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 2 del pipeline: limpieza y transformacion de los datos de Revolico.

Toma el dato crudo mas reciente de `data/raw/` (o `--archivo`) y trabaja
unicamente con los anuncios incluidos en las tres categorias permitidas.

  1. Elimina duplicados (por ID y por URL).
  2. Normaliza titulos (emojis, caracteres especiales, espacios).
  3. Convierte precios a numero y detecta la moneda.
  4. Valida URLs, IDs y categorias.
  5. Elimina registros incompletos (sin titulo, sin precio, sin URL o sin ID).
  6. Marca precios atipicos (IQR de Tukey y Z-score) dentro de cada categoria.
  7. Se queda con los N anuncios mas recientes.

Salida:
  - data/processed/revolico_processed_<sello>.json / .csv

Uso:
    python clean.py
    python clean.py --archivo data/raw/revolico_raw_20261022_101500.json
    python clean.py --precio-minimo 100 --max-registros 30
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    TZ_HABANA,
    Logger,
    ahora_habana,
    categoria_legacy,
    detecta_marca,
    detecta_moneda,
    extraer_anio,
    extraer_cc,
    extraer_voltaje,
    extraer_watts,
    guardar_csv,
    guardar_json,
    normalizar_titulo,
    parse_precio,
    paths,
    sello,
    subtipo_vehiculo,
    tipo_vehiculo_legacy,
    url_valida,
)

PRECIO_MINIMO_DEFECTO = 100


def limpiar(anuncios, precio_minimo=PRECIO_MINIMO_DEFECTO, max_registros=30):
    """Devuelve (registros_limpios, descartes)."""
    registros, descartes = [], []
    vistos_id, vistos_url = set(), set()

    for ad in anuncios:
        sc = ad.get("_scraping", {}) or {}
        incluido = sc.get("incluido", not sc.get("descartado", False))
        if not incluido:
            continue

        ad_id = str(sc.get("id") or ad.get("id", "") or "")
        titulo = normalizar_titulo(sc.get("titulo_original") or ad.get("title", ""))
        descripcion = (sc.get("descripcion") or ad.get("description") or "").strip()
        precio_crudo = sc.get("precio_original")
        if precio_crudo is None:
            precio_crudo = ad.get("price")
        moneda_cruda = sc.get("moneda_original") or ad.get("currency", "")
        url = sc.get("url") or ad.get("url", "")
        fecha = sc.get("fecha_publicacion") or ad.get("updatedOnToOrder", "") or ""
        categoria = sc.get("categoria") or ""

        # --- duplicados ---
        if ad_id and ad_id in vistos_id:
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "duplicado"})
            continue
        if url and url in vistos_url:
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "duplicado"})
            continue

        # --- validaciones / registros incompletos ---
        if not ad_id:
            descartes.append({"id": "", "url": url, "titulo": titulo, "motivo": "sin_id"})
            continue
        if not titulo:
            descartes.append({"id": ad_id, "url": url, "titulo": "", "motivo": "sin_titulo"})
            continue
        if not url_valida(url):
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "url_invalida"})
            continue
        if categoria not in ("combustion", "electrica", "patinete"):
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "fuera_de_categorias"})
            continue
        precio = parse_precio(precio_crudo)
        if precio is None:
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "precio_ausente"})
            continue
        if precio < precio_minimo:
            descartes.append({"id": ad_id, "url": url, "titulo": titulo, "motivo": "precio_invalido"})
            continue

        vistos_id.add(ad_id)
        vistos_url.add(url)
        precio_valido = True
        moneda, moneda_por_titulo = detecta_moneda(moneda_cruda, titulo)

        fecha_utc, fecha_habana = fecha, ""
        try:
            dt = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            fecha_utc = dt.isoformat()
            fecha_habana = dt.astimezone(TZ_HABANA).isoformat()
        except Exception:
            pass

        registros.append(
            {
                "id": ad_id,
                "titulo": titulo,
                "titulo_normalizado": titulo.upper(),
                "precio": precio,
                "precio_valido": precio_valido,
                "moneda": moneda,
                "moneda_detectada_en_titulo": moneda_por_titulo,
                "categoria": categoria,
                "categoria_clave": categoria_legacy(categoria),
                "tipo_vehiculo": tipo_vehiculo_legacy(categoria, titulo),
                "subtipo": subtipo_vehiculo(categoria, titulo),
                "marca": detecta_marca(titulo) or "SIN_MARCA",
                "anio_modelo": extraer_anio(titulo),
                "cc": extraer_cc(titulo),
                "watts": extraer_watts(titulo),
                "voltaje": extraer_voltaje(titulo),
                "es_electrica": categoria in ("electrica", "patinete"),
                "ubicacion": sc.get("ubicacion", ""),
                "provincia": sc.get("provincia", ""),
                "municipio": sc.get("municipio", ""),
                "descripcion": descripcion,
                "descripcion_vacia": not bool(descripcion),
                "url": url,
                "fecha_publicacion": fecha,
                "fecha_utc": fecha_utc,
                "fecha_habana": fecha_habana,
                "imagenes": ad.get("imagesCount", 0),
                "vistas": ad.get("viewCount", 0),
                "promocionado": bool(ad.get("isPromoted", False)),
                "es_outlier": False,
                "outlier_metodo": "",
                "outlier_zscore": None,
            }
        )

    marcar_atipicos(registros)

    registros.sort(key=lambda r: r.get("fecha_publicacion") or "", reverse=True)
    if max_registros and len(registros) > max_registros:
        for r in registros[max_registros:]:
            descartes.append(
                {"id": r["id"], "url": r["url"], "titulo": r["titulo"], "motivo": "fuera_del_ranking"}
            )
        registros = registros[:max_registros]
    return registros, descartes


def marcar_atipicos(registros, factor_iqr=1.5, umbral_z=3.0):
    """Marca precios atipicos dentro de cada categoria (IQR de Tukey / Z-score)."""
    grupos = {}
    for r in registros:
        if not r.get("precio_valido"):
            continue
        grupos.setdefault(r["categoria"], []).append(r)
    for lista in grupos.values():
        precios = [float(r["precio"]) for r in lista]
        if len(precios) < 4:
            continue
        q1, q3 = statistics.quantiles(precios, n=4)[0], statistics.quantiles(precios, n=4)[2]
        iqr = q3 - q1
        limite_sup = q3 + factor_iqr * iqr
        limite_inf = q1 - factor_iqr * iqr
        media = statistics.mean(precios)
        desv = statistics.stdev(precios) if len(precios) > 1 else 0.0
        for r in lista:
            p = float(r["precio"])
            z = ((p - media) / desv) if desv else 0.0
            por_iqr = p > limite_sup or p < limite_inf
            por_z = abs(z) > umbral_z
            r["outlier_zscore"] = round(z, 3)
            if por_iqr or por_z:
                r["es_outlier"] = True
                r["outlier_metodo"] = "+".join(
                    m for m, ok in (("IQR", por_iqr), ("Z", por_z)) if ok
                )


def guardar_processed(carpeta, registros, descartes, origen, max_registros=30):
    carpeta.mkdir(parents=True, exist_ok=True)
    est = sello()
    meta = {
        "origen": Path(origen).name if origen else "",
        "generado_habana": ahora_habana().isoformat(),
        "total": len(registros),
        "total_precio_valido": sum(1 for r in registros if r.get("precio_valido")),
        "total_atipicos": sum(1 for r in registros if r.get("es_outlier")),
        "descartes": descartes,
        "registros": registros,
    }
    ruta_json = guardar_json(carpeta / f"revolico_processed_{est}.json", meta)
    columnas = [
        "id", "titulo", "precio", "precio_valido", "moneda", "categoria",
        "categoria_clave", "tipo_vehiculo", "subtipo", "marca", "anio_modelo",
        "cc", "watts", "voltaje", "es_electrica", "ubicacion", "provincia",
        "municipio", "url", "fecha_publicacion", "fecha_utc", "fecha_habana",
        "imagenes", "vistas", "promocionado", "es_outlier", "outlier_metodo",
        "outlier_zscore", "descripcion",
    ]
    ruta_csv = guardar_csv(carpeta / f"revolico_processed_{est}.csv", registros, columnas)
    return ruta_json, ruta_csv


def json_mas_reciente(carpeta):
    archivos = sorted(carpeta.glob("revolico_raw_*.json"))
    if not archivos:
        raise SystemExit(f"No hay datos crudos en {carpeta}")
    return archivos[-1]


def main():
    ap = argparse.ArgumentParser(description="Limpieza de datos de Revolico")
    ap.add_argument("--archivo", default=None, help="JSON crudo de entrada")
    ap.add_argument("--proyecto", default=None, help="Ruta raiz del proyecto")
    ap.add_argument("--entrada", default=None, help="Carpeta de datos crudos (data/raw)")
    ap.add_argument("--salida", default=None, help="Carpeta de salida (data/processed)")
    ap.add_argument("--precio-minimo", type=float, default=PRECIO_MINIMO_DEFECTO)
    ap.add_argument("--max-registros", type=int, default=30)
    args = ap.parse_args()

    p = paths(Path(args.proyecto) if args.proyecto else None)
    entrada = Path(args.entrada) if args.entrada else p["raw"]
    salida = Path(args.salida) if args.salida else p["processed"]
    origen = Path(args.archivo) if args.archivo else json_mas_reciente(entrada)

    log = Logger(p["logs"] / f"revolico_{sello()}.log")
    log(f"=== Limpieza de datos de Revolico - {ahora_habana().isoformat()} ===")
    log(f"Origen: {origen}")

    datos = json.loads(origen.read_text(encoding="utf-8"))
    anuncios = datos.get("anuncios", [])
    log(f"Anuncios consultados en el crudo: {len(anuncios)}")

    registros, descartes = limpiar(anuncios, args.precio_minimo, args.max_registros)
    log.contar("anuncios_validos", len(registros))
    log.contar("anuncios_descartados_limpieza", len(descartes))
    for d in descartes:
        log.contar(f"descartados_{d['motivo']}")
        log.log(f"  [descartado:{d['motivo']}] {d['titulo'][:60]}")

    ruta_json, ruta_csv = guardar_processed(salida, registros, descartes, origen, args.max_registros)
    log.log(f"Datos procesados guardados en:\n  - {ruta_json}\n  - {ruta_csv}")
    log.cerrar()
    print(f"\nOK  registros={len(registros)}  descartados={len(descartes)}")
    print(f"    {ruta_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
