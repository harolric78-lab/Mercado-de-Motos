#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcribe audios de entrevistas con faster-whisper, en local.

Copia el audio a `data/raw/audios/<ID>.<ext>` y escribe:
  - `data/raw/entrevistas/<ID>.md` con la transcripción verbatim.
  - `data/raw/entrevistas/<ID>.transcripcion.json` con segmentos, tiempos y metadatos.

La transcripción es automática: se marca como tal y no se corrige el habla.

Uso:
    .venv\\Scripts\\python.exe src/cualitativo/transcribir.py "audio.m4a" --id ENTREVISTA_001
    .venv\\Scripts\\python.exe src/cualitativo/transcribir.py directorio/ --modelo small --idioma es
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
AUDIOS = BASE / "data" / "raw" / "audios"
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
        ruta = Path(entrada).expanduser()
        if ruta.is_dir():
            rutas.extend(sorted(p for p in ruta.iterdir() if p.suffix.lower() in EXTENSIONES))
        elif ruta.is_file():
            rutas.append(ruta)
        else:
            print(f"Omitido (no existe): {ruta}", file=sys.stderr)
    return rutas


def transcribir(ruta: Path, modelo: str, idioma: str) -> dict:
    from faster_whisper import WhisperModel

    motor = WhisperModel(modelo, device="cpu", compute_type="int8")
    segmentos, info = motor.transcribe(
        str(ruta),
        language=idioma,
        vad_filter=True,
        beam_size=5,
    )
    salida = []
    for segmento in segmentos:
        salida.append({
            "inicio": round(segmento.start, 2),
            "fin": round(segmento.end, 2),
            "texto": segmento.text.strip(),
        })
    return {
        "duracion_segundos": round(info.duration, 2),
        "idioma": info.language,
        "probabilidad_idioma": round(info.language_probability, 4),
        "segmentos": salida,
        "texto": " ".join(s["texto"] for s in salida).strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audios de entrevistas en local.")
    parser.add_argument("entradas", nargs="+", help="Archivos o carpetas de audio.")
    parser.add_argument("--id", dest="identificador", help="Identificador de la entrevista (ej. ENTREVISTA_001).")
    parser.add_argument("--modelo", default="small", help="Tamaño del modelo faster-whisper (tiny, base, small, medium, large-v3).")
    parser.add_argument("--idioma", default="es")
    parser.add_argument("--sobrescribir", action="store_true")
    args = parser.parse_args()

    rutas = recolectar(args.entradas)
    if not rutas:
        print("No se encontraron audios.", file=sys.stderr)
        return 1
    if args.identificador and len(rutas) > 1:
        print("--id solo admite un audio. Transcribe uno por uno.", file=sys.stderr)
        return 1

    AUDIOS.mkdir(parents=True, exist_ok=True)
    TRANSCRIPCIONES.mkdir(parents=True, exist_ok=True)
    resumen = []

    for ruta in rutas:
        identificador = args.identificador or ruta.stem.replace(" ", "_").upper()
        destino_audio = AUDIOS / f"{identificador}{ruta.suffix.lower()}"
        if ruta.resolve() != destino_audio.resolve():
            if destino_audio.exists() and not args.sobrescribir:
                print(f"Audio ya presente, se reutiliza: {destino_audio.name}")
            else:
                shutil.copy2(ruta, destino_audio)

        marca = sha256(destino_audio)
        print(f"Transcribiendo {destino_audio.name} ({marca[:12]}…) con modelo {args.modelo}…")

        resultado = transcribir(destino_audio, args.modelo, args.idioma)

        md = TRANSCRIPCIONES / f"{identificador}.md"
        escribir_md = not md.exists() or args.sobrescribir
        if not escribir_md:
            print(f"{md.name} ya existe; se conserva el registro manual y solo se genera el sidecar.", file=sys.stderr)

        if escribir_md:
            encabezado = [
                f"# Entrevista {identificador}",
                "",
                f"- **Audio:** `data/raw/audios/{destino_audio.name}`",
                f"- **SHA256:** `{marca}`",
                f"- **Duración:** {resultado['duracion_segundos']:.1f} s",
                f"- **Idioma detectado:** {resultado['idioma']} ({resultado['probabilidad_idioma']:.2f})",
                f"- **Modelo:** faster-whisper `{args.modelo}` (CPU, int8)",
                f"- **Generado:** {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
                "- **Aviso:** transcripción automática, sin revisión manual. No se corrige el habla.",
                "",
                "## Transcripción",
                "",
                resultado["texto"],
                "",
            ]
            md.write_text("\n".join(encabezado), encoding="utf-8")

        sidecar = TRANSCRIPCIONES / f"{identificador}.transcripcion.json"
        sidecar.write_text(
            json.dumps({
                "id": identificador,
                "audio": f"data/raw/audios/{destino_audio.name}",
                "audio_sha256": marca,
                "modelo": args.modelo,
                "generado": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "transcripcion_automatica": True,
                **resultado,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        resumen.append({
            "id": identificador,
            "audio": destino_audio.name,
            "sha256": marca,
            "duracion": resultado["duracion_segundos"],
            "palabras": len(resultado["texto"].split()),
            "transcripcion": str(md.relative_to(BASE)),
        })
        print(f"  → {md.relative_to(BASE)}")
        print(f"  → {sidecar.relative_to(BASE)}")

    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
