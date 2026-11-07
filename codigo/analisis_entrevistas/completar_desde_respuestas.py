# -*- coding: utf-8 -*-
"""Completa campos estructurados solo cuando la respuesta transcrita es explicita.

Regla del proyecto: no se inventan datos. Este script no deduce ni estima:
solo copia a los bloques estructurados valores que ya estan escritos en
``respuestas`` o en el perfil declarado por el entrevistado.

Uso:
    python codigo/analisis_entrevistas/completar_desde_respuestas.py
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ENT = BASE / "docs" / "entrevistas"

# id -> {bloque: {campo: valor}}
# Cada valor debe estar sustentado por el texto de ``respuestas`` del propio
# registro o por una frase explicita del entrevistado. No hay inferencias.
COMPLETAR = {
    "COMPRADOR_006": {
        "compra": {
            "precio_final": 2800,
            "moneda": "USD",
            "canal_busqueda": "Conocido importador",
        },
        "opiniones_mercado": {
            "autonomia_electrica_km": "80 km anunciados / ~70 km reales",
        },
    },
    "COMPRADOR_007": {
        "compra": {"canal_busqueda": "Importador (por confirmar)"},
    },
    "COMPRADOR_008": {
        "compra": {"canal_busqueda": "Importador / empresa familiar (por confirmar)"},
    },
    "COMPRADOR_010": {
        "compra": {
            "tipo_moto": "Eléctrica",
            "canal_busqueda": "Facebook (dueño anterior)",
        },
    },
    "COMPRADOR_011": {
        "perfil": {"sexo": "Masculino", "provincia": "La Habana"},
        "compra": {"canal_busqueda": "Conocido"},
        "uso": {
            "km_diarios": 40,
            "unico_medio_transporte": True,
            "tiene_alarma_candado": False,
        },
    },
    "COMPRADOR_013": {
        "uso": {"uso_principal": "Trabajo y transporte"},
    },
    "COMPRADOR_014": {
        "opiniones_mercado": {
            "autonomia_electrica_km": "80-100 km anunciados / 50-69 km reales",
        },
    },
    "COMPRADOR_016": {
        "compra": {
            "tipo_moto": "Eléctrica",
            "canal_busqueda": "Importadora",
        },
        "uso": {"uso_principal": "Trabajo (trabajitos)"},
    },
    "COMPRADOR_017": {
        "opiniones_mercado": {
            "autonomia_electrica_km": "~75 km (real/anunciada por confirmar)",
        },
    },
    "COMPRADOR_018": {
        "compra": {"precio_final": "~2.000 (moneda por confirmar)"},
    },
    "COMPRADOR_020": {
        "uso": {"uso_principal": "Personal / salidas"},
    },
    "COMPRADOR_022": {
        "uso": {"uso_principal": "Trabajo"},
    },
    "COMPRADOR_023": {
        "compra": {"canal_busqueda": "Importación (Panamá)"},
        "uso": {"uso_principal": "Trabajo"},
    },
    "COMPRADOR_024": {
        "perfil": {"ocupacion": "Comercializa productos (por confirmar)"},
        "uso": {"uso_principal": "Trabajo"},
    },
}


def esta_vacio(valor: object) -> bool:
    return valor in (None, "", [])


def main() -> int:
    archivos = {
        "compradores.json": "COMPRADOR",
        "talleres.json": "TALLER",
        "importadoras.json": "IMPORTADORA",
    }
    cambios = 0
    for nombre, prefijo in archivos.items():
        ruta = ENT / nombre
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        for entrevista in datos["entrevistas"]:
            eid = entrevista["id"]
            if eid not in COMPLETAR:
                continue
            for bloque, campos in COMPLETAR[eid].items():
                for campo, valor in campos.items():
                    actual = entrevista.get(bloque, {}).get(campo)
                    if esta_vacio(actual):
                        entrevista[bloque][campo] = valor
                        print(f"{eid}: {bloque}.{campo} = {valor!r}")
                        cambios += 1
                    else:
                        print(f"{eid}: {bloque}.{campo} ya tenia {actual!r} (sin cambios)")
        ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Campos completados: {cambios}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
