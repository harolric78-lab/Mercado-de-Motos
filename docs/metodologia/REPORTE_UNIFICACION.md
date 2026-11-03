# Reporte de unificación de evidencia cualitativa

**Fecha:** 2026-11-01
**Alcance:** unificación de entrevistas, observaciones y evidencia fotográfica del proyecto.

---

## 1. Entrevistas detectadas

| Tipo de fuente | Detectadas | Ubicación original |
|---|---:|---|
| Talleres | 0 | — |
| Importadoras | 0 | — |
| Compradores | 2 | `COMPRADOR_001` (JSON, 2026-11-01) y `COMPRADOR_002` (texto aportado, 2026-11-03) |

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
- **Fecha de registro:** 2026-11-03 (fecha del audio por confirmar)
- **Ubicación:** La Habana, Cuba (por confirmar)
- **Entrevistado:** comprador anónimo
- **Origen:** texto aportado por el investigador a partir de un audio.
- **Clasificación:** comprador.
- **Nota:** la transcripción automática con `faster-whisper` no pudo ejecutarse (`ctranslate2` falla con Python 3.14); la correspondencia texto-audio está pendiente de verificar.

## 2. Entrevistas migradas

| Archivo de destino | Registros | Estado |
|---|---:|---|
| `docs/entrevistas/talleres.json` | 0 | Estructura vacía documentada |
| `docs/entrevistas/importadoras.json` | 0 | Estructura vacía documentada |
| `docs/entrevistas/compradores.json` | 2 | `COMPRADOR_001` (transcripción + audio) y `COMPRADOR_002` (texto aportado) |

No se fabricaron entrevistas ni respuestas. Los campos sin información quedaron vacíos y la ausencia se documentó en cada archivo y en `docs/entrevistas/README.md`.

## 3. Archivos convertidos a JSON

| Origen | Destino | Formato |
|---|---|---|
| JSON `comprador_001` | `docs/entrevistas/compradores.json` | JSON → JSON normalizado |
| Transcripción `comprador_001` | `data/raw/entrevistas/comprador_001.md` | Texto → Markdown |
| Texto `COMPRADOR_002` | `docs/entrevistas/compradores.json` | Texto → JSON normalizado |
| Texto `COMPRADOR_002` | `data/raw/entrevistas/comprador_002.md` | Texto → Markdown |

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
- La correspondencia entre el texto de `COMPRADOR_002` y `data/raw/audios/COMPRADOR_002.aac` está pendiente de verificar.
- El audio `COMPRADOR_003.ogg` sigue pendiente de transcripción y clasificación.

## 7. Validación

- JSON de `docs/entrevistas/` validado sintácticamente.
- Estructura de carpetas verificada.
- `python src/verificar_datos.py` ejecutado sin errores.
- `pytest -q` ejecutado sin errores.
