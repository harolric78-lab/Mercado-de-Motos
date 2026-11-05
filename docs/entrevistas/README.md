# Entrevistas y evidencia cualitativa

Este directorio unifica la evidencia cualitativa del proyecto en archivos JSON normalizados y reutilizables.

## Estado actual

El **2026-11-04** se reinició el registro de entrevistas: se eliminaron las entrevistas anteriores, sus transcripciones y sus audios para comenzar desde cero. Se incorporaron veinticuatro entrevistas de compradores, cuatro de talleres y una de importadora (Solimport).

| Tipo de fuente | Archivo | Entrevistas |
|---|---|---:|
| Compradores | [`compradores.json`](compradores.json) | 24 |
| Talleres | [`talleres.json`](talleres.json) | 4 |
| Importadoras | [`importadoras.json`](importadoras.json) | 1 |

Las entrevistas `COMPRADOR_001`, `COMPRADOR_002`, `COMPRADOR_004`, `COMPRADOR_005` y `COMPRADOR_006` (2026-11-04) reúnen los audios nuevos de las carpetas de compradores, transcritos con Vosk. `COMPRADOR_007` y `COMPRADOR_008` corresponden a las carpetas `Entrevista comprador 8` y `Entrevista comprador 9` (2026-11-05). `COMPRADOR_009` a `COMPRADOR_013` corresponden a las carpetas 10 a 14; `COMPRADOR_011` y `COMPRADOR_012` tienen audio del 2026-10-23. `COMPRADOR_014` a `COMPRADOR_016` corresponden a las carpetas 15 a 17; `COMPRADOR_014` tiene audio del 2026-11-04. `COMPRADOR_017` corresponde a la carpeta 18 y reúne cuatro audios del 2026-11-05; `COMPRADOR_018` a `COMPRADOR_024` corresponden a las carpetas 19 a 25. `COMPRADOR_003` se recuperó como texto, sin audio. `TALLER_001` a `TALLER_004` corresponden a las carpetas de taller 1 a 4 (2026-11-05). La entrevista `IMPORTADORA_001` corresponde a Solimport y también se transcribió con Vosk. Cada transcripción está en `data/raw/entrevistas/<ID>.md` y los audios en `data/raw/audios/<ID>/`. Se descartaron los audios y carpetas que duplicaban la sesión antigua.

El análisis cualitativo del lote más reciente está en [`analisis_lote_2026-11-05.md`](analisis_lote_2026-11-05.md).

## Propósito

Complementar el análisis cuantitativo de los anuncios de Revolico con información de campo que permita interpretar precios, preferencias, disponibilidad de repuestos y prácticas del mercado.

## Metodología de recopilación

- Entrevistas semiestructuradas realizadas en La Habana.
- Observación directa en talleres, tiendas e importadoras.
- Registro fotográfico de campo.
- Conversión de notas y transcripciones a un esquema JSON común.

Cada registro conserva el texto original cuando existe, para mantener la trazabilidad entre la fuente y el dato normalizado.

## Estructura de registro

- `texto_original`: respuesta literal o transcripción verbatim, sin corregir el habla.
- `perfil`, `compra`, `uso`, `repuestos`, `opiniones_mercado` y `satisfaccion`: campos normalizados según [`esquema.json`](esquema.json) y [`cuestionario.json`](cuestionario.json).
- `respuestas`: respuestas abiertas que no encajan en los bloques anteriores.
- `preguntas_pendientes`: datos que faltan y deben confirmarse en campo.
- `transcripcion_automatica` y `modelo_transcripcion`: trazabilidad del origen.
- `audio_sha256`: verificación de la fuente.

**Principio:** se registran solo las respuestas explícitas. Los campos sin respuesta quedan en `null` (o `[]` en listas) y se listan en `preguntas_pendientes`; no se infieren ni se completan con supuestos.

## Flujo para registrar una nueva entrevista

1. El investigador aporta las respuestas o el audio de la entrevista.
2. Se identifica el tipo de fuente (`comprador`, `taller` o `importadora`).
3. Se normaliza en `docs/entrevistas/<tipo>.json` con el identificador correspondiente (`COMPRADOR_001`, `TALLER_001`, `IMPORTADORA_001`).
4. Se guarda la transcripción en `data/raw/entrevistas/` y, si existe, el audio en `data/raw/audios/`.
5. Se actualiza `total_entrevistas` y la tabla de estado de este README.
6. Se valida con `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

## Categorías de análisis

- Precios y rangos de precios.
- Modelos y marcas con mayor demanda.
- Preferencias de compra.
- Disponibilidad de repuestos y mantenimiento.
- Diferencias entre motos de combustión y eléctricas.

## Limitaciones

- El número de entrevistas es todavía muy reducido y no es representativo del mercado.
- La evidencia cualitativa se usa para interpretar los datos cuantitativos, no para estimar volúmenes ni precios.
- No se fabrican ni completan respuestas: los campos sin información quedan vacíos y documentados.
