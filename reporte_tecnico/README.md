# Reporte técnico — Procesamiento de entrevistas

**Fecha:** 2026-11-04
**Proyecto:** Mercado-de-Motos
**Alcance:** transcripción, detección de duplicados, clasificación e integración de los audios de `Entrevistas/`.

---

## 1. Resumen

- Se procesaron los **14 audios** de `Entrevistas/`: 2 del 23/10 y 12 del 28/10. El audio de `COMPRADOR_001` se transcribió de nuevo para verificar su ficha.
- Se consolidaron **3 entrevistas de compradores**: `COMPRADOR_001`, `COMPRADOR_002` y `COMPRADOR_003`.
- **No se identificaron** entrevistas a talleres ni a importadoras.
- Se detectaron **3 duplicados exactos** entre `data/raw/audios/` y `Entrevistas/`.
- Se corrigió una atribución: el texto de 11 respuestas aportado el 2026-11-03 pertenece a la sesión del 28/10 (`COMPRADOR_003`), no al audio `COMPRADOR_002.aac`.

---

## 2. Qué se hizo

1. Inventario de los 14 audios con tamaño, duración y SHA256.
2. Intento de transcripción con `faster-whisper`/`ctranslate2` (falló).
3. Instalación de `vosk` y del modelo `vosk-model-small-es-0.42` en un Python 3.12 portátil.
4. Transcripción de los 13 audios pendientes y verificación del audio de `COMPRADOR_001`.
5. Agrupación de las 12 notas del 28/10 como una sola sesión (`COMPRADOR_003`).
6. Normalización de respuestas claras en `docs/entrevistas/compradores.json`; lo no inteligible quedó en `null`.
7. Actualización de README, explicación del pipeline, reporte de unificación, journal y hand-off.
8. Validación del JSON, del dataset, de las pruebas y de la compilación.

En los campos normalizados solo se registran respuestas; las preguntas del entrevistador permanecen únicamente en la transcripción bruta.

---

## 3. Errores y soluciones

| Error | Detalle | Solución |
|---|---|---|
| `ctranslate2` access violation | `EXIT=-1073741819` al inferir con `faster-whisper`, en Python 3.14 y 3.12, con `int8` y `float32` | Se descartó `faster-whisper` y se usó Vosk |
| `pip install ctranslate2==4.0.0` | Falló con `PIP=1` | No se insistió; se cambió de motor |
| `pip install vosk` | Falló al construir `srt` porque faltaba `wheel` | Se instaló `wheel` y luego Vosk |
| Transcripción ruidosa | Vosk confunde palabras en audios de WhatsApp | Solo se registran respuestas claras; el resto queda en `null` y en `preguntas_pendientes` |

No se corrigió el habla ni se completaron respuestas por inferencia.

---

## 4. Duplicados detectados

| Copia en `data/raw/audios/` | Archivo original en `Entrevistas/` | SHA256 |
|---|---|---|
| `COMPRADOR_001.mp4` | `WhatsApp Audio 2026-10-23 at 11.57.00 PM.mp4` | `89420e2084fc1b81a170fb9754f39ec2d35790a4ac9e69e9e4d29a741b9f5087` |
| `COMPRADOR_002.aac` | `WhatsApp Audio 2026-10-23 at 10.32.41 PM.aac` | `fc213b25f64fceb81d7a296c876fe75bcb91019dc2c7b525cb1bda1d3bac8733` |
| `COMPRADOR_003.ogg` | `WhatsApp Audio 2026-10-28 at 2.46.59 PM.ogg` | `8cc7a9e46a15e1b0627c0e1acc0784086000b74fdb29aa9fc30b834582569412` |

- Dentro de `Entrevistas/` **no hay hashes repetidos**.
- Las 12 notas del 28/10 **no son duplicados**: son partes de una misma sesión (15 min 45,8 s en total).
- El texto de 11 respuestas coincide con el contenido de la sesión del 28/10, no con el audio `COMPRADOR_002.aac`.

---

## 5. Archivos modificados y creados

**Modificados:**

- `README.md`
- `explicacion_pipeline.md`
- `docs/entrevistas/compradores.json`
- `docs/entrevistas/README.md`
- `docs/entrevistas/talleres.json`
- `docs/entrevistas/importadoras.json`
- `docs/metodologia/REPORTE_UNIFICACION.md`
- `docs/journal/README.md`
- `docs/entregables/HANDOFF.md`
- `data/raw/entrevistas/comprador_002.md`

**Creados:**

- `data/raw/entrevistas/comprador_003.md`
- `data/raw/entrevistas/comprador_003_partes.md`
- `src/cualitativo/transcribir_vosk.py`
- `reporte_tecnico/README.md`

---

## 6. Validación

| Comprobación | Resultado |
|---|---|
| `json.load` de `docs/entrevistas/*.json` | OK (5 archivos) |
| `python src/verificar_datos.py` | OK (6.101 anuncios) |
| `pytest -q` | OK (2 passed) |
| `py_compile` de `src/cualitativo/` | OK |

---

## 7. Pendientes

1. Confirmar perfiles y voces de `COMPRADOR_002` y `COMPRADOR_003`.
2. Confirmar que el texto de 11 respuestas corresponde a las 12 notas del 28/10.
3. Conseguir entrevistas de talleres e importadoras.
4. Ejecutar un nuevo corte de Revolico cuando se quiera refrescar el dataset.
5. Autorizar y ejecutar el commit de esta fase.

---

## 8. Comandos principales

```powershell
# Entorno portátil con Vosk
python -m pip install wheel
python -m pip install vosk

# Transcripción combinada de las 12 partes del 28/10
python src/cualitativo/transcribir_vosk.py "..\Entrevistas\*.ogg" `
  --modelo "C:\ruta\a\vosk-model-small-es-0.42" `
  --salida data/raw/entrevistas/comprador_003_partes.md `
  --sobrescribir

# Validación
python -c "import json,pathlib; [json.loads(p.read_text(encoding='utf-8')) for p in pathlib.Path('docs/entrevistas').glob('*.json')]"
python src/verificar_datos.py
pytest -q
python -m py_compile src/cualitativo/transcribir_vosk.py
```
