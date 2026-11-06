# Reporte técnico — Procesamiento de entrevistas

**Fecha:** 2026-11-05 (actualizado)
**Proyecto:** Mercado-de-Motos
**Alcance:** inventario, transcripción, detección de duplicados, normalización e integración de los audios de `Entrevistas/` y de las entrevistas aportadas en texto.

> Esta es la copia publicada dentro del repositorio. El original se mantiene en `reporte_tecnico/README.md` (fuera del repositorio Git).

---

## 1. Resumen

- Se inventariaron **49 audios** en 29 carpetas de `Entrevistas/` (todos con hash único dentro de la fuente).
- Se integraron **38 audios** en `data/raw/audios/`, distribuidos en 27 carpetas de ID (27 con audio; `COMPRADOR_003` y `COMPRADOR_025` son texto sin audio).
- Los **11 audios restantes** corresponden a tomas antiguas ya consolidadas (4 de la carpeta 1, 1 de la carpeta 2, 1 de la carpeta 4 y 5 de la carpeta 3) y no se volvieron a copiar.
- Se normalizaron **30 entrevistas**: **25 compradores**, **4 talleres** y **1 importadora** (Solimport).
- Se detectó **1 duplicado nuevo**: un audio de la carpeta 19 es idéntico a `COMPRADOR_007` y se descartó.
- La transcripción automática se hizo con **Vosk** (`vosk-model-small-es-0.42`); `faster-whisper`/`ctranslate2` no funciona en este equipo.

---

## 2. Qué se hizo

1. Inventario de los audios con tamaño, duración y SHA256.
2. Copia de los audios válidos a `data/raw/audios/<ID>/`.
3. Transcripción con Vosk a `data/raw/entrevistas/<ID>.md`.
4. Detección de duplicados por hash (dentro de la fuente y contra el archivo ya procesado).
5. Normalización en `docs/entrevistas/compradores.json`, `talleres.json` e `importadoras.json`.
6. Registro de solo respuestas explícitas; lo no inteligible queda en `null` y en `preguntas_pendientes`.
7. Actualización de `README.md`, `explicacion_pipeline.md`, `docs/entrevistas/README.md`, `handoff/HANDOFF.md`, `journal/journal.md` y del análisis cualitativo.
8. Validación de JSON, dataset, pruebas y compilación.

En los campos normalizados solo se registran respuestas; las preguntas del entrevistador permanecen únicamente en la transcripción bruta.

---

## 3. Errores y soluciones

| Error | Detalle | Solución |
|---|---|---|
| `ctranslate2` access violation | `faster-whisper 1.2.1` + `ctranslate2 4.5.0`; `EXIT=-1073741819` al inferir con Python 3.14 (`.venv`) y 3.12 portátil | Se descartó `faster-whisper` y se usó Vosk |
| `pip install ctranslate2==4.0.0` | Falló con `PIP=1` | No se insistió; se cambió de motor |
| `pip install vosk` | Falló al construir `srt` porque faltaba `wheel` | Se instaló `wheel` y luego Vosk |
| Transcripción ruidosa | Vosk confunde palabras en audios de WhatsApp (p. ej. "Revolico" → "robo ligá") | Solo se registran respuestas claras; el resto queda en `null` y en `preguntas_pendientes` |
| Entrevistas en texto | `COMPRADOR_003` y `COMPRADOR_025` no tienen audio | Se registran como texto, con `transcripcion_automatica: false` y `audio_partes: []` |

No se corrigió el habla ni se completaron respuestas por inferencia.

---

## 4. Duplicados detectados

| Copia en `data/raw/audios/` | Archivo original en `Entrevistas/` | SHA256 |
|---|---|---|
| `COMPRADOR_001.mp4` | `WhatsApp Audio 2026-10-23 at 11.57.00 PM.mp4` | `89420e2084fc1b81a170fb9754f39ec2d35790a4ac9e69e9e4d29a741b9f5087` |
| `COMPRADOR_002.aac` | `WhatsApp Audio 2026-10-23 at 10.32.41 PM.aac` | `fc213b25f64fceb81d7a296c876fe75bcb91019dc2c7b525cb1bda1d3bac8733` |
| `COMPRADOR_003.ogg` | `WhatsApp Audio 2026-10-28 at 2.46.59 PM.ogg` | `8cc7a9e46a15e1b0627c0e1acc0784086000b74fdb29aa9fc30b834582569412` |
| `COMPRADOR_007/WhatsApp Ptt 2026-11-05 at 8.25.19 AM.ogg` | `Entrevista comprador 19/WhatsApp Ptt 2026-11-05 at 8.25.19 AM.ogg` | `824bd33ef00236b89af2c45ce404627a4e6ca7b76796bb0b911df24e4fe0733d` |

- Dentro de `Entrevistas/` no hay hashes repetidos.
- Las 12 notas del 28/10 no son duplicados: son partes de una misma sesión (`COMPRADOR_003`).
- El audio duplicado de la carpeta 19 se descartó y no se volvió a transcribir.

---

## 5. Entrevistas integradas

| Grupo | IDs | Cantidad | Audio |
|---|---|---|---|
| Compradores | `COMPRADOR_001` a `COMPRADOR_025` | 25 | 23 con audio; `003` y `025` en texto |
| Talleres | `TALLER_001` a `TALLER_004` | 4 | 4 con audio |
| Importadora | `IMPORTADORA_001` (Solimport) | 1 | 1 con audio |
| **Total** | — | **30** | — |

Fechas: 2 audios del 2026-10-23, 1 sesión del 2026-10-28 (texto), y el resto del 2026-11-04 y 2026-11-05.

---

## 6. Archivos modificados y creados

**Modificados:**

- `README.md`
- `explicacion_pipeline.md`
- `docs/entrevistas/compradores.json`
- `docs/entrevistas/talleres.json`
- `docs/entrevistas/importadoras.json`
- `docs/entrevistas/README.md`
- `docs/entrevistas/analisis_lote_2026-11-05.md`
- `handoff/HANDOFF.md`
- `journal/journal.md`
- `data/raw/entrevistas/comprador_002.md`

**Creados:**

- `data/raw/entrevistas/COMPRADOR_001.md` a `COMPRADOR_025.md` (según disponibilidad de audio o texto)
- `data/raw/entrevistas/TALLER_001.md` a `TALLER_004.md`
- `data/raw/entrevistas/IMPORTADORA_001.md`
- `src/cualitativo/transcribir_vosk.py`
- `codigo/analisis_entrevistas/normalizar_lote.py`
- `codigo/analisis_entrevistas/validar_entrevistas.py`
- `docs/entregables/reporte_tecnico.md`

---

## 7. Validación

| Comprobación | Resultado |
|---|---|
| `json.load` de `docs/entrevistas/*.json` | OK (3 archivos, 30 entrevistas) |
| `python src/verificar_datos.py` | OK (6.101 anuncios) |
| `pytest -q` | OK (2 passed) |
| `py_compile` de los scripts cualitativos | OK |
| `validar_entrevistas.py` | 30 entrevistas; solo errores preexistentes de `COMPRADOR_001`-`003` (texto) e `IMPORTADORA_001` (esquema propio) |

---

## 8. Pendientes

1. Confirmar perfiles, precios y moneda de los compradores con respuestas dudosas (ver `preguntas_pendientes`).
2. Confirmar que `TALLER_001` a `TALLER_004` son realmente talleres: la asignación proviene de la carpeta de origen.
3. Aclarar la pieza robada/dañada y el estado de las baterías en `COMPRADOR_023`, `024` y `025`.
4. Ejecutar un nuevo corte de Revolico cuando se quiera refrescar el dataset.

---

## 9. Comandos principales

```powershell
# Entorno con Vosk
python -m pip install wheel
python -m pip install vosk

# Transcripción de un audio a texto
python src/cualitativo/transcribir_vosk.py "data/raw/audios/COMPRADOR_024/WhatsApp Ptt 2026-11-05 at 4.30.57 PM.ogg" `
  --modelo "modelos/vosk-model-small-es-0.42" `
  --salida "data/raw/entrevistas/COMPRADOR_024.md"

# Normalización y validación
python codigo/analisis_entrevistas/normalizar_lote.py
python codigo/analisis_entrevistas/validar_entrevistas.py
python src/verificar_datos.py
pytest -q
```
