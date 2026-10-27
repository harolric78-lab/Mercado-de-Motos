#!/usr/bin/env python3
"""Scraper del catalogo oficial de VEDCA (vedca.cu).

Extrae el catalogo de productos de Vehiculos Electricos del Caribe (VEDCA),
descarga las fichas tecnicas de cada producto y aplica la lista blanca del
proyecto: solo motos electricas, bicicletas electricas y patinetes
electricos. Triciclos, cuatriciclos, juguetes y repuestos quedan unicamente
en data/raw como evidencia cruda.

Salidas (sello AAAAMMDD_HHMMSS):
  data/raw/vedca_raw_<sello>.json|csv
  data/processed/vedca_processed_<sello>.json|csv
  datos/importadora_vedca/vedca_catalogo_<sello>.json|csv
  docs/informes/vedca_catalogo_<sello>.md
  logs/vedca_<sello>.log

Reglas:
  - Nunca guarda telefonos, correos ni otros datos de contacto.
  - No inventa precios: VEDCA no publica precios en su pagina.
  - Respeta la pausa entre peticiones (--delay, 1 s por defecto).

Uso:
  python src/scraping/vedca.py [--proyecto RUTA] [--delay 1.0] [--sin-fichas]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contactos import sanear_contactos  # noqa: E402

BASE = "http://www.vedca.cu/"
UA = {"User-Agent": "Mercado-de-Motos-ICD/1.0 (scraping educativo)"}

CATEGORIA_CLAVE = {
    "combustion": "motos_combustion",
    "electrica": "motos_electricas",
    "patinete": "motos_electricas",
}

MOTIVO_EXCLUSION = {
    "filter-tri": "triciclo_fuera_de_lista_blanca",
    "filter-cuat": "cuatriciclo_fuera_de_lista_blanca",
    "filter-jug": "juguete_fuera_de_lista_blanca",
    "filter-ppa": "repuesto_fuera_de_lista_blanca",
}


def log(lineas: list[str], texto: str) -> None:
    print(texto)
    lineas.append(texto)


def obtener(session: requests.Session, url: str, reintentos: int = 2) -> str:
    ultimo = None
    for intento in range(reintentos + 1):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            if "charset" not in r.headers.get("content-type", ""):
                r.encoding = "utf-8"
            return r.text
        except Exception as exc:  # noqa: BLE001
            ultimo = exc
            if intento < reintentos:
                time.sleep(2)
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def limpiar(texto: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", texto)).strip()


def parsear_catalogo(html: str) -> list[dict]:
    """Devuelve los productos del portafolio de la pagina principal."""
    items = []
    bloques = re.findall(
        r"portfolio-item\s+(filter-\w+)[^>]*>(.*?)<!--\s*portfolio-item end\s*-->",
        html,
        re.S,
    )
    for filtro, bloque in bloques:
        img = re.search(r'<img src="([^"]+)"', bloque)
        ficha = re.search(r'<a href="([^"]+\.html)"\s+class="link-details"', bloque)
        disp = re.search(
            r"<h4>\s*Disponible en:\s*</h4>\s*<span>([^<]*)</span>", bloque, re.S
        )
        items.append(
            {
                "filtro": filtro,
                "imagen": img.group(1) if img else "",
                "ficha_relativa": ficha.group(1) if ficha else "",
                "tienda": limpiar(disp.group(1)) if disp else "",
            }
        )
    return items


def parsear_ficha(html: str) -> dict:
    """Extrae titulo, lista de datos, descripcion y tablas de la ficha."""
    info = re.search(r'<div class="portfolio-info">(.*?)</div>', html, re.S)
    titulo = ""
    datos: dict[str, str] = {}
    if info:
        h3 = re.search(r"<h3>(.*?)</h3>", info.group(1), re.S)
        titulo = limpiar(h3.group(1)) if h3 else ""
        for clave, valor in re.findall(
            r"<li><strong>([^<]+)</strong>:\s*(.*?)</li>", info.group(1), re.S
        ):
            datos[limpiar(clave)] = limpiar(valor)

    pdf = ""
    en_pdf = re.search(r'href="(assets/fichatecnica/[^"]+)"', html)
    if en_pdf:
        pdf = en_pdf.group(1)

    descripcion = ""
    desc = re.search(r'<div class="portfolio-description">(.*?)</div>', html, re.S)
    if desc:
        p = re.search(r"<p>(.*?)</p>", desc.group(1), re.S)
        if p:
            descripcion = limpiar(p.group(1))

    especificaciones: dict[str, list[str]] = {}
    for tabla in re.findall(r'<table class="table table-striped">(.*?)</table>', html, re.S):
        for fila in re.findall(r"<tr>(.*?)</tr>", tabla, re.S):
            celdas = [limpiar(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", fila, re.S)]
            celdas = [c for c in celdas if c]
            if len(celdas) >= 2 and celdas[0].lower() not in ("caracteristica",):
                especificaciones.setdefault(celdas[0], [])
                for valor in celdas[1:]:
                    if valor not in especificaciones[celdas[0]]:
                        especificaciones[celdas[0]].append(valor)

    return {
        "titulo": sanear_contactos(titulo),
        "datos": datos,
        "pdf": pdf,
        "descripcion": sanear_contactos(descripcion),
        "especificaciones": especificaciones,
    }


def modelo_desde_imagen(imagen: str) -> str:
    stem = Path(imagen).stem
    m = re.search(r"(\d{3,4})", stem)
    return m.group(1) if m else stem.upper()


def clasificar(filtro: str, imagen: str, titulo_ficha: str) -> tuple[str, str, str, str]:
    """Devuelve (categoria, tipo_vehiculo, motivo_exclusion, nombre_producto).

    La taxonomia propia del sitio (clase ``filter-*``) tiene prioridad; el
    titulo de la ficha y el nombre de la imagen solo se usan como respaldo.
    """
    stem = Path(imagen).stem.lower()
    titulo = (titulo_ficha or "").lower()

    if stem.startswith("pat-") or "patinet" in titulo:
        return "patinete", "patinete_electrico", "", "Patinete Eléctrico"
    if filtro in MOTIVO_EXCLUSION:
        return "", "", MOTIVO_EXCLUSION[filtro], ""
    if filtro == "filter-moto" or stem.startswith("moto-") or "moto" in titulo:
        return "electrica", "moto_electrica", "", "Moto Eléctrica"
    if filtro == "filter-bici" or stem.startswith("bici-") or "bicicleta" in titulo:
        return "electrica", "bicicleta_electrica", "", "Bicicleta Eléctrica"

    return "", "", "fuera_de_lista_blanca", ""


def numero(texto: str, patron: str) -> float | None:
    m = re.search(patron, texto or "", re.I)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", "."))
    except ValueError:
        return None


def enriquecer(registro: dict, ficha: dict) -> None:
    espec = ficha.get("especificaciones", {})
    registro["autonomia"] = " / ".join(espec.get("Autonomía", [])) or None
    registro["velocidad_maxima_kmh"] = numero(
        " ".join(espec.get("Velocidad máxima", [])), r"([\d.,]+)\s*km"
    )
    registro["peso_kg"] = numero(" ".join(espec.get("Peso neto", [])), r"([\d.,]+)")

    bateria = " ".join(espec.get("Batería", []))
    registro["bateria"] = bateria or None
    registro["voltaje"] = numero(bateria, r"(\d+)\s*V")
    registro["capacidad_ah"] = numero(bateria, r"(\d+(?:\.\d+)?)\s*Ah")

    potencia = " ".join(espec.get("Potencia de Motor", espec.get("Potencia", [])))
    registro["watts"] = numero(potencia, r"(\d+)\s*W")
    registro["tipo_bateria"] = " / ".join(espec.get("Tipo de batería", [])) or None
    registro["dimension"] = " / ".join(espec.get("Dimensión", [])) or None


def escribir_csv(ruta: Path, registros: list[dict], campos: list[str]) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        for reg in registros:
            fila = dict(reg)
            for k, v in list(fila.items()):
                if isinstance(v, (dict, list)):
                    fila[k] = json.dumps(v, ensure_ascii=False)
            writer.writerow(fila)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scraper del catalogo VEDCA")
    parser.add_argument("--proyecto", default="Mercado-de-Motos", help="Ruta del proyecto")
    parser.add_argument("--delay", type=float, default=1.0, help="Pausa entre peticiones")
    parser.add_argument("--sin-fichas", action="store_true", help="No descargar fichas tecnicas")
    args = parser.parse_args()

    raiz = Path(args.proyecto).resolve()
    sello = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    ahora = datetime.now().astimezone().isoformat(timespec="seconds")

    lineas: list[str] = []
    log(lineas, "=" * 70)
    log(lineas, f"CATALOGO VEDCA - {ahora}")
    log(lineas, f"Proyecto: {raiz}")
    log(lineas, "=" * 70)

    session = requests.Session()
    session.headers.update(UA)

    log(lineas, "1) Leyendo catalogo de la pagina principal...")
    html_index = obtener(session, BASE)
    catalogo = parsear_catalogo(html_index)
    log(lineas, f"   Productos en el portafolio: {len(catalogo)}")

    registros_raw: list[dict] = []
    incluidos: list[dict] = []
    errores: list[str] = []
    fichas_descargadas = 0

    for i, item in enumerate(catalogo, 1):
        url_ficha = BASE + item["ficha_relativa"] if item["ficha_relativa"] else ""
        ficha = None
        if url_ficha and not args.sin_fichas:
            try:
                ficha = parsear_ficha(obtener(session, url_ficha))
                fichas_descargadas += 1
                log(lineas, f"   [{i:02d}] ficha OK: {ficha['titulo'] or item['imagen']}")
            except Exception as exc:  # noqa: BLE001
                errores.append(f"{url_ficha}: {exc}")
                log(lineas, f"   [{i:02d}] ficha ERROR: {exc}")
            time.sleep(args.delay)

        titulo_ficha = ficha["titulo"] if ficha else ""
        categoria, tipo_vehiculo, motivo, nombre = clasificar(
            item["filtro"], item["imagen"], titulo_ficha
        )
        incluido = not motivo

        modelo = ""
        if ficha:
            modelo = re.sub(r"\s+", "", ficha["datos"].get("Modelo", ""))
        if not modelo and incluido:
            modelo = modelo_desde_imagen(item["imagen"])

        registro = {
            "filtro": item["filtro"],
            "imagen": item["imagen"],
            "ficha_relativa": item["ficha_relativa"],
            "url": url_ficha,
            "tienda": item["tienda"],
            "titulo_ficha": titulo_ficha,
            "categoria": categoria,
            "tipo_vehiculo": tipo_vehiculo,
            "incluido": incluido,
            "motivo_exclusion": motivo,
            "ficha": ficha,
        }
        registros_raw.append(registro)

        if not incluido:
            continue

        nombre_producto = titulo_ficha or nombre
        if modelo and modelo.upper() not in nombre_producto.upper():
            nombre_producto = f"{nombre_producto} {modelo}".strip()

        reg = {
            "id": f"vedca-{Path(item['imagen']).stem}",
            "fuente": "vedca.cu",
            "titulo": nombre_producto,
            "titulo_normalizado": nombre_producto.upper(),
            "marca": "VEDCA",
            "modelo": modelo or None,
            "categoria": categoria,
            "categoria_clave": CATEGORIA_CLAVE[categoria],
            "tipo_vehiculo": tipo_vehiculo,
            "subtipo": tipo_vehiculo,
            "es_electrica": True,
            "precio": None,
            "precio_valido": False,
            "moneda": "",
            "sin_precio": True,
            "anio_modelo": None,
            "cc": None,
            "watts": None,
            "voltaje": None,
            "autonomia": None,
            "velocidad_maxima_kmh": None,
            "bateria": None,
            "capacidad_ah": None,
            "tipo_bateria": None,
            "peso_kg": None,
            "dimension": None,
            "color": (ficha or {}).get("datos", {}).get("Color disponible") or None,
            "descripcion": (ficha or {}).get("descripcion", ""),
            "especificaciones": (ficha or {}).get("especificaciones", {}),
            "pdf": (ficha or {}).get("pdf", ""),
            "tienda": item["tienda"] or None,
            "provincia": "La Habana",
            "municipio": "Boyeros",
            "url": url_ficha,
            "imagen": BASE + item["imagen"],
            "fecha_captura": ahora,
            "es_outlier": False,
            "outlier_metodo": "",
            "outlier_zscore": None,
        }
        if ficha:
            enriquecer(reg, ficha)
        incluidos.append(reg)

    # Guardar salidas -------------------------------------------------------
    raw_dir = raiz / "data" / "raw"
    proc_dir = raiz / "data" / "processed"
    dataset_dir = raiz / "datos" / "importadora_vedca"
    informes_dir = raiz / "docs" / "informes"
    logs_dir = raiz / "logs"
    for d in (raw_dir, proc_dir, dataset_dir, informes_dir, logs_dir):
        d.mkdir(parents=True, exist_ok=True)

    resumen_raw = {
        "fuente": "vedca.cu",
        "url": BASE,
        "generado_habana": ahora,
        "params": {"delay": args.delay, "fichas": not args.sin_fichas},
        "total_consultados": len(registros_raw),
        "total_incluidos": len(incluidos),
        "total_descartados": len(registros_raw) - len(incluidos),
        "errores": errores,
        "productos": registros_raw,
    }
    raw_json = raw_dir / f"vedca_raw_{sello}.json"
    raw_json.write_text(json.dumps(resumen_raw, ensure_ascii=False, indent=2), encoding="utf-8")
    escribir_csv(
        raw_dir / f"vedca_raw_{sello}.csv",
        [
            {
                **{k: v for k, v in p.items() if k != "ficha"},
                "titulo_ficha": p["titulo_ficha"],
            }
            for p in registros_raw
        ],
        [
            "filtro",
            "imagen",
            "ficha_relativa",
            "url",
            "tienda",
            "titulo_ficha",
            "categoria",
            "tipo_vehiculo",
            "incluido",
            "motivo_exclusion",
        ],
    )

    resumen_proc = {
        "origen": raw_json.name,
        "generado_habana": ahora,
        "total": len(incluidos),
        "total_precio_valido": 0,
        "total_sin_precio": len(incluidos),
        "descartes": [
            {"imagen": p["imagen"], "motivo": p["motivo_exclusion"]}
            for p in registros_raw
            if not p["incluido"]
        ],
        "registros": incluidos,
    }
    proc_json = proc_dir / f"vedca_processed_{sello}.json"
    proc_json.write_text(
        json.dumps(resumen_proc, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    campos = list(incluidos[0].keys()) if incluidos else []
    escribir_csv(proc_dir / f"vedca_processed_{sello}.csv", incluidos, campos)

    dataset = {"registros": incluidos, "generado_habana": ahora, "origen": proc_json.name}
    (dataset_dir / f"vedca_catalogo_{sello}.json").write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    escribir_csv(dataset_dir / f"vedca_catalogo_{sello}.csv", incluidos, campos)

    # Informe ---------------------------------------------------------------
    por_categoria: dict[str, int] = {}
    for reg in incluidos:
        por_categoria[reg["categoria"]] = por_categoria.get(reg["categoria"], 0) + 1
    excluidos = [p for p in registros_raw if not p["incluido"]]

    md = [
        "# Catalogo oficial de VEDCA (vedca.cu)",
        "",
        f"- **Generado (La Habana):** {ahora}",
        f"- **Origen de los datos:** {proc_json.name}",
        f"- **Productos en el catalogo:** {len(registros_raw)}",
        f"- **Productos incluidos (lista blanca):** {len(incluidos)}",
        f"- **Productos excluidos:** {len(excluidos)}",
        "",
        "## Productos por categoria",
        "",
        "| Categoria | Productos |",
        "|---|---:|",
    ]
    for cat in ("combustion", "electrica", "patinete"):
        if por_categoria.get(cat):
            md.append(f"| {cat} | {por_categoria[cat]} |")
    md += [
        "",
        "## Productos incluidos",
        "",
        "| Producto | Categoria | Modelo | Autonomia | Vel. max (km/h) | Bateria | Disponibilidad |",
        "|---|---|---|---|---:|---|---|",
    ]
    for reg in sorted(incluidos, key=lambda r: (r["categoria"], r["titulo"])):
        md.append(
            "| {titulo} | {categoria} | {modelo} | {aut} | {vel} | {bat} | {tienda} |".format(
                titulo=reg["titulo"],
                categoria=reg["categoria"],
                modelo=reg["modelo"] or "-",
                aut=reg["autonomia"] or "-",
                vel=reg["velocidad_maxima_kmh"] if reg["velocidad_maxima_kmh"] is not None else "-",
                bat=reg["bateria"] or "-",
                tienda=reg["tienda"] or "VEDCA (fábrica)",
            )
        )
    md += [
        "",
        "## Notas",
        "",
        "- VEDCA **no publica precios** en su pagina: la venta se realiza a traves",
        "  de tiendas online (Islagrande, Supermarket23, Katapulk) o en fabrica.",
        "- Los precios de estos modelos se obtienen de dichas tiendas y se",
        "  contrastan con los anuncios de Revolico en el analisis.",
        "- Los productos fuera de la lista blanca (triciclos, cuatriciclos,",
        "  juguetes y repuestos) solo se conservan en `data/raw/` como evidencia.",
        "",
    ]
    informe = informes_dir / f"vedca_catalogo_{sello}.md"
    informe.write_text("\n".join(md), encoding="utf-8")

    log(lineas, f"2) Dato crudo    -> {raw_json}")
    log(lineas, f"3) Procesado     -> {proc_json}")
    log(lineas, f"4) Dataset       -> {dataset_dir / ('vedca_catalogo_' + sello + '.json')}")
    log(lineas, f"5) Informe       -> {informe}")
    log(lineas, "")
    log(lineas, "Por categoria (incluidos): " + json.dumps(por_categoria, ensure_ascii=False))
    log(lineas, f"Excluidos (solo raw): {len(excluidos)}")
    log(lineas, f"Errores de ficha: {len(errores)}")
    log(lineas, "=" * 70)

    (logs_dir / f"vedca_{sello}.log").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
