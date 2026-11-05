#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcribe audios de entrevistas con Vosk, en local.

Requiere `vosk`, `av` y un modelo de Vosk (por ejemplo `vosk-model-small-es-0.42`).
No corrige el habla: la transcripción se marca como automática.

Uso:
    python src/cualitativo/transcribir_vosk.py audio.ogg --modelo C:\\modelos\\vosk-model-small-es-0.42
    python src/cualitativo/transcribir_vosk.py Entrevistas/ --modelo C:\\modelos\\vosk-model-small-es-0.42 --salida data/raw/entrevistas/comprador_003_partes.md
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import av
from av.audio.resampler import AudioResampler
from vosk import KaldiRecognizer, Model, SetLogLevel

BASE = Path(__file__).resolve().parents[2]
TRANSCRIPCIONES = BASE / "data" / "raw" / "entrevistas"
EXTENSIONES = {".mp3", ".mp4", ".m4a", ".aac", ".ogg", ".opus", ".wav", ".flac", ".webm"}


def sha256(ruta: Path) -> str:
    digest = hashlib.sha256()
    with ruta.open("rb") as handle:
        for bloque in iter(lambda: handle.read(1 << 20), b""):
            digest.update(bloque)
    return digest.hexdigest()


def recolectar(entradas: list[str]) -> list[Path]:
    rutas: list[Path] = []
    for entrada in entradas:
        if any(caracter in entrada for caracter in "*?["):
            rutas.extend(
                sorted(
                    Path(p)
                    for p in glob.glob(entrada)
                    if Path(p).is_file() and Path(p).suffix.lower() in EXTENSIONES
                )
            )
            continue
        ruta = Path(entrada).expanduser()
        if ruta.is_dir():
            rutas.extend(sorted(p for p in ruta.iterdir() if p.suffix.lower() in EXTENSIONES))
        elif ruta.is_file():
            rutas.append(ruta)
        else:
            print(f"Omitido (no existe): {ruta}", file=sys.stderr)
    return rutas


def decodificar(ruta: Path) -> bytes:
    with av.open(str(ruta)) as contenedor:
        remuestreador = AudioResampler(format="s16", layout="mono", rate=16000)
        bloques: list[bytes] = []
        for frame in contenedor.decode(audio=0):
            for salida in remuestreador.resample(frame):
                bloques.append(salida.to_ndarray().tobytes())
        cola = remuestreador.resample(None)
        if cola:
            for salida in cola:
                bloques.append(salida.to_ndarray().tobytes())
    return b"".join(bloques)


def transcribir(ruta: Path, modelo: Model) -> dict:
    pcm = decodificar(ruta)
    reconocedor = KaldiRecognizer(modelo, 16000)
    partes: list[str] = []
    paso = 32000
    for inicio in range(0, len(pcm), paso):
        if reconocedor.AcceptWaveform(pcm[inicio : inicio + paso]):
            partes.append(json.loads(reconocedor.Result()).get("text", ""))
    partes.append(json.loads(reconocedor.FinalResult()).get("text", ""))
    return {
        "duracion_segundos": round(len(pcm) / 32000, 1),
        "texto": " ".join(p for p in partes if p).strip(),
    }


def bloque_md(ruta: Path, resultado: dict, modelo_nombre: str) -> list[str]:
    return [
        f"## {ruta.name}",
        "",
        f"- **SHA256:** `{sha256(ruta)}`",
        f"- **Duración:** {resultado['duracion_segundos']:.1f} s",
        f"- **Modelo:** Vosk `{modelo_nombre}`",
        "- **Aviso:** transcripción automática, sin revisión manual. No se corrige el habla.",
        "",
        resultado["texto"],
        "",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audios de entrevistas con Vosk.")
    parser.add_argument("entradas", nargs="+", help="Archivos o carpetas de audio.")
    parser.add_argument("--modelo", default=os.environ.get("VOSK_MODELO"), help="Ruta al modelo de Vosk.")
    parser.add_argument("--salida", help="Archivo Markdown combinado. Si se omite, escribe un .md por audio.")
    parser.add_argument("--sobrescribir", action="store_true")
    args = parser.parse_args()

    if not args.modelo:
        print("Indica --modelo o define VOSK_MODELO.", file=sys.stderr)
        return 1
    rutas = recolectar(args.entradas)
    if not rutas:
        print("No se encontraron audios.", file=sys.stderr)
        return 1

    SetLogLevel(-1)
    modelo = Model(args.modelo)
    modelo_nombre = Path(args.modelo).name
    TRANSCRIPCIONES.mkdir(parents=True, exist_ok=True)

    if args.salida:
        destino = Path(args.salida)
        if destino.exists() and not args.sobrescribir:
            print(f"{destino} ya existe. Usa --sobrescribir.", file=sys.stderr)
            return 1
        lineas = [
            "# Transcripciones automáticas — Vosk",
            "",
            f"- **Modelo:** `{modelo_nombre}`",
            f"- **Generado:** {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
            "",
        ]
        resumen = []
        for ruta in rutas:
            print(f"Transcribiendo {ruta.name}…")
            resultado = transcribir(ruta, modelo)
            lineas.extend(bloque_md(ruta, resultado, modelo_nombre))
            resumen.append({"audio": ruta.name, **resultado})
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(lineas), encoding="utf-8")
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
        return 0

    resumen = []
    for ruta in rutas:
        destino = TRANSCRIPCIONES / f"{ruta.stem}.md"
        if destino.exists() and not args.sobrescribir:
            print(f"{destino.name} ya existe; se omite.", file=sys.stderr)
            continue
        print(f"Transcribiendo {ruta.name}…")
        resultado = transcribir(ruta, modelo)
        encabezado = [
            f"# Entrevista {ruta.stem}",
            "",
            f"- **Audio:** `{ruta}`",
            f"- **SHA256:** `{sha256(ruta)}`",
            f"- **Duración:** {resultado['duracion_segundos']:.1f} s",
            f"- **Modelo:** Vosk `{modelo_nombre}`",
            f"- **Generado:** {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
            "- **Aviso:** transcripción automática, sin revisión manual. No se corrige el habla.",
            "",
            "## Transcripción",
            "",
            resultado["texto"],
            "",
        ]
        destino.write_text("\n".join(encabezado), encoding="utf-8")
        resumen.append({"audio": ruta.name, "transcripcion": str(destino), **resultado})
        print(f"  → {destino}")
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
