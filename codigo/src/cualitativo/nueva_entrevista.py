#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captura asistida de entrevistas semiestructuradas.

Lee `docs/entrevistas/cuestionario.json`, pregunta bloque por bloque y escribe:
  - `docs/entrevistas/<tipo>.json` con la entrevista normalizada.
  - `data/raw/entrevistas/<ID>.md` con el registro literal de preguntas y respuestas.

Los campos sin respuesta se guardan en `null` o cadena vacia. No se infiere nada.

Uso:
    python src/cualitativo/nueva_entrevista.py --tipo comprador
    python src/cualitativo/nueva_entrevista.py --tipo taller --id TALLER_002
    python src/cualitativo/nueva_entrevista.py --exportar-cuestionario
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DOCS = BASE / "docs" / "entrevistas"
RAW = BASE / "data" / "raw" / "entrevistas"
CUESTIONARIO = DOCS / "cuestionario.json"

TIPOS = {
    "comprador": {"archivo": "compradores.json", "prefijo": "COMPRADOR", "tipo_fuente": "compradores"},
    "usuario": {"archivo": "compradores.json", "prefijo": "COMPRADOR", "tipo_fuente": "compradores"},
    "taller": {"archivo": "talleres.json", "prefijo": "TALLER", "tipo_fuente": "talleres"},
    "importadora": {"archivo": "importadoras.json", "prefijo": "IMPORTADORA", "tipo_fuente": "importadoras"},
}


def cargar_cuestionario() -> dict:
    return json.loads(CUESTIONARIO.read_text(encoding="utf-8"))


def exportar_csv(destino: Path | None = None) -> Path:
    """Exporta el cuestionario a CSV legible para trabajo de campo."""
    cuestionario = cargar_cuestionario()
    destino = destino or DOCS / "cuestionario.csv"
    filas = []
    for bloque in cuestionario["bloques"]:
        for pregunta in bloque["preguntas"]:
            filas.append({
                "bloque": bloque["id"],
                "campo": pregunta["campo"],
                "pregunta": pregunta["pregunta"],
                "tipo": pregunta["tipo"],
                "opciones": " | ".join(pregunta.get("opciones", [])),
                "obligatorio": "si" if pregunta.get("obligatorio") else "no",
            })
    with destino.open("w", encoding="utf-8", newline="") as handle:
        escritor = csv.DictWriter(handle, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    return destino


def siguiente_id(prefijo: str, existentes: list[dict]) -> str:
    numeros = [
        int(e["id"].split("_")[1])
        for e in existentes
        if isinstance(e.get("id"), str) and e["id"].startswith(f"{prefijo}_")
    ]
    return f"{prefijo}_{(max(numeros) if numeros else 0) + 1:03d}"


def preguntar_texto(pregunta: str, defecto: str | None = None) -> str:
    sufijo = f" [{defecto}]" if defecto else ""
    valor = input(f"{pregunta}{sufijo}: ").strip()
    if not valor:
        return defecto or ""
    return valor


def preguntar_tipo(pregunta: dict) -> object:
    tipo = pregunta["tipo"]
    texto = pregunta["pregunta"]
    opciones = pregunta.get("opciones")

    if tipo == "booleano":
        respuesta = input(f"{texto} (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí", "y", "yes"):
            return True
        if respuesta in ("n", "no"):
            return False
        return None

    if tipo == "opcion" and opciones:
        print(f"{texto}")
        for i, opcion in enumerate(opciones, 1):
            print(f"  {i}. {opcion}")
        respuesta = input("> ").strip()
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            return opciones[int(respuesta) - 1]
        return respuesta or None

    if tipo == "lista" and opciones:
        print(f"{texto}")
        print(f"  Opciones: {', '.join(opciones)}")
        respuesta = input("> ").strip()
        if not respuesta:
            return []
        return [parte.strip() for parte in respuesta.replace(";", ",").split(",") if parte.strip()]

    if tipo == "entero":
        respuesta = input(f"{texto}: ").strip()
        try:
            return int(respuesta) if respuesta else None
        except ValueError:
            return respuesta

    if tipo == "decimal":
        respuesta = input(f"{texto}: ").strip().replace(",", ".")
        try:
            return float(respuesta) if respuesta else None
        except ValueError:
            return respuesta

    return preguntar_texto(texto, pregunta.get("defecto")) or None


def fijar(registro: dict, campo: str, valor) -> None:
    partes = campo.split(".")
    actual = registro
    for parte in partes[:-1]:
        actual = actual.setdefault(parte, {})
    actual[partes[-1]] = valor


def construir_markdown(entrevista: dict, bloques: list[dict], respuestas_literales: list[tuple[str, object]]) -> str:
    lineas = [
        f"# Entrevista {entrevista['id']}",
        "",
        f"- **Fecha:** {entrevista['fecha']}",
        f"- **Lugar:** {entrevista['ubicacion']}",
        f"- **Entrevistado:** {entrevista['entrevistado'] or '—'}",
        f"- **Cargo:** {entrevista['cargo'] or '—'}",
        f"- **Consentimiento:** {'sí' if entrevista['consentimiento'] else 'no consta'}",
        f"- **Fuente:** captura asistida (`src/cualitativo/nueva_entrevista.py`)",
        "",
        "## Registro de preguntas y respuestas",
        "",
    ]
    bloque_actual = None
    for campo, pregunta, valor in respuestas_literales:
        bloque = campo.split(".")[0]
        if bloque != bloque_actual:
            bloque_actual = bloque
            titulo = next((b["titulo"] for b in bloques if b["id"] == bloque), bloque)
            lineas += ["", f"### {titulo}", ""]
        lineas.append(f"- **{pregunta}**")
        lineas.append(f"  - {formatear(valor)}")
    return "\n".join(lineas) + "\n"


def formatear(valor) -> str:
    if valor is None or valor == "" or valor == []:
        return "_(sin respuesta)_"
    if valor is True:
        return "Sí"
    if valor is False:
        return "No"
    if isinstance(valor, list):
        return ", ".join(str(v) for v in valor)
    return str(valor)


def main() -> int:
    parser = argparse.ArgumentParser(description="Captura una entrevista semiestructurada.")
    parser.add_argument("--tipo", choices=list(TIPOS), help="Tipo de fuente de la entrevista.")
    parser.add_argument("--id", dest="identificador", help="Identificador explícito (ej. COMPRADOR_002).")
    parser.add_argument("--fecha", help="Fecha en formato AAAA-MM-DD.")
    parser.add_argument("--ubicacion", default="La Habana, Cuba")
    parser.add_argument("--entrevistado", default="")
    parser.add_argument("--cargo", default="")
    parser.add_argument("--exportar-cuestionario", action="store_true", help="Regenera docs/entrevistas/cuestionario.csv y sale.")
    args = parser.parse_args()

    if args.exportar_cuestionario:
        ruta = exportar_csv()
        print(f"Cuestionario: {ruta}")
        return 0

    if not args.tipo:
        parser.error("--tipo es obligatorio salvo con --exportar-cuestionario")

    config = TIPOS[args.tipo]
    archivo = DOCS / config["archivo"]
    payload = json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else {
        "tipo_fuente": config["tipo_fuente"],
        "entrevistas": [],
    }
    existentes = payload.get("entrevistas", [])

    identificador = args.identificador or siguiente_id(config["prefijo"], existentes)
    fecha = args.fecha or input("Fecha (AAAA-MM-DD): ").strip()
    cuestionario = cargar_cuestionario()

    print(f"\nEntrevista {identificador}")
    consentimiento = preguntar_tipo(cuestionario["consentimiento"])

    registro: dict = {
        "id": identificador,
        "fecha": fecha,
        "ubicacion": args.ubicacion,
        "entrevistado": args.entrevistado,
        "cargo": args.cargo,
        "consentimiento": consentimiento,
        "temas": [],
    }
    respuestas_literales: list[tuple[str, str, object]] = []

    for bloque in cuestionario["bloques"]:
        print(f"\n--- {bloque['titulo']} ---")
        registro[bloque["destino"]] = {}
        for pregunta in bloque["preguntas"]:
            valor = preguntar_tipo(pregunta)
            fijar(registro, pregunta["campo"], valor)
            respuestas_literales.append((pregunta["campo"], pregunta["pregunta"], valor))
        if any(registro[bloque["destino"]].values()):
            registro["temas"].append(bloque["id"])

    print("\n--- Cierre ---")
    observaciones = input("Observaciones de campo (opcional): ").strip()

    transcripcion = f"data/raw/entrevistas/{identificador}.md"
    registro.update({
        "preguntas_pendientes": [],
        "observaciones": observaciones,
        "transcripcion": transcripcion,
        "audio": "",
        "audio_sha256": None,
        "texto_original": "",
        "transcripcion_automatica": False,
        "modelo_transcripcion": None,
    })

    RAW.mkdir(parents=True, exist_ok=True)
    (BASE / transcripcion).write_text(
        construir_markdown(registro, cuestionario["bloques"], respuestas_literales),
        encoding="utf-8",
    )

    existentes.append(registro)
    payload["entrevistas"] = existentes
    payload["total_entrevistas"] = len(existentes)
    archivo.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nGuardado: {archivo}")
    print(f"Transcripción: {BASE / transcripcion}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
