#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eliminacion de datos de contacto (telefonos y correos) en textos.
===============================================================

Los datos del proyecto nunca deben contener telefonos ni correos
(regla de privacidad del proyecto). Esta utilidad se aplica en los
scrapers y en el ETL justo antes de guardar, y tambien puede usarse
para sanear ficheros ya existentes.

Uso como modulo:
    from contactos import sanear_contactos
    texto = sanear_contactos(texto)

Uso desde linea de comandos (sanea ficheros .json/.csv in place):
    python src/contactos.py data_clean/anuncios_limpios.json ...
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# +53 con formatos: "+53 5 994-8751", "+5354701131", "+53 7 656-2154"
TEL_53 = re.compile(r"\+53[\s.-]*\d(?:[\s.-]*\d){6,11}")
# Etiqueta seguida de numero: "telefono: 555 12 34", "whatsapp 5 994-8751"
TEL_ETIQUETA = re.compile(
    r"(?i)\b(?:tel[eé]fono|whatsapp|celular|m[oó]vil)\b"
    r"[^0-9\"'\n,]{0,20}\+?\d[\d\s.-]{6,}\d"
)
# Moviles/lineas cubanas locales: "5 994-8751", "7 656-2154"
TEL_LOCAL = re.compile(r"(?<![\d.])[5-9][\s-]\d{3}[\s-]?\d{4}(?![\d.])")


def sanear_contactos(texto, colapsar: bool = True):
    """Devuelve `texto` sin telefonos ni correos."""
    if not texto or not isinstance(texto, str):
        return texto
    original = texto
    texto = TEL_ETIQUETA.sub("", texto)
    texto = TEL_53.sub("", texto)
    texto = EMAIL.sub("", texto)
    texto = TEL_LOCAL.sub("", texto)
    if colapsar and texto != original:
        texto = re.sub(r"[ \t]{2,}", " ", texto)
        texto = re.sub(r"\s+([,.;:])", r"\1", texto)
        texto = texto.strip()
    return texto


def sanear_fichero(ruta: Path) -> bool:
    """Sanea un fichero .json/.csv en su sitio. Devuelve True si cambio."""
    texto = ruta.read_text(encoding="utf-8")
    nuevo = sanear_contactos(texto, colapsar=False)
    if nuevo == texto:
        return False
    if ruta.suffix.lower() == ".json":
        json.loads(nuevo)  # si falla la validacion, no se escribe
    ruta.write_text(nuevo, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    cambiados = 0
    for arg in argv:
        ruta = Path(arg)
        if not ruta.exists():
            print(f"  [no existe] {ruta}")
            continue
        if sanear_fichero(ruta):
            cambiados += 1
            print(f"  saneado: {ruta}")
        else:
            print(f"  sin cambios: {ruta}")
    print(f"Ficheros modificados: {cambiados}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
