#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza y normalizacion de los datos crudos de Revolico (La Habana)
===================================================================

Toma el JSON de datos crudos mas reciente de `datos/revolico/` y lo limpia:

    1. Normaliza el titulo: convierte letras decoradas (𝐌𝐎𝐓О -> MOTO), elimina
       emojis y simbolos, y colapsa espacios dobles.
    2. Detecta y normaliza la MARCA (ej. MISOSHUKI -> MISHOZUKI, KRATOS ->
       KRATHOS, X MOTORS -> XMOTORS).
    3. Clasifica el TIPO de vehiculo (combustion, moto/bicicleta/bicimoto/patinete
       electrico, u otro electrico).
    4. Normaliza el PRECIO: lo deja numerico y marca como invalido el valor de
       relleno (0, 1) o los no numericos.
    5. Extrae el ANIO de modelo, el CILINDRAJE (cc) y la POTENCIA (W) del titulo.

Los resultados quedan en `datos/limpios/` en CSV y JSON, listos para analisis.

Uso:
    python limpiar_revolico.py
    python limpiar_revolico.py --archivo datos/revolico/anuncios_revolico_XXXX.json
"""

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ_HABANA = ZoneInfo("America/Havana")
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATOS_CRUDOS = REPO_ROOT / "datos" / "revolico"
DATOS_LIMPIOS = REPO_ROOT / "datos" / "limpios"

# Precios minimos considerados reales (por debajo son "relleno" / a negociar)
PRECIO_MINIMO = 100

# ---------------------------------------------------------------------------
# Normalizacion de texto
# ---------------------------------------------------------------------------
def normalizar_titulo(titulo):
    """Quita emojis/simbolos y deja un titulo legible."""
    if not titulo:
        return ""
    # 𝐌𝐎𝐓𝐎 -> MOTO, ① -> 1, ² -> 2, etc.
    s = unicodedata.normalize("NFKC", titulo)
    # Conservar solo letras, digitos y puntuacion basica
    s = re.sub(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s.,\-/():'!¿?+%*&$#@]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def quitar_acentos(texto):
    s = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in s if not unicodedata.combining(c)).upper()


# ---------------------------------------------------------------------------
# Normalizacion de marcas
# ---------------------------------------------------------------------------
# canonica -> variantes reales encontradas en los anuncios
MARCAS_CANONICAS = {
    "XMOTORS": ["XMOTORS", "X MOTORS", "X-MOTORS", "XMOTOS"],
    "KRATHOS": ["KRATHOS", "KRATOS"],
    "MISHOZUKI": ["MISHOZUKI", "MISOSHUKI", "MICHOSUKI", "MISHOZUK"],
    "MIKAZUKI": ["MIKAZUKI", "MIKASZUKI", "MIKAZUKI", "MIKAZUKI"],
    "HAOJIANG": ["HAOJIANG", "HAO JIANG", "HAO JIANG"],
    "MOTORSTRECK": ["MOTORSTRECK", "MOTOR STRECK", "MOTORSTREK"],
    "BUCATTI": ["BUCATTI", "BUCATI", "BUCATTI"],
    "BEVOMECON": ["BEVOMECON", "BEVOMECON"],
    "TREVALIX": ["TREVALIX", "TREVALIX"],
    "YESELF": ["YESELF", "YES EL F", "YESELF"],
    "KATZU": ["KATZU", "KATZU"],
    "ITALY": ["ITALY", "ITALI"],
    "LIFAN": ["LIFAN"],
    "JIN": ["JIN"],
    "UNISON": ["UNISON"],
    "VEDCA": ["VEDCA"],
    "CHALLENGER": ["CHALLENGER"],
    "MOUNTAIN": ["MOUNTAIN"],
    "KVITOVA": ["KVITOVA"],
    "MOTICO": ["MOTICO", "MOTICO"],
    "YOAZAKY": ["YOAZAKY", "YOA ZAKY"],
    "TOPMAQ": ["TOPMAQ", "TOPMAQ"],
    "OWAY": ["OWAY"],
    "JMD": ["JMD"],
    "MAF": ["MAF"],
    "MRK": ["MRK"],
    "LAZER": ["LAZER"],
    "MIDHA": ["MIDHA"],
    "SK8": ["SK8"],
    "OKDAY": ["OKDAY"],
    "PROTENZZA": ["PROTENZZA", "PROTENZA"],
    "TORVAN": ["TORVAN"],
    "OUPES": ["OUPES"],
    "XIAOMI": ["XIAOMI"],
    "KAWASAKI": ["KAWASAKI"],
    "VESPA": ["VESPA"],
    "TREK": ["TREK", "TRECK"],
    "SIERRA": ["SIERRA"],
}

# lista plana de (variante_sin_acentos, canonica) para busqueda rapida
_VARIANTES = []
for canonica, variantes in MARCAS_CANONICAS.items():
    for v in variantes:
        _VARIANTES.append((quitar_acentos(v), canonica))


def detectar_marca(titulo):
    """Devuelve la marca canonica o None."""
    t = quitar_acentos(titulo)
    mejor = None
    for variante, canonica in _VARIANTES:
        # coincidencia por palabra completa
        if re.search(rf"\b{re.escape(variante)}\b", t):
            if mejor is None or len(variante) > len(mejor[0]):
                mejor = (variante, canonica)
    return mejor[1] if mejor else None


# ---------------------------------------------------------------------------
# Clasificacion de tipo de vehiculo
# ---------------------------------------------------------------------------
def clasificar_vehiculo(categoria_clave, titulo_normalizado, es_electrica):
    """Devuelve una clave de tipo de vehiculo."""
    t = quitar_acentos(titulo_normalizado)
    if categoria_clave == "motos_combustion":
        if "SCOOTER" in t or "VESPA" in t:
            return "combustion_scooter"
        if "DEPORTIVA" in t or "NINJA" in t:
            return "combustion_deportiva"
        return "combustion"
    if not es_electrica:
        return "otro"
    if "PATIN" in t:
        return "patinete_electrico"
    if "BICIMOTO" in t:
        return "bicimoto_electrica"
    if "BICICLETA" in t or "EBIKE" in t or "E BIKE" in t or "E-BIKE" in t:
        return "bicicleta_electrica"
    if "MOTICO" in t or "MOTO" in t or "SCOOTER" in t:
        return "moto_electrica"
    return "electrico_sin_clasificar"


# ---------------------------------------------------------------------------
# Extraccion de atributos del titulo
# ---------------------------------------------------------------------------
def extraer_anio(titulo):
    for y in re.findall(r"\b(20[1-3]\d)\b", titulo or ""):
        return int(y)
    return None


def extraer_cc(titulo):
    m = re.search(r"\b(\d{2,4})\s*(?:CC|Cc|cc)\b", titulo or "")
    return int(m.group(1)) if m else None


def extraer_watts(titulo):
    m = re.search(r"\b(\d{2,5})\s*(?:W|WATTS|Wats|w)\b", titulo or "")
    return int(m.group(1)) if m else None


def extraer_voltaje(titulo):
    m = re.search(r"\b(\d{2,3})\s*V\b", titulo or "")
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Precios
# ---------------------------------------------------------------------------
def normalizar_precio(precio):
    """Devuelve (precio_numerico, es_valido)."""
    if precio in (None, ""):
        return None, False
    if isinstance(precio, (int, float)):
        p = float(precio)
    else:
        limpio = re.sub(r"[^\d.,]", "", str(precio))
        limpio = limpio.replace(",", ".")
        try:
            p = float(limpio)
        except ValueError:
            return None, False
    if p <= 0:
        return None, False
    if p < PRECIO_MINIMO:  # 1, 2, 5... son valores de relleno
        return None, False
    return round(p), True


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def json_mas_reciente():
    archivos = sorted(DATOS_CRUDOS.glob("anuncios_revolico_*.json"))
    if not archivos:
        raise SystemExit("No hay datos crudos en datos/revolico/")
    return archivos[-1]


def limpiar(anuncios):
    filas = []
    for a in anuncios:
        titulo_limpio = normalizar_titulo(a.get("titulo"))
        es_elec = bool(a.get("es_electrica")) or any(
            c in quitar_acentos(titulo_limpio)
            for c in ("ELECTRIC", "LITIO", "BATERIA", "EBIKE", "BICICLETA")
        )
        precio, valido = normalizar_precio(a.get("precio"))
        filas.append(
            {
                "id": a.get("id", ""),
                "categoria": a.get("categoria", ""),
                "categoria_clave": a.get("categoria_clave", ""),
                "tipo_vehiculo": clasificar_vehiculo(
                    a.get("categoria_clave"), titulo_limpio, es_elec
                ),
                "marca": detectar_marca(titulo_limpio) or "SIN_MARCA",
                "titulo": titulo_limpio,
                "precio": precio,
                "precio_valido": valido,
                "moneda": (a.get("moneda") or "USD").upper(),
                "anio_modelo": extraer_anio(titulo_limpio),
                "cc": extraer_cc(titulo_limpio),
                "watts": extraer_watts(titulo_limpio),
                "voltaje": extraer_voltaje(titulo_limpio),
                "es_electrica": es_elec,
                "vistas": a.get("vistas", 0),
                "imagenes": a.get("imagenes", 0),
                "promocionado": a.get("promocionado", False),
                "url": a.get("url", ""),
                "fecha_utc": a.get("fecha_utc", ""),
                "fecha_habana": a.get("fecha_habana", ""),
            }
        )
    return filas


def guardar(filas, origen):
    DATOS_LIMPIOS.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now(TZ_HABANA)
    sello = ahora.strftime("%Y%m%d_%H%M")
    meta = {
        "origen": origen.name,
        "generado_habana": ahora.isoformat(),
        "total": len(filas),
        "total_precio_valido": sum(1 for f in filas if f["precio_valido"]),
        "registros": filas,
    }
    ruta_json = DATOS_LIMPIOS / f"revolico_limpio_{sello}.json"
    ruta_json.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    columnas = list(filas[0].keys())
    ruta_csv = DATOS_LIMPIOS / f"revolico_limpio_{sello}.csv"
    with ruta_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)
    return ruta_json, ruta_csv


def imprimir_resumen(filas):
    print(f"Total de registros limpios: {len(filas)}")
    print(f"Con precio valido (>= {PRECIO_MINIMO} USD): "
          f"{sum(1 for f in filas if f['precio_valido'])}")

    print("\nPor tipo de vehiculo:")
    for tipo, n in Counter(f["tipo_vehiculo"] for f in filas).most_common():
        print(f"  {tipo:<28} {n:>6}")

    print("\nMarcas mas comunes:")
    for marca, n in Counter(f["marca"] for f in filas).most_common(12):
        print(f"  {marca:<18} {n:>6}")


def main():
    parser = argparse.ArgumentParser(description="Limpieza de datos de Revolico")
    parser.add_argument("--archivo", default=None, help="Ruta al JSON crudo")
    args = parser.parse_args()

    origen = Path(args.archivo) if args.archivo else json_mas_reciente()
    datos = json.loads(origen.read_text(encoding="utf-8"))
    filas = limpiar(datos["anuncios"])

    imprimir_resumen(filas)
    ruta_json, ruta_csv = guardar(filas, origen)
    print(f"\nDatos limpios guardados:\n  - {ruta_csv}\n  - {ruta_json}")


if __name__ == "__main__":
    main()
