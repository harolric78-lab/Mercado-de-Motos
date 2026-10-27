#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline completo de actualizacion de la base de datos de Revolico.

Ejecuta, en orden:

  1. Scrape   -> datos/raw/revolico_raw_<sello>.json|csv   (auditoria, sin limpiar)
  2. Limpieza-> datos/processed/revolico_processed_<sello>.json|csv
  3. Reemplazo del dataset del proyecto:
       datos/revolico/anuncios_revolico_<sello>.json|csv
       datos/limpios/revolico_limpio_<sello>.json|csv
     (los archivos anteriores se archivan en datos/_reemplazados/<sello>/)
  4. Analisis -> datos/processed/metricas_revolico_<sello>.json|csv
                 docs/informes/precios_categorias_<sello>.md
  5. Reportes y graficos del proyecto:
       src/analisis/precios_atipicos.py, src/analisis/top30_recientes.py,
       src/visualizacion/grafico_evolucion.py y el notebook notebooks/eda_motos.ipynb
  6. Log final en logs/revolico_<sello>.log con todos los contadores

Uso:
    python pipeline.py
    python pipeline.py --n 30 --delay 1.0 --max-paginas 3
    python pipeline.py --sin-reportes --sin-notebook
    python pipeline.py --proyecto "C:/ruta/Mercado-de-Motos"
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze as mod_analyze  # noqa: E402
import clean as mod_clean  # noqa: E402
import scrape as mod_scrape  # noqa: E402
from common import (  # noqa: E402
    Logger,
    ahora_habana,
    guardar_csv,
    guardar_json,
    paths,
    sello,
)


# ---------------------------------------------------------------------------
# 3. Reemplazo del dataset que usa el proyecto
# ---------------------------------------------------------------------------
def archivar_viejos(carpeta, destino, log, etiqueta):
    """Mueve los archivos anteriores a la carpeta de archivo."""
    destino.mkdir(parents=True, exist_ok=True)
    movidos = []
    for f in sorted(carpeta.glob("*")):
        if f.is_file() and f.suffix in (".csv", ".json", ".md"):
            destino.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(destino / f.name))
            movidos.append(f.name)
    if movidos:
        log.log(f"  {etiqueta}: {len(movidos)} archivo(s) anterior(es) archivados en {destino}")
    else:
        log.log(f"  {etiqueta}: no habia archivos anteriores que reemplazar")
    return movidos


def escribir_dataset_proyecto(p, registros, log, est):
    """
    Escribe los dos archivos que consume el resto del proyecto, con el mismo
    formato que usan los scripts existentes:
      - datos/revolico/anuncios_revolico_<sello>.json  {"anuncios": [...]}
      - datos/limpios/revolico_limpio_<sello>.json     {"registros": [...]}
    """
    p["datos_revolico"].mkdir(parents=True, exist_ok=True)
    p["datos_limpios"].mkdir(parents=True, exist_ok=True)

    anuncios = []
    for r in registros:
        anuncios.append(
            {
                "id": r["id"],
                "categoria": ETIQUETA_CATEGORIA[r["categoria"]],
                "categoria_clave": r["categoria_clave"],
                "titulo": r["titulo"],
                "precio": r["precio"],
                "moneda": r["moneda"],
                "es_electrica": r["es_electrica"],
                "url": r["url"],
                "fecha_utc": r["fecha_utc"],
                "fecha_habana": r["fecha_habana"],
                "imagenes": r["imagenes"],
                "vistas": r["vistas"],
                "promocionado": r["promocionado"],
                "descripcion": r["descripcion"],
                "ubicacion": r["ubicacion"],
                "categoria_detectada": r["categoria"],
            }
        )
    ruta_json_raw = guardar_json(
        p["datos_revolico"] / f"anuncios_revolico_{est}.json",
        {
            "fuente": "Revolico",
            "provincia": "La Habana",
            "categorias": sorted({a["categoria"] for a in anuncios}),
            "generado_habana": ahora_habana().isoformat(),
            "total": len(anuncios),
            "anuncios": anuncios,
        },
    )
    ruta_csv_raw = guardar_csv(
        p["datos_revolico"] / f"anuncios_revolico_{est}.csv",
        anuncios,
        list(anuncios[0].keys()) if anuncios else [],
    )

    ruta_json_limpio = guardar_json(
        p["datos_limpios"] / f"revolico_limpio_{est}.json",
        {
            "origen": ruta_json_raw.name,
            "generado_habana": ahora_habana().isoformat(),
            "total": len(registros),
            "total_precio_valido": sum(1 for r in registros if r["precio_valido"]),
            "registros": registros,
        },
    )
    ruta_csv_limpio = guardar_csv(
        p["datos_limpios"] / f"revolico_limpio_{est}.csv",
        registros,
        list(registros[0].keys()) if registros else [],
    )
    log.log(f"  Dataset del proyecto actualizado:")
    log.log(f"    - {ruta_json_raw}")
    log.log(f"    - {ruta_csv_raw}")
    log.log(f"    - {ruta_json_limpio}")
    log.log(f"    - {ruta_csv_limpio}")
    return [ruta_json_raw, ruta_csv_raw, ruta_json_limpio, ruta_csv_limpio]


ETIQUETA_CATEGORIA = {
    "combustion": "Motos de Combustion",
    "electrica": "Motos Electricas",
    "patinete": "Patinetes Electricos",
}


# ---------------------------------------------------------------------------
# 5. Reportes y graficos del proyecto
# ---------------------------------------------------------------------------
def ejecutar_script(ruta, cwd, log):
    if not ruta.exists():
        log.log(f"  [aviso] no existe {ruta}, se omite")
        return False
    try:
        proc = subprocess.run(
            [sys.executable, str(ruta)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
    except Exception as exc:
        log.log(f"  [error] ejecutando {ruta.name}: {exc}")
        return False
    if proc.returncode != 0:
        log.log(f"  [error] {ruta.name} termino con codigo {proc.returncode}")
        if proc.stderr:
            log.log("    " + proc.stderr.strip()[:800])
        return False
    log.log(f"  OK {ruta.name}")
    return True


def ejecutar_notebook(ruta, cwd, log):
    """Ejecuta las celdas de codigo del notebook para regenerar los graficos."""
    if not ruta.exists():
        log.log(f"  [aviso] no existe {ruta}, se omite")
        return False
    try:
        nb = json.loads(ruta.read_text(encoding="utf-8"))
    except Exception as exc:
        log.log(f"  [error] no se pudo leer el notebook: {exc}")
        return False
    try:
        import matplotlib
        matplotlib.use("Agg")
    except Exception:
        pass
    import os

    anterior = Path.cwd()
    ns = {"__name__": "__notebook__"}
    try:
        os.chdir(str(cwd))
        for i, celda in enumerate(nb.get("cells", [])):
            if celda.get("cell_type") != "code":
                continue
            fuente = "".join(celda.get("source", []))
            fuente = "\n".join(
                linea for linea in fuente.splitlines() if not linea.strip().startswith(("%", "!"))
            )
            exec(compile(fuente, f"<celda {i}>", "exec"), ns)  # noqa: S102
    except BaseException as exc:
        log.log(f"  [error] fallo al ejecutar el notebook: {exc}")
        return False
    finally:
        os.chdir(str(anterior))
    log.log(f"  OK notebook {ruta.name}")
    return True


def regenerar_reportes(p, log, con_notebook=True):
    log.log("5) Regenerando reportes y graficos del proyecto...")
    root = p["root"]
    mod_analyze_paths = [
        p["src_analisis"] / "precios_atipicos.py",
        p["src_analisis"] / "top30_recientes.py",
    ]
    for s in mod_analyze_paths:
        ejecutar_script(s, root, log)
    ejecutar_script(p["src_visualizacion"] / "grafico_evolucion.py", root, log)
    if con_notebook:
        ejecutar_notebook(p["notebooks"] / "eda_motos.ipynb", p["notebooks"], log)


# ---------------------------------------------------------------------------
# 6. Actualizacion del README
# ---------------------------------------------------------------------------
def _tabla_marcas(registros):
    """Filas de la tabla de marcas mas demandadas por subtipo."""
    from collections import Counter

    grupos = [
        ("Moto de combustión", lambda r: r["categoria"] == "combustion"),
        ("Moto eléctrica", lambda r: r.get("subtipo") == "moto_electrica"),
        ("Bicicleta eléctrica", lambda r: r.get("subtipo") == "bicicleta_electrica"),
        ("Patinete eléctrico", lambda r: r["categoria"] == "patinete"),
    ]
    filas = []
    for nombre, cond in grupos:
        items = [r for r in registros if cond(r)]
        if not items:
            continue
        marcas = Counter(r["marca"] for r in items if r.get("marca") not in ("", "SIN_MARCA"))
        marca = marcas.most_common(1)[0][0] if marcas else "—"
        precios = [r["precio"] for r in items if r.get("precio_valido")]
        if precios:
            lo, hi = min(precios), max(precios)
            if lo == hi:
                rango = f"{lo:,.0f}".replace(",", " ")
            else:
                rango = f"{lo:,.0f} – {hi:,.0f}".replace(",", " ")
        else:
            rango = "—"
        url = items[0].get("url", "")
        filas.append(f"| {nombre} | {marca} | {rango} | {len(items)} | [ver]({url}) |")
    return filas


def actualizar_readme(p, registros, log):
    readme = p["root"] / "README.md"
    if not readme.exists():
        return
    try:
        texto = readme.read_text(encoding="utf-8")
    except Exception:
        return
    import re as _re

    original = texto
    conteo = len(registros)
    por_categoria = {}
    for r in registros:
        por_categoria[r["categoria"]] = por_categoria.get(r["categoria"], 0) + 1
    n_comb = por_categoria.get("combustion", 0)
    n_elec = por_categoria.get("electrica", 0)
    n_pat = por_categoria.get("patinete", 0)

    texto = texto.replace("6 466", str(conteo))
    texto = texto.replace("6466", str(conteo))
    texto = texto.replace(
        "Anuncios clasificados de La Habana (últimos 7 días)",
        f"Anuncios clasificados de La Habana ({conteo} más recientes)",
    )
    texto = _re.sub(
        r"Datos de \*\*\d[\d\s]*anuncios\*\* publicados en Revolico \(La Habana(?:, [^)]*)?\)\.",
        f"Datos de los **{conteo} anuncios más recientes** publicados en Revolico (La Habana).",
        texto,
        count=1,
    )

    # Frase resumen de la fuente
    linea = (
        f"> **Revolico** (única fuente con datos actualmente): {conteo} anuncios — "
        f"{n_comb} de combustión, {n_elec} eléctricos (incluye bicicletas) "
        f"y {n_pat} patinetes."
    )
    texto = _re.sub(r"^> \*\*Revolico\*\*.*$", linea, texto, count=1, flags=_re.M)

    # Tabla de marcas mas demandadas
    filas = _tabla_marcas(registros)
    if filas:
        tabla = (
            "| Categoría | Marca más demandada | Rango de precio (USD) | Anuncios | Enlace Revolico |\n"
            "|-----------|---------------------|----------------------:|---------:|-----------------|\n"
            + "\n".join(filas)
        )
        texto = _re.sub(
            r"\| Categoría \| Marca más demandada \|.*?(?=\n\n)",
            tabla,
            texto,
            count=1,
            flags=_re.S,
        )
        texto = _re.sub(r"(\|[^\n]*\|)\n{3,}(### )", r"\1\n\n\2", texto)

    # Frase de evolucion: sin cifras que queden obsoletas
    texto = _re.sub(
        r"Anuncios en Revolico \(La Habana\) según el \*\*año de modelo\*\*[^\n]*",
        "Anuncios en Revolico (La Habana) según el **año de modelo** indicado en el título. "
        "El gráfico compara la cantidad de anuncios de motos eléctricas frente a las de combustión.",
        texto,
        count=1,
    )

    if texto != original:
        readme.write_text(texto, encoding="utf-8")
        log.log(f"  README actualizado (total de anuncios: {conteo}, por categoria: {por_categoria})")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Pipeline completo de Revolico")
    ap.add_argument("--n", type=int, default=30, help="Anuncios validos a obtener")
    ap.add_argument("--extra", type=int, default=15, help="Anuncios extra para cubrir descartes de limpieza")
    ap.add_argument("--max-paginas", type=int, default=3)
    ap.add_argument("--max-candidatos", type=int, default=160)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--precio-minimo", type=float, default=mod_clean.PRECIO_MINIMO_DEFECTO)
    ap.add_argument("--proyecto", default=None)
    ap.add_argument("--sin-imagenes", action="store_true")
    ap.add_argument("--sin-reemplazo", action="store_true", help="No tocar datos/ del proyecto")
    ap.add_argument("--sin-reportes", action="store_true", help="No regenerar informes y graficos")
    ap.add_argument("--sin-notebook", action="store_true", help="No ejecutar el notebook EDA")
    ap.add_argument("--sin-readme", action="store_true", help="No actualizar el README")
    args = ap.parse_args()

    p = paths(Path(args.proyecto) if args.proyecto else None)
    est = sello()
    log = Logger(p["logs"] / f"revolico_{est}.log")
    log.log("=" * 70)
    log.log(f"PIPELINE DE REVOLICO - {ahora_habana().isoformat()}")
    log.log(f"Proyecto: {p['root']}")
    log.log("=" * 70)

    # --- 1. scraping ---
    import requests

    session = requests.Session()
    seleccionados, descartados, errores = mod_scrape.scrape(
        session,
        args.n + args.extra,
        args.max_paginas,
        args.delay,
        log,
        con_imagenes=not args.sin_imagenes,
        max_candidatos=args.max_candidatos,
    )
    encontrados = len(seleccionados) + len(descartados)
    log.contar("anuncios_consultados", encontrados)
    log.contar("anuncios_validos", len(seleccionados))
    log.contar("anuncios_descartados", len(descartados))
    for cat in ("combustion", "electrica", "patinete"):
        log.contar(
            f"validos_{cat}",
            sum(1 for a in seleccionados if a.get("_scraping", {}).get("categoria") == cat),
        )
    log.contar("errores", len(errores))
    for e in errores:
        log.log(f"  ERROR: {e.get('id')} -> {e.get('error')}")

    ruta_json_raw, ruta_csv_raw = mod_scrape.guardar_raw(
        p["raw"],
        seleccionados,
        descartados,
        errores,
        {"sello": est, "params": vars(args)},
    )
    log.log("")
    log.log(f"1) Dato crudo -> {ruta_json_raw}")
    log.log(f"                {ruta_csv_raw}")

    # --- 2. limpieza ---
    registros, descartes_limpieza = mod_clean.limpiar(
        seleccionados, args.precio_minimo, args.n
    )
    for d in descartes_limpieza:
        log.contar(f"descartados_{d['motivo']}")
        log.log(f"  [descartado:{d['motivo']}] {d['titulo'][:60]}")
    ruta_json_proc, ruta_csv_proc = mod_clean.guardar_processed(
        p["processed"], registros, descartes_limpieza, ruta_json_raw, args.n
    )
    log.log("")
    log.log(f"2) Dato procesado -> {ruta_json_proc}")
    log.log(f"                   {ruta_csv_proc}")

    # --- 3. reemplazo del dataset del proyecto ---
    log.log("")
    if args.sin_reemplazo:
        log.log("3) Reemplazo del dataset OMITIDO (--sin-reemplazo)")
    else:
        log.log("3) Reemplazando el dataset del proyecto...")
        destino = p["archivo"] / est
        archivar_viejos(p["datos_revolico"], destino / "revolico", log, "datos/revolico")
        archivar_viejos(p["datos_limpios"], destino / "limpios", log, "datos/limpios")
        escribir_dataset_proyecto(p, registros, log, est)
        log.contar("anuncios_reemplazados", len(registros))

    # --- 4. metricas ---
    log.log("")
    metricas_ = mod_analyze.analizar(registros)
    p["processed"].mkdir(parents=True, exist_ok=True)
    ruta_json_metricas = guardar_json(
        p["processed"] / f"metricas_revolico_{est}.json",
        {
            "generado_habana": ahora_habana().isoformat(),
            "origen": ruta_json_proc.name,
            "metricas": metricas_,
        },
    )
    filas = mod_analyze.filas_metricas(metricas_)
    ruta_csv_metricas = guardar_csv(
        p["processed"] / f"metricas_revolico_{est}.csv", filas, list(filas[0].keys())
    )
    p["informes"].mkdir(parents=True, exist_ok=True)
    ruta_md = p["informes"] / f"precios_categorias_{est}.md"
    ruta_md.write_text(
        mod_analyze.informe_markdown(metricas_, registros, ruta_json_proc.name),
        encoding="utf-8",
    )
    log.log("4) Metricas de precios por categoria:")
    for cat in list(mod_analyze.CATEGORIAS) + ["total"]:
        m = metricas_[cat]
        log.log(
            f"   {mod_analyze.ETIQUETAS.get(cat,'Total'):<24} n={m['anuncios']:<4} "
            f"min={m['precio_min']} max={m['precio_max']} prom={m['precio_promedio']} "
            f"med={m['mediana']} desv={m['desviacion_estandar']}"
        )
    log.log(f"   {ruta_json_metricas}")
    log.log(f"   {ruta_csv_metricas}")
    log.log(f"   {ruta_md}")

    # --- 5. reportes y graficos ---
    log.log("")
    if args.sin_reportes:
        log.log("5) Reportes OMITIDOS (--sin-reportes)")
    else:
        regenerar_reportes(p, log, con_notebook=not args.sin_notebook)

    # --- 6. README ---
    if not args.sin_readme and not args.sin_reemplazo:
        actualizar_readme(p, registros, log)

    # --- resumen final ---
    log.log("")
    log.log("=" * 70)
    log.log("RESUMEN DE LA EJECUCION")
    log.log("=" * 70)
    log.log(f"Fecha y hora de ejecucion (La Habana): {ahora_habana().isoformat()}")
    log.log(f"Anuncios consultados: {log.contadores.get('anuncios_consultados', 0)}")
    log.log(f"Anuncios validos: {log.contadores.get('anuncios_validos', 0)}")
    log.log(f"Anuncios descartados: {log.contadores.get('anuncios_descartados', 0)}")
    log.log(f"Descartados en limpieza/ranking: {len(descartes_limpieza)}")
    log.log(f"Anuncios reemplazados en el proyecto: {log.contadores.get('anuncios_reemplazados', 0)}")
    log.log(f"Errores encontrados: {log.contadores.get('errores', 0)}")
    log.log("")
    log.log("Validos por categoria:")
    for cat in ("combustion", "electrica", "patinete"):
        log.log(f"  {cat}: {log.contadores.get(f'validos_{cat}', 0)}")
    log.log("-" * 70)
    for k in sorted(log.contadores):
        log.log(f"  {k}: {log.contadores[k]}")
    log.log("=" * 70)
    log.cerrar()

    print("\nPipeline completado.")
    print(f"  Log: {p['logs'] / f'revolico_{est}.log'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
