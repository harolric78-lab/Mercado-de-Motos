#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades compartidas del pipeline de scraping de Revolico.

Contiene:
  - Resolucion de rutas del proyecto (datos/raw, datos/processed, logs, datos/...)
  - Normalizacion de texto, precios, monedas y URLs
  - Reglas de negocio: inclusion/exclusion de vehiculos y deteccion de triciclos
  - Logger con contadores para el archivo de log
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:  # evita UnicodeEncodeError en consolas Windows (cp1252)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

BASE_URL = "https://www.revolico.com"
TZ_HABANA = ZoneInfo("America/Havana")
PROVINCIA = "la-habana"
CATEGORIA = "vehiculos"

# Subcategorias de Revolico que se scrapean (La Habana)
SUBCATEGORIAS = {
    "combustion": "vehiculos-motos-de-combustion",
    "electricas": "vehiculos-motos-electricas-y-triciclos",
}

# Categorias permitidas por la regla de negocio
CATEGORIAS_PERMITIDAS = ("combustion", "electrica", "patinete")

# ---------------------------------------------------------------------------
# Palabras clave (se comparan sin acentos y en minusculas)
# ---------------------------------------------------------------------------
# Evidencia positiva de cada categoria permitida
MOTO = ("moto", "motocicleta", "motico", "motoneta", "scooter", "vespa",
        "ciclomotor", "moped", "minimoto")
PATINETE = ("patinete", "patineta", "monopatin",
            "patin electrico", "patin electrica")
BICICLETA = ("bicicleta", "bicicl", "bicimoto", "bicimot", "ebike",
             "e bike", "bici")
COMBUSTION_EVID = ("combustion", "combustible", "gasolina", "petroleo",
                   "diesel", "cilindrada", "chimoto")
ELECTRICA_EVID = ("electrica", "electrico", "electric", "bateria", "litio",
                  "lithium", "lifepo", "electromoto", "motor electrico",
                  "48v", "60v", "72v", "84v")
ACCESORIO = ("repuesto", "repuestos", "accesorio", "accesorios", "extensor",
             "cargador", "llanta", "llantas", "neumatico", "escape", "manillar",
             "asiento", "espejo", "espejos", "faro", "faros", "cuadro", "buje",
             "freno", "frenos", "cadena", "pedal", "maneta", "filtro", "aceite",
             "bateria de", "motor de", "motor para", "kit de", "engranaje",
             "bombin", "guiño", "balancin", "culata", "carcasa", "pintura",
             "guantes", "casco", "arnes", "motor", "motores")
# Evidencia fuerte de vehiculo completo (para no confundir un accesorio)
VEHICULO_FUERTE = ("motocicleta", "moto electrica", "motico", "vespa",
                   "patinete", "patineta", "monopatin", "ciclomotor", "moped",
                   "scooter electrico", "scooter electrica", "scooter plegable",
                   "combustion", "combustible", "gasolina",
                   "bicicleta electrica", "bicimoto")
# Compuestos que no son moto ni patinete (evitan falsos positivos con "moto")
NO_PERMITIDO = ("triciclo", "trimoto", "tricimoto", "cuatrimoto", "mototaxi",
                "motocarro", "motocasa", "mototren", "autocarro", "quad",
                "buggy", "sidecar", "rickshaw", "tres ruedas", "3 ruedas")

# Motivos de descarte. Triciclos y similares no se etiquetan: solo quedan
# fuera de las tres categorias permitidas.
MOTIVOS = {
    "no_permitido": "No es moto de combustion, moto electrica ni patinete",
    "no_vehiculo": "No es un vehiculo (repuesto o accesorio)",
    "sin_titulo": "Anuncio sin titulo",
    "fuera_de_categorias": "No se identifica como una categoria permitida",
    "precio_ausente": "Anuncio sin precio",
    "url_invalida": "Anuncio sin URL valida",
    "duplicado": "Anuncio duplicado",
    "fuera_del_ranking": "Fuera del top de anuncios mas recientes",
    "error_descarga": "Error al descargar el detalle del anuncio",
}

# Marcas normalizadas (variantes -> canonica). Mismo criterio que el
# proyecto original (src/limpieza_datos/limpiar_revolico.py).
MARCAS_CANONICAS = {
    "XMOTORS": ["XMOTORS", "X MOTORS", "X-MOTORS", "XMOTOS"],
    "KRATHOS": ["KRATHOS", "KRATOS"],
    "MISHOZUKI": ["MISHOZUKI", "MISOSHUKI", "MICHOSUKI", "MISHOZUK"],
    "MIKAZUKI": ["MIKAZUKI", "MIKASZUKI", "MIKAZUKI"],
    "HAOJIANG": ["HAOJIANG", "HAO JIANG"],
    "MOTORSTRECK": ["MOTORSTRECK", "MOTOR STRECK", "MOTORSTREK"],
    "BUCATTI": ["BUCATTI", "BUCATI"],
    "BEVOMECON": ["BEVOMECON"],
    "TREVALIX": ["TREVALIX"],
    "YESELF": ["YESELF", "YES EL F"],
    "KATZU": ["KATZU"],
    "ITALY": ["ITALY", "ITALI"],
    "LIFAN": ["LIFAN"],
    "JIN": ["JIN"],
    "UNISON": ["UNISON"],
    "VEDCA": ["VEDCA"],
    "CHALLENGER": ["CHALLENGER"],
    "MOUNTAIN": ["MOUNTAIN"],
    "KVITOVA": ["KVITOVA"],
    "MOTICO": ["MOTICO"],
    "YOAZAKY": ["YOAZAKY", "YOA ZAKY"],
    "TOPMAQ": ["TOPMAQ"],
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
    "WERHY": ["WERHY"],
    "KIWITOWA": ["KIWITOWA", "KIWITOWA", "KIWI TOWA"],
}


# ---------------------------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------------------------
def project_root(start=None):
    """Resuelve la raiz del proyecto (donde viven datos/, docs/, src/)."""
    env = os.environ.get("REVOLICO_PROJECT_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    p = Path(start or Path.cwd()).resolve()
    candidatos = [p] + list(p.parents)
    for c in candidatos:
        if (c / "datos").is_dir() and (c / "src").is_dir():
            return c
    for c in candidatos:
        sub = c / "Mercado-de-Motos"
        if (sub / "datos").is_dir():
            return sub
    return p


def paths(root=None):
    """Devuelve el diccionario de carpetas del pipeline."""
    root = Path(root) if root else project_root()
    return {
        "root": root,
        "raw": root / "datos" / "raw",
        "processed": root / "datos" / "processed",
        "logs": root / "logs",
        "datos_revolico": root / "datos" / "revolico",
        "datos_limpios": root / "datos" / "limpios",
        "informes": root / "docs" / "informes",
        "graficos": root / "graficos",
        "notebooks": root / "notebooks",
        "src_analisis": root / "src" / "analisis",
        "src_visualizacion": root / "src" / "visualizacion",
        "archivo": root / "datos" / "_reemplazados",
    }


def sello(momento=None):
    """Sello temporal YYYYMMDD_HHMMSS en hora de La Habana."""
    momento = momento or datetime.now(TZ_HABANA)
    return momento.strftime("%Y%m%d_%H%M%S")


def ahora_habana():
    return datetime.now(TZ_HABANA)


# ---------------------------------------------------------------------------
# Texto
# ---------------------------------------------------------------------------
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF"
    "\U0000FE0F\U0000200D\U000020E3\U0001F1E6-\U0001F1FF]+"
)


def quitar_acentos(texto):
    s = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in s if not unicodedata.combining(c))


def norm(texto):
    """Minusculas, sin acentos, sin puntuacion: para comparar palabras clave."""
    s = quitar_acentos(texto or "").lower()
    s = re.sub(r"[^0-9a-z]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalizar_titulo(titulo):
    """Titulo legible: NFKC, sin emojis, sin caracteres de reemplazo."""
    if not titulo:
        return ""
    s = unicodedata.normalize("NFKC", str(titulo))
    s = _EMOJI.sub(" ", s)
    s = s.replace("\ufffd", " ")
    s = re.sub(r"[\u200b-\u200f\u202a-\u202e]", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n", s)
    s = re.sub(r"\n", " ", s)
    return s.strip(" -–—|,\t")


def contiene(texto_norm, claves):
    return any(c in texto_norm for c in claves)


# Indice de marcas: (variante normalizada -> marca canonica)
_VARIANTES = []
for _canonica, _vs in MARCAS_CANONICAS.items():
    for _v in _vs:
        _VARIANTES.append((norm(_v), _canonica))
_VARIANTES.sort(key=lambda x: len(x[0]), reverse=True)


def detecta_marca(titulo):
    """Devuelve la marca canonica o None."""
    t = norm(titulo)
    mejor = None
    for variante, canonica in _VARIANTES:
        if re.search(rf"\b{re.escape(norm(variante))}\b", t):
            if mejor is None or len(variante) > len(mejor[0]):
                mejor = (variante, canonica)
    return mejor[1] if mejor else None


def extraer_anio(titulo):
    for y in re.findall(r"\b(20[1-3]\d)\b", titulo or ""):
        return int(y)
    return None


def extraer_cc(titulo):
    m = re.search(r"\b(\d{2,4})\s*(?:cc|cm3)\b", titulo or "", re.I)
    return int(m.group(1)) if m else None


def extraer_watts(titulo):
    m = re.search(r"\b(\d{2,5})\s*(?:w|watts|wats)\b", titulo or "", re.I)
    return int(m.group(1)) if m else None


def extraer_voltaje(titulo):
    m = re.search(r"\b(\d{2,3})\s*v\b", titulo or "", re.I)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Precios, moneda y URLs
# ---------------------------------------------------------------------------
def parse_precio(valor):
    """Convierte a float. Devuelve None si no es numerico o es <= 0."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        p = float(valor)
    else:
        s = str(valor).strip()
        s = re.sub(r"[^\d.,]", "", s)
        if not s:
            return None
        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "," in s:
            s = s.replace(",", ".")
        try:
            p = float(s)
        except ValueError:
            return None
    if p <= 0:
        return None
    return round(p, 2)


MONEDAS = ("USD", "CUP", "MZN", "EUR", "CAD", "MXN", "BTC")


def detecta_moneda(moneda_cruda, titulo=""):
    """Normaliza la divisa. Devuelve (moneda, detectada_en_titulo)."""
    m = (moneda_cruda or "").strip().upper()
    if m in MONEDAS:
        return m, False
    t = norm(titulo)
    for clave in MONEDAS:
        if re.search(rf"\b{clave.lower()}\b", t):
            return clave, True
    if re.search(r"\b(cup|pesos?\s+cubanos?)\b", t):
        return "CUP", True
    if re.search(r"[$]|usd|dolar|dólar", t):
        return "USD", True
    return (m or "DESCONOCIDA"), False


URL_RE = re.compile(r"^https?://(www\.)?revolico\.com/item/[A-Za-z0-9\-_]+/?$")


def url_valida(url):
    return bool(url) and bool(URL_RE.match(url.strip()))


# ---------------------------------------------------------------------------
# Reglas de negocio: lista blanca de vehiculos
# ---------------------------------------------------------------------------
def contiene(texto_norm, claves):
    """True si alguna clave aparece al inicio de una palabra del texto."""
    for clave in claves:
        if re.search(rf"(?<![0-9a-z]){re.escape(clave)}", texto_norm):
            return True
    return False


def _categoria_texto(t, subcategoria):
    """
    Devuelve la categoria permitida si hay evidencia positiva en el texto,
    o None si el texto no permite afirmar que sea una de las tres.
    """
    sub_elec = subcategoria == "electricas"
    ev_moto = contiene(t, MOTO)
    ev_pat = contiene(t, PATINETE)
    ev_bici = contiene(t, BICICLETA)
    ev_comb = contiene(t, COMBUSTION_EVID) or bool(
        re.search(r"(?<![0-9a-z])\d{2,4}\s*cc(?![0-9a-z])", t)
    )
    ev_elec = contiene(t, ELECTRICA_EVID)

    # Patinete electrico
    if ev_pat and (ev_elec or sub_elec):
        return "patinete"
    if "scooter" in t and "plegable" in t and (ev_elec or sub_elec):
        return "patinete"

    # Moto de combustion
    if ev_comb and (ev_moto or subcategoria == "combustion"):
        return "combustion"

    # Moto electrica o bicicleta electrica (ambas entran como "electrica")
    if (ev_moto or ev_bici) and ev_elec:
        return "electrica"
    if ev_moto and sub_elec:
        return "electrica"
    if ev_bici and sub_elec:
        return "electrica"
    if ev_moto and subcategoria == "combustion":
        return "combustion"
    return None


def clasificar_vehiculo(titulo, descripcion="", subcategoria="combustion"):
    """
    Lista blanca: solo acepta motos de combustion, motos electricas
    (incluye bicicletas electricas) y patinetes electricos.

    Devuelve (categoria, motivo):
      categoria in {"combustion", "electrica", "patinete"} o None
      motivo = None si el anuncio entra; si no, un motivo interno.
    """
    t = norm(titulo)
    if not t:
        return None, "sin_titulo"

    # Compuestos que no son moto ni patinete (sin etiquetarlos)
    if contiene(t, NO_PERMITIDO):
        return None, "no_permitido"

    # Repuestos y accesorios (sin evidencia de vehiculo completo)
    if contiene(t, ACCESORIO) and not contiene(t, VEHICULO_FUERTE):
        return None, "no_vehiculo"

    categoria = _categoria_texto(t, subcategoria)
    if categoria:
        return categoria, None

    # Segundo intento con la descripcion (solo evidencia explicita)
    d = norm(descripcion)
    if d:
        if contiene(d, NO_PERMITIDO):
            return None, "no_permitido"
        categoria = _categoria_texto(d, subcategoria)
        if categoria:
            return categoria, None

    return None, "fuera_de_categorias"


def categoria_legacy(categoria):
    """Mapea la categoria nueva a las claves que usa el resto del proyecto."""
    return {
        "combustion": "motos_combustion",
        "electrica": "motos_electricas",
        "patinete": "motos_electricas",
    }.get(categoria, "")


def subtipo_vehiculo(categoria, titulo=""):
    """Subtipo descriptivo dentro de las tres categorias permitidas."""
    t = norm(titulo)
    if categoria == "combustion":
        if "scooter" in t or "vespa" in t:
            return "combustion_scooter"
        if "deportiva" in t or "ninja" in t:
            return "combustion_deportiva"
        return "combustion"
    if categoria == "patinete":
        return "patinete_electrico"
    if contiene(t, BICICLETA):
        return "bicicleta_electrica"
    return "moto_electrica"


def tipo_vehiculo_legacy(categoria, titulo=""):
    return subtipo_vehiculo(categoria, titulo)


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------
class Logger:
    """Escribe en consola y en logs/revolico_<sello>.log, y cuenta eventos."""

    def __init__(self, ruta_log=None, verbose=True):
        self.ruta_log = Path(ruta_log) if ruta_log else None
        self.verbose = verbose
        self.contadores = {}
        self.lineas = []
        if self.ruta_log:
            self.ruta_log.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg=""):
        self.lineas.append(str(msg))
        if self.verbose:
            print(msg, flush=True)
        if self.ruta_log:
            with self.ruta_log.open("a", encoding="utf-8") as fh:
                fh.write(str(msg) + "\n")

    def contar(self, clave, n=1):
        self.contadores[clave] = self.contadores.get(clave, 0) + n

    def __call__(self, msg=""):
        self.log(msg)

    def cerrar(self):
        if self.ruta_log:
            self.log("")
            self.log("--- Contadores ---")
            for k in sorted(self.contadores):
                self.log(f"{k}: {self.contadores[k]}")


def guardar_json(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


def guardar_csv(ruta, filas, columnas=None):
    import csv

    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not filas:
        filas = []
    if columnas is None:
        columnas = list(filas[0].keys()) if filas else []
    with ruta.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)
    return ruta
