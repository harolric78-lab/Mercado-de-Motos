#!/usr/bin/env python3
"""Scraper de precios de Islagrande (islagrande.com), tienda online de VEDCA.

Extrae los precios en USD de motos y bicicletas electricas y de combustion,
y deja los triciclos y repuestos unicamente en data/raw como evidencia cruda.

Fuentes consultadas:
  - categoria electricos (2 paginas)
  - categoria combustion
  - categoria triciclos (solo raw, excluidos)
  - enlaces del sitemap y portada que apunten a vehiculos no listados

Salidas (sello AAAAMMDD_HHMMSS):
  data/raw/islagrande_raw_<sello>.json|csv
  data/processed/islagrande_processed_<sello>.json|csv
  datos/tiendas_online/islagrande/islagrande_<sello>.json|csv
  docs/informes/islagrande_precios_<sello>.md
  logs/islagrande_<sello>.log

Reglas:
  - Lista blanca: solo `combustion`, `electrica` y `patinete`.
  - Triciclos, repuestos y accesorios: excluidos (solo raw).
  - Nunca guarda telefonos, correos ni datos de contacto.
  - No inventa precios: si el producto no tiene precio publicado se marca
    `sin_precio`.
  - Cambia la moneda de la tienda a USD antes de leer los precios.

Uso:
  python src/scraping/islagrande.py [--proyecto RUTA] [--delay 1.0]
"""

from __future__ import annotations

import argparse
import base64
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

BASE = "https://islagrande.com"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

CATEGORIAS = {
    "electricos": "/vehiculos-electricos/motos-y-bicicletas-electricas.html",
    "combustion": "/automotriz/motores-combustion.html",
    "triciclos": "/vehiculos-electricos/triciclos.html",
}

CATEGORIA_CLAVE = {
    "combustion": "motos_combustion",
    "electrica": "motos_electricas",
    "patinete": "motos_electricas",
}

REPUESTO_PATRON = (
    r"^\s*(tire|r13\b|llanta|neum[aá]tic|espejo|accesori|repuesto|charger|"
    r"battery with charger|bater[ií]a con cargador)"
)

TRICICLO_PATRON = r"triciclo|tricycle"
PATINETE_PATRON = r"patinet|scooter"
BICI_PATRON = r"bicycle|\bbike\b|bicicleta|\bbici\b"
MOTO_PATRON = r"motorcycle|moto"
CC_PATRON = r"(\d{2,3})\s*cc\b"


def log(lineas: list[str], texto: str) -> None:
    print(texto)
    lineas.append(texto)


def obtener(session: requests.Session, url: str, referer: str | None = None,
            reintentos: int = 2) -> str:
    ultimo = None
    for intento in range(reintentos + 1):
        try:
            r = session.get(url, timeout=30, headers={"Referer": referer} if referer else None)
            r.raise_for_status()
            if "charset" not in r.headers.get("content-type", ""):
                r.encoding = "utf-8"
            return r.text
        except Exception as exc:  # noqa: BLE001
            ultimo = exc
            if intento < reintentos:
                time.sleep(2)
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def cambiar_a_usd(session: requests.Session, categoria_url: str) -> bool:
    """Activa la moneda USD de la tienda (Magento currency switch)."""
    uenc = (
        base64.urlsafe_b64encode(categoria_url.encode())
        .decode()
        .rstrip("=")
        .replace("=", "~")
    )
    url = f"{BASE}/directory/currency/switch/currency/USD/uenc/{uenc}"
    try:
        r = session.get(url, headers={"Referer": categoria_url}, timeout=30)
        r.raise_for_status()
        if "charset" not in r.headers.get("content-type", ""):
            r.encoding = "utf-8"
        return "USD" in r.text
    except Exception:  # noqa: BLE001
        return False


def parsear_precios(texto: str) -> list[tuple[str, float, str]]:
    """Devuelve pares (tipo, monto, etiqueta) de los bloques de precio."""
    out: list[tuple[str, float, str]] = []
    for m in re.finditer(r'<span[^>]*data-price-amount="([\d.]+)"[^>]*>', texto):
        monto = float(m.group(1))
        tm = re.search(r'data-price-type="(\w+)"', m.group(0))
        tipo = tm.group(1) if tm else ""
        resto = texto[m.end(): m.end() + 400]
        pm = re.search(r'<span class="price">([^<]+)</span>', resto)
        etiqueta = pm.group(1).replace("\xa0", " ").strip() if pm else ""
        out.append((tipo, monto, etiqueta))
    return out


def parsear_tiles(html: str, origen: str) -> list[dict]:
    """Extrae las tarjetas de producto de una pagina de categoria."""
    items = []
    bloques = re.findall(
        r'class="item product[^"]*product-item[^"]*"(.*?)</li>', html, re.S
    )
    for bloque in bloques:
        nombre = re.search(r'class="product-item-link"[^>]*>\s*([^<]+?)\s*<', bloque)
        href = re.search(
            r'<a href="(https://islagrande\.com/[^"]+\.html)"\s+class="product photo', bloque
        ) or re.search(r'class="product-item-link"[^>]*href="([^"]+)"', bloque)
        sku = re.search(r'data-product-sku="([^"]+)"', bloque)
        precios: dict[str, tuple[float, str]] = {}
        for tipo, monto, etiqueta in parsear_precios(bloque):
            if tipo and tipo not in precios:
                precios[tipo] = (monto, etiqueta)
        descuento = re.search(r'class="discount-percent">([^<]+)</span>', bloque)
        if not nombre or not href:
            continue
        final = precios.get("finalPrice")
        viejo = precios.get("oldPrice")
        if viejo and viejo[0] < 100:
            viejo = None
        items.append(
            {
                "nombre": nombre.group(1).strip(),
                "url": href.group(1),
                "sku": sku.group(1) if sku else "",
                "precio_final": final[0] if final else None,
                "precio_anterior": viejo[0] if viejo else None,
                "etiqueta": final[1] if final else "",
                "descuento": descuento.group(1).strip() if descuento else "",
                "origen_categoria": origen,
            }
        )
    return items


def paginas_de_categoria(session: requests.Session, ruta: str, origen: str,
                         lineas: list[str], delay: float) -> list[dict]:
    """Recorre todas las paginas de una categoria (p=1..N hasta vaciar)."""
    items: list[dict] = []
    pagina = 1
    while pagina <= 20:
        url = BASE + ruta + (f"?p={pagina}" if pagina > 1 else "")
        html = obtener(session, url, referer=BASE + "/")
        nuevos = parsear_tiles(html, origen)
        log(lineas, f"   {origen} p{pagina}: {len(nuevos)} producto(s)")
        if not nuevos:
            break
        items.extend(nuevos)
        if not re.search(r"[?&]p=" + str(pagina + 1), html):
            break
        pagina += 1
        time.sleep(delay)
    return items


def parsear_ficha(session: requests.Session, url: str, lineas: list[str],
                  delay: float) -> dict:
    """Lee una ficha de producto: nombre, precio USD y especificaciones."""
    html = obtener(session, url, referer=BASE + "/")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    nombre = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else ""

    precio = None
    precio_anterior = None
    moneda = ""
    etiqueta = ""
    for tipo, monto, texto in parsear_precios(html):
        if tipo == "finalPrice" and precio is None:
            precio, etiqueta = monto, texto
        elif tipo == "oldPrice" and precio_anterior is None and monto >= 100:
            precio_anterior = monto
    if etiqueta:
        if re.search(r"USD", etiqueta, re.I):
            moneda = "USD"
        elif "€" in etiqueta:
            moneda = "EUR"
        elif "$" in etiqueta:
            moneda = "USD"
    if precio is not None and precio <= 0:
        precio, precio_anterior = None, None

    desc = re.search(r'<div class="product attribute description">(.*?)</div>', html, re.S)
    descripcion = (
        re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", desc.group(1))).strip() if desc else ""
    )

    time.sleep(delay)
    return {
        "nombre": sanear_contactos(nombre),
        "url": url,
        "precio": precio,
        "precio_anterior": precio_anterior,
        "moneda": moneda,
        "etiqueta": etiqueta,
        "descripcion": sanear_contactos(descripcion[:1500]),
    }


def es_repuesto(nombre: str) -> bool:
    if re.search(REPUESTO_PATRON, nombre, re.I):
        return True
    return bool(re.search(r"\(for electric", nombre, re.I))


def clasificar(nombre: str, origen: str) -> tuple[str, str, str]:
    """Devuelve (categoria, tipo_vehiculo, motivo_exclusion)."""
    n = nombre.lower()

    if re.search(TRICICLO_PATRON, n):
        return "", "", "triciclo_fuera_de_lista_blanca"
    if es_repuesto(nombre):
        return "", "", "repuesto_fuera_de_lista_blanca"
    if re.search(PATINETE_PATRON, n):
        return "patinete", "patinete_electrico", ""
    if re.search(CC_PATRON, n) or origen == "combustion":
        if re.search(CC_PATRON, n) and not re.search(r"electric|el[eé]ctr", n):
            return "combustion", "combustion", ""
    if re.search(BICI_PATRON, n):
        return "electrica", "bicicleta_electrica", ""
    if re.search(MOTO_PATRON, n):
        if re.search(r"electric|el[eé]ctr|lifepo4|lt[- ]?4\d{3}|\d{2,3}\s*v\b", n):
            return "electrica", "moto_electrica", ""
        if origen == "electricos":
            return "electrica", "moto_electrica", ""
        return "combustion", "combustion", ""
    if origen == "electricos":
        return "electrica", "moto_electrica", ""
    return "", "", "fuera_de_lista_blanca"


def marca_de(nombre: str) -> str:
    n = nombre.lower()
    for marca in ("vedca", "hongli", "yamaki", "topmaq", "volta", "torvan"):
        if marca in n:
            return marca.upper()
    if re.search(r"lt[- ]?4\d{3}", n):
        return "VEDCA"
    return "SIN_MARCA"


def modelo_de(nombre: str) -> str | None:
    m = re.search(r"LT[\s-]?(\d{4})", nombre, re.I)
    if m:
        modelo = f"LT-{m.group(1)}"
        suf = re.search(rf"LT[\s-]?{m.group(1)}\s+([A-Z]\d)", nombre, re.I)
        if suf:
            modelo += f" {suf.group(1).upper()}"
        return modelo
    m = re.search(r"\b(42\d{2})\b", nombre)
    if m:
        modelo = m.group(1)
        suf = re.search(rf"\b{m.group(1)}\s+([A-Z]\d)\b", nombre)
        if suf:
            modelo += f" {suf.group(1).upper()}"
        return modelo
    m = re.search(r"\b([A-Z]{2,4}-?[A-Z]?\d{2,4})\b", nombre.upper())
    return m.group(1) if m else None


def numeros(texto: str) -> dict:
    return {
        "voltaje": (re.search(r"(\d{2,3})\s*V\b", texto, re.I) or [None, None])[1]
        if re.search(r"(\d{2,3})\s*V\b", texto, re.I)
        else None,
        "capacidad_ah": (
            float(re.search(r"(\d+(?:\.\d+)?)\s*Ah", texto, re.I).group(1))
            if re.search(r"(\d+(?:\.\d+)?)\s*Ah", texto, re.I)
            else None
        ),
        "watts": (
            int(re.search(r"(\d{3,4})\s*W\b", texto, re.I).group(1))
            if re.search(r"(\d{3,4})\s*W\b", texto, re.I)
            else None
        ),
        "cc": (
            int(re.search(r"(\d{2,3})\s*cc\b", texto, re.I).group(1))
            if re.search(r"(\d{2,3})\s*cc\b", texto, re.I)
            else None
        ),
    }


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
    parser = argparse.ArgumentParser(description="Scraper de precios Islagrande")
    parser.add_argument("--proyecto", default="Mercado-de-Motos", help="Ruta del proyecto")
    parser.add_argument("--delay", type=float, default=1.0, help="Pausa entre peticiones")
    parser.add_argument("--sin-fichas", action="store_true",
                        help="No leer fichas individuales (solo tarjetas)")
    args = parser.parse_args()

    raiz = Path(args.proyecto).resolve()
    sello = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    ahora = datetime.now().astimezone().isoformat(timespec="seconds")

    lineas: list[str] = []
    log(lineas, "=" * 70)
    log(lineas, f"PRECIOS ISLAGRANDE - {ahora}")
    log(lineas, f"Proyecto: {raiz}")
    log(lineas, "=" * 70)

    session = requests.Session()
    session.headers.update(UA)

    cat_elec = BASE + CATEGORIAS["electricos"]
    log(lineas, "0) Activando moneda USD en la tienda...")
    usd_ok = cambiar_a_usd(session, cat_elec)
    log(lineas, f"   USD activo: {usd_ok}")

    log(lineas, "1) Leyendo categorias...")
    candidatos: dict[str, dict] = {}

    def agregar(items: list[dict]) -> None:
        for it in items:
            previo = candidatos.get(it["url"])
            if previo is None:
                candidatos[it["url"]] = it
            else:
                previo.setdefault("fuentes", []).append(it["origen_categoria"])

    for clave in ("electricos", "combustion", "triciclos"):
        agregar(paginas_de_categoria(session, CATEGORIAS[clave], clave, lineas,
                                     args.delay))
        time.sleep(args.delay)

    # Respaldo: portada + sitemap, por si algun vehiculo no esta en categoria
    log(lineas, "2) Respaldo (portada y sitemap)...")
    respaldo = 0
    try:
        html_home = obtener(session, BASE + "/")
        for href in sorted(set(re.findall(r'href="(https://islagrande\.com/[^"]+\.html)"',
                                          html_home))):
            if re.search(r"motocicleta|moto-electrica|bicicleta-electrica|scooter|patinet",
                         href) and href not in candidatos:
                candidatos[href] = {
                    "nombre": Path(href).stem.replace("-", " "),
                    "url": href,
                    "sku": "",
                    "precio_final": None,
                    "precio_anterior": None,
                    "etiqueta": "",
                    "descuento": "",
                    "origen_categoria": "portada",
                }
                respaldo += 1
        html_mapa = obtener(session, BASE + "/sitemap.xml")
        for href in sorted(set(re.findall(r"<loc>([^<]+)</loc>", html_mapa))):
            if re.search(r"moto-electrica|bicicleta-electrica|motocicleta-", href) \
                    and href not in candidatos:
                candidatos[href] = {
                    "nombre": Path(href).stem.replace("-", " "),
                    "url": href,
                    "sku": "",
                    "precio_final": None,
                    "precio_anterior": None,
                    "etiqueta": "",
                    "descuento": "",
                    "origen_categoria": "sitemap",
                }
                respaldo += 1
    except Exception as exc:  # noqa: BLE001
        log(lineas, f"   respaldo ERROR: {exc}")
    log(lineas, f"   candidatos extra: {respaldo}")
    log(lineas, f"   candidatos totales: {len(candidatos)}")

    # Fichas y clasificacion -----------------------------------------------
    log(lineas, "3) Leyendo fichas y clasificando...")
    registros_raw: list[dict] = []
    incluidos: list[dict] = []
    errores: list[str] = []

    for i, (url, cand) in enumerate(sorted(candidatos.items()), 1):
        nombre = cand["nombre"]
        precio = cand["precio_final"]
        precio_anterior = cand["precio_anterior"]
        moneda = "USD" if usd_ok else ""
        descripcion = ""
        ficha_url = url

        requiere_ficha = (
            not args.sin_fichas
            and cand["origen_categoria"] not in ("triciclos",)
            and precio is None
        ) or (
            not args.sin_fichas
            and cand["origen_categoria"] in ("electricos", "combustion", "portada", "sitemap")
        )

        if requiere_ficha:
            try:
                ficha = parsear_ficha(session, url, lineas, args.delay)
                if ficha["nombre"]:
                    nombre = ficha["nombre"]
                if ficha["precio"] is not None:
                    precio = ficha["precio"]
                if ficha["precio_anterior"] is not None:
                    precio_anterior = ficha["precio_anterior"]
                moneda = ficha["moneda"] or moneda
                descripcion = ficha["descripcion"]
                log(lineas, f"   [{i:02d}] {nombre[:60]} -> "
                            f"{precio if precio is not None else 'sin precio'}")
            except Exception as exc:  # noqa: BLE001
                errores.append(f"{url}: {exc}")
                log(lineas, f"   [{i:02d}] ERROR: {exc}")

        categoria, tipo_vehiculo, motivo = clasificar(nombre, cand["origen_categoria"])
        incluido = not motivo
        specs = numeros(f"{nombre} {descripcion}")

        registro = {
            "nombre": nombre,
            "url": url,
            "sku": cand["sku"],
            "origen_categoria": cand["origen_categoria"],
            "precio": precio,
            "precio_anterior": precio_anterior,
            "moneda": moneda,
            "descuento": cand["descuento"],
            "categoria": categoria,
            "tipo_vehiculo": tipo_vehiculo,
            "incluido": incluido,
            "motivo_exclusion": motivo,
            "descripcion": descripcion,
            "especificaciones": specs,
        }
        registros_raw.append(registro)

        if not incluido:
            continue

        reg = {
            "id": f"islagrande-{Path(url).stem}",
            "fuente": "islagrande.com",
            "titulo": nombre,
            "titulo_normalizado": nombre.upper(),
            "marca": marca_de(nombre),
            "modelo": modelo_de(nombre),
            "categoria": categoria,
            "categoria_clave": CATEGORIA_CLAVE[categoria],
            "tipo_vehiculo": tipo_vehiculo,
            "subtipo": tipo_vehiculo,
            "es_electrica": categoria != "combustion",
            "precio": precio,
            "precio_valido": precio is not None and precio >= 100,
            "moneda": moneda or "USD",
            "sin_precio": precio is None,
            "precio_anterior": precio_anterior,
            "descuento": cand["descuento"] or None,
            "anio_modelo": None,
            "cc": specs["cc"],
            "watts": specs["watts"],
            "voltaje": int(specs["voltaje"]) if specs["voltaje"] else None,
            "capacidad_ah": specs["capacidad_ah"],
            "descripcion": descripcion,
            "sku": cand["sku"] or None,
            "tienda": "Islagrande",
            "provincia": "",
            "municipio": "",
            "url": url,
            "fecha_captura": ahora,
            "es_outlier": False,
            "outlier_metodo": "",
            "outlier_zscore": None,
        }
        incluidos.append(reg)

    # Salidas ---------------------------------------------------------------
    raw_dir = raiz / "data" / "raw"
    proc_dir = raiz / "data" / "processed"
    dataset_dir = raiz / "datos" / "tiendas_online" / "islagrande"
    informes_dir = raiz / "docs" / "informes"
    logs_dir = raiz / "logs"
    for d in (raw_dir, proc_dir, dataset_dir, informes_dir, logs_dir):
        d.mkdir(parents=True, exist_ok=True)

    resumen_raw = {
        "fuente": "islagrande.com",
        "generado_habana": ahora,
        "params": {"delay": args.delay, "usd": usd_ok},
        "total_consultados": len(registros_raw),
        "total_incluidos": len(incluidos),
        "total_descartados": len(registros_raw) - len(incluidos),
        "errores": errores,
        "productos": registros_raw,
    }
    raw_json = raw_dir / f"islagrande_raw_{sello}.json"
    raw_json.write_text(json.dumps(resumen_raw, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    campos_raw = [c for c in registros_raw[0].keys()] if registros_raw else []
    escribir_csv(raw_dir / f"islagrande_raw_{sello}.csv", registros_raw, campos_raw)

    resumen_proc = {
        "origen": raw_json.name,
        "generado_habana": ahora,
        "total": len(incluidos),
        "total_precio_valido": sum(1 for r in incluidos if r["precio_valido"]),
        "total_sin_precio": sum(1 for r in incluidos if r["sin_precio"]),
        "descartes": [
            {"nombre": p["nombre"], "motivo": p["motivo_exclusion"]}
            for p in registros_raw
            if not p["incluido"]
        ],
        "registros": incluidos,
    }
    proc_json = proc_dir / f"islagrande_processed_{sello}.json"
    proc_json.write_text(json.dumps(resumen_proc, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    campos = list(incluidos[0].keys()) if incluidos else []
    escribir_csv(proc_dir / f"islagrande_processed_{sello}.csv", incluidos, campos)

    dataset = {"registros": incluidos, "generado_habana": ahora,
               "origen": proc_json.name}
    (dataset_dir / f"islagrande_{sello}.json").write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    escribir_csv(dataset_dir / f"islagrande_{sello}.csv", incluidos, campos)

    # Informe ---------------------------------------------------------------
    por_categoria: dict[str, int] = {}
    for reg in incluidos:
        por_categoria[reg["categoria"]] = por_categoria.get(reg["categoria"], 0) + 1
    excluidos = [p for p in registros_raw if not p["incluido"]]
    validos = [r for r in incluidos if r["precio_valido"]]
    con_precio = validos

    md = [
        "# Precios de motos en Islagrande (tienda online, USD)",
        "",
        f"- **Generado (La Habana):** {ahora}",
        f"- **Origen de los datos:** {proc_json.name}",
        f"- **Productos consultados:** {len(registros_raw)}",
        f"- **Productos incluidos (lista blanca):** {len(incluidos)}",
        f"- **Productos excluidos (triciclos/repuestos):** {len(excluidos)}",
        f"- **Precios validos (>= 100 USD):** {len(validos)}",
        "",
        "## Productos por categoria",
        "",
        "| Categoria | Productos | Con precio valido |",
        "|---|---:|---:|",
    ]
    for cat in ("combustion", "electrica", "patinete"):
        if por_categoria.get(cat):
            n_precio = sum(
                1 for r in incluidos
                if r["categoria"] == cat and r["precio_valido"]
            )
            md.append(f"| {cat} | {por_categoria[cat]} | {n_precio} |")
    md += [
        "",
        "## Catalogo con precios (USD)",
        "",
        "| Producto | Categoria | Marca | Modelo | Precio USD | Antes USD | Especificaciones |",
        "|---|---|---|---|---:|---:|---|",
    ]
    vistos: set[tuple[str, float]] = set()
    duplicados = 0
    for reg in sorted(validos, key=lambda r: (r["categoria"], r["precio"])):
        clave = (reg["titulo"], reg["precio"])
        if clave in vistos:
            duplicados += 1
            continue
        vistos.add(clave)
        espec = []
        if reg["voltaje"]:
            espec.append(f"{reg['voltaje']}V")
        if reg["capacidad_ah"]:
            espec.append(f"{reg['capacidad_ah']:g}Ah")
        if reg["watts"]:
            espec.append(f"{reg['watts']}W")
        if reg["cc"]:
            espec.append(f"{reg['cc']}cc")
        md.append(
            "| {t} | {c} | {m} | {mod} | {p} | {a} | {e} |".format(
                t=reg["titulo"],
                c=reg["categoria"],
                m=reg["marca"],
                mod=reg["modelo"] or "-",
                p=f"{reg['precio']:,.2f}",
                a=f"{reg['precio_anterior']:,.2f}"
                if reg["precio_anterior"]
                and reg["precio_anterior"] > reg["precio"] >= 100
                else "-",
                e=", ".join(espec) or "-",
            )
        )
    md += [
        "",
        "## Notas",
        "",
        "- Precios en **USD**, moneda activada en la tienda antes de la captura.",
        "- Solo se listan precios **validos (>= 100 USD)**; los importes",
        "  implausibles se conservan en `data/raw/` como evidencia y quedan",
        "  marcados `precio_valido: false` en `data/processed/`.",
        f"- Filas repetidas (mismo producto publicado en varias sedes): {duplicados}"
        + " omitidas en esta tabla."
        if duplicados
        else "- Sin productos repetidos en el catalogo.",
        "- Los **triciclos** y los repuestos/accesorios quedan solo en `data/raw/`",
        "  como evidencia, fuera del analisis.",
        "- Los productos sin precio publicado se marcan `sin_precio` y no entran",
        "  a las metricas.",
        "",
    ]
    informe = informes_dir / f"islagrande_precios_{sello}.md"
    informe.write_text("\n".join(md), encoding="utf-8")

    log(lineas, f"4) Dato crudo  -> {raw_json}")
    log(lineas, f"5) Procesado   -> {proc_json}")
    log(lineas, f"6) Dataset     -> {dataset_dir / ('islagrande_' + sello + '.json')}")
    log(lineas, f"7) Informe     -> {informe}")
    log(lineas, "")
    log(lineas, "Incluidos por categoria: " + json.dumps(por_categoria, ensure_ascii=False))
    log(lineas, f"Excluidos (solo raw): {len(excluidos)}")
    log(lineas, f"Con precio: {len(con_precio)} / {len(incluidos)}")
    log(lineas, f"Errores: {len(errores)}")
    log(lineas, "=" * 70)

    (logs_dir / f"islagrande_{sello}.log").write_text("\n".join(lineas) + "\n",
                                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
