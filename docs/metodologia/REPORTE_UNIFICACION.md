# Reporte de unificación de evidencia cualitativa

**Fecha:** 2026-11-01
**Alcance:** unificación de entrevistas, observaciones y evidencia fotográfica del proyecto.

---

## 1. Entrevistas detectadas

| Tipo de fuente | Detectadas | Ubicación original |
|---|---:|---|
| Talleres | 0 | — |
| Importadoras | 0 | — |
| Compradores | 3 | `COMPRADOR_001` (JSON, 2026-11-01), `COMPRADOR_002` (audio transcrito, 2026-10-23) y `COMPRADOR_003` (12 notas de voz, 2026-10-28) |

Detalle de las entrevistas detectadas:

- **Identificador:** `TALLER_001`
- **Estado:** eliminada del dataset.
- **Motivo:** registro recuperado del historial de Git que no identificaba entrevistado, cargo ni establecimiento; su clasificación como taller era tentativa.

- **Identificador:** `COMPRADOR_001`
- **Fecha:** 2026-10-17
- **Ubicación:** San Miguel del Padrón, La Habana, Cuba
- **Entrevistado:** comprador anónimo (chófer profesional, 60 años)
- **Origen:** JSON, transcripción y audio aportados el 2026-11-01.
- **Clasificación:** comprador.

- **Identificador:** `COMPRADOR_002`
- **Fecha del audio:** 2026-10-23
- **Ubicación:** La Habana, Cuba (por confirmar)
- **Entrevistado:** comprador anónimo
- **Origen:** audio `WhatsApp Audio 2026-10-23 at 10.32.41 PM.aac`, transcrito automáticamente con Vosk.
- **Clasificación:** comprador.
- **Nota:** el texto de 11 respuestas aportado el 2026-11-03 se reasignó a `COMPRADOR_003`; no pertenecía a este audio.

- **Identificador:** `COMPRADOR_003`
- **Fecha:** 2026-10-28
- **Ubicación:** La Habana, Cuba (por confirmar)
- **Entrevistado:** comprador anónimo (una o varias voces por confirmar)
- **Origen:** 12 notas de voz de WhatsApp y texto de 11 respuestas aportado por el investigador.
- **Clasificación:** comprador.
- **Nota:** la primera parte está duplicada en `data/raw/audios/COMPRADOR_003.ogg`; las transcripciones están en `data/raw/entrevistas/comprador_003.md` y `comprador_003_partes.md`.

## 2. Entrevistas migradas

| Archivo de destino | Registros | Estado |
|---|---:|---|
| `docs/entrevistas/talleres.json` | 0 | Estructura vacía documentada |
| `docs/entrevistas/importadoras.json` | 0 | Estructura vacía documentada |
| `docs/entrevistas/compradores.json` | 3 | `COMPRADOR_001`, `COMPRADOR_002` y `COMPRADOR_003` (transcripciones y audios) |

No se fabricaron entrevistas ni respuestas. Los campos sin información quedaron vacíos y la ausencia se documentó en cada archivo y en `docs/entrevistas/README.md`.

## 3. Archivos convertidos a JSON

| Origen | Destino | Formato |
|---|---|---|
| JSON `comprador_001` | `docs/entrevistas/compradores.json` | JSON → JSON normalizado |
| Transcripción `comprador_001` | `data/raw/entrevistas/comprador_001.md` | Texto → Markdown |
| Audio `COMPRADOR_002` | `data/raw/entrevistas/comprador_002.md` | Audio → Markdown (Vosk) |
| Audio `COMPRADOR_003` | `data/raw/entrevistas/comprador_003.md` | Texto y audio → Markdown |
| 12 partes `COMPRADOR_003` | `data/raw/entrevistas/comprador_003_partes.md` | Audio → Markdown (Vosk) |

Se conservó el campo `texto_original` para mantener la trazabilidad entre la fuente y el registro normalizado.

## 4. Imágenes reorganizadas

| Origen | Destino | Archivos |
|---|---|---:|
| `docs/images/Importadora de motos/` | `docs/images/importadoras/` | 4 |
| `docs/images/Tiendas de motos electricas y de combustion/` | `docs/images/tiendas/` | 3 |
| — | `docs/images/talleres/` | 0 (creada vacía con `.gitkeep`) |

Total de imágenes reorganizadas: **7**. Todas con metadatos EXIF del 2026-10-08.

## 5. Documentación generada

| Archivo | Contenido |
|---|---|
| `docs/entrevistas/README.md` | Propósito, metodología, conteo, categorías y limitaciones |
| `docs/images/evidencia_campo.md` | Origen, organización, propósito y relación con entrevistas y hallazgos |
| `docs/metodologia/REPORTE_UNIFICACION.md` | Este reporte |

Además, se actualizó el `README.md` principal con la sección **Fuentes Cualitativas** y el árbol de estructura.

## 6. Ausencias documentadas

- No existen entrevistas a importadoras.
- No existen fotografías de talleres.
- El catálogo VEDCA detectado en el historial (`datos/importadora_vedca/vedca_catalogo_20261026_100817.json`) es un listado de productos, no una entrevista, por lo que no se migró.
- No existen entrevistas a talleres.
- La transcripción de `COMPRADOR_001` está en `data/raw/entrevistas/comprador_001.md` y su audio en `data/raw/audios/COMPRADOR_001.mp4`.
- La correspondencia texto-audio de `COMPRADOR_002` se verificó: el texto de 11 respuestas no pertenecía a ese audio y se reasignó a `COMPRADOR_003`.
- El audio `COMPRADOR_003.ogg` y las 12 partes del 2026-10-28 se transcribieron y clasificaron como comprador.
- Los 14 audios de `Entrevistas/` se procesaron; no se identificaron entrevistas a talleres o importadoras.

## 7. Validación

- JSON de `docs/entrevistas/` validado sintácticamente.
- Estructura de carpetas verificada.
- `python src/verificar_datos.py` ejecutado sin errores.
- `pytest -q` ejecutado sin errores.

---

## 8. Actualización 2026-11-04

- Se transcribieron los 14 audios de `Entrevistas/` con `vosk-model-small-es-0.42` (Python 3.12 portátil), tras descartar `faster-whisper`/`ctranslate2` por el fallo de acceso (`EXIT=-1073741819`).
- Se detectaron 3 duplicados exactos: los audios `COMPRADOR_001.mp4`, `COMPRADOR_002.aac` y `COMPRADOR_003.ogg` de `data/raw/audios/` son copias de archivos de `Entrevistas/`.
- Se corrigió la atribución del texto de 11 respuestas: pertenece a la sesión del 2026-10-28 (`COMPRADOR_003`), no al audio `COMPRADOR_002.aac`.
- Estado actual: 3 entrevistas de compradores y 14 audios procesados. Talleres e importadoras siguen sin entrevistas.
- Validación: `json.load`, `python src/verificar_datos.py`, `pytest -q` y `py_compile` (ver resultados en el journal).
