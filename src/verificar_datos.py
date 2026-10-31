#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica la integridad del dataset publico y de los cortes historicos.

Uso:
    python src/verificar_datos.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[1]
CLEAN = BASE / "data" / "processed"

CATEGORIAS = {
    "motos_combustion": "Motos de Combustión",
    "motos_electricas": "Motos Eléctricas",
    "bicicletas_electricas": "Bicicletas Eléctricas",
    "patinetes": "Patinetes",
}
TOTAL_ESPERADO = 6101
CONTEOS_ESPERADOS = {
    "motos_combustion": 1099,
    "motos_electricas": 2201,
    "bicicletas_electricas": 2576,
    "patinetes": 225,
}
CORTE_20261026 = {
    "motos_combustion": 9,
    "motos_electricas": 3,
    "bicicletas_electricas": 17,
    "patinetes": 1,
}


def cargar(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8"))


def validar() -> tuple[list[str], dict]:
    errores: list[str] = []
    dataset = cargar(CLEAN / "anuncios_limpios.json")
    registros = dataset.get("registros", [])
    total = dataset.get("total", len(registros))

    if total != TOTAL_ESPERADO or len(registros) != TOTAL_ESPERADO:
        errores.append(f"Total inesperado: {len(registros)} (esperado {TOTAL_ESPERADO})")

    ids = [str(registro.get("id") or "") for registro in registros]
    if any(not identificador for identificador in ids):
        errores.append("Hay registros sin identificador")
    duplicados = [identificador for identificador, n in Counter(ids).items() if n > 1]
    if duplicados:
        errores.append(f"Identificadores duplicados: {duplicados[:5]}")

    for registro in registros:
        categoria = registro.get("categoria")
        if categoria not in CATEGORIAS:
            errores.append(f"Categoría no permitida en {registro.get('id')}: {categoria}")
            continue
        if registro.get("categoria_clave") != categoria:
            errores.append(f"categoria_clave inconsistente en {registro.get('id')}")
        if registro.get("categoria_nombre") != CATEGORIAS[categoria]:
            errores.append(f"categoria_nombre inconsistente en {registro.get('id')}")

    conteos = dict(Counter(registro.get("categoria") for registro in registros))
    if conteos != CONTEOS_ESPERADOS:
        errores.append(f"Conteos por categoría inesperados: {conteos}")

    for nombre, esperado in (("corte_20261022.json", 30), ("corte_20261026.json", 30)):
        corte = cargar(CLEAN / "cortes" / nombre)
        if corte.get("total") != esperado or len(corte.get("registros", [])) != esperado:
            errores.append(f"{nombre}: total inesperado")

    corte_26 = cargar(CLEAN / "cortes" / "corte_20261026.json")
    conteo_26 = dict(Counter(registro.get("categoria") for registro in corte_26.get("registros", [])))
    if conteo_26 != CORTE_20261026:
        errores.append(f"Conteos del corte 26/10 inesperados: {conteo_26}")

    for registro in corte_26.get("registros", []):
        if str(registro.get("id")) == "58383493" and registro.get("categoria") != "motos_combustion":
            errores.append("58383493 no está clasificado como combustión en el corte 26/10")

    resumen = {
        "total": len(registros),
        "categorias": conteos,
        "cortes": {
            "2026-10-22": cargar(CLEAN / "cortes" / "corte_20261022.json").get("total"),
            "2026-10-26": corte_26.get("total"),
        },
    }
    return errores, resumen


def main() -> int:
    errores, resumen = validar()
    if errores:
        print("Errores de validación:")
        for error in errores:
            print(f"  - {error}")
        return 1
    print("Dataset válido")
    print(f"  Total: {resumen['total']}")
    for clave, nombre in CATEGORIAS.items():
        print(f"  {nombre}: {resumen['categorias'].get(clave, 0)}")
    for corte, total in resumen["cortes"].items():
        print(f"  Corte {corte}: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
