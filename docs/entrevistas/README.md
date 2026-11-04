# Entrevistas y evidencia cualitativa

Este directorio unifica la evidencia cualitativa del proyecto en archivos JSON normalizados y reutilizables.

## Propósito

Complementar el análisis cuantitativo de los anuncios de Revolico con información de campo que permita interpretar precios, preferencias, disponibilidad de repuestos y prácticas del mercado.

## Metodología de recopilación

- Entrevistas semiestructuradas realizadas en La Habana.
- Observación directa en talleres, tiendas e importadoras.
- Registro fotográfico de campo.
- Conversión de notas y transcripciones dispersas a un esquema JSON común.

Cada registro conserva el texto original cuando existe, para mantener la trazabilidad entre la fuente y el dato normalizado.

## Entrevistas encontradas

| Tipo de fuente | Archivo | Entrevistas reales | Estado |
|---|---|---:|---|
| Talleres | [`talleres.json`](talleres.json) | 0 | Estructura vacía documentada |
| Importadoras | [`importadoras.json`](importadoras.json) | 0 | Estructura vacía documentada |
| Compradores | [`compradores.json`](compradores.json) | 3 | `COMPRADOR_001` (2026-10-17), `COMPRADOR_002` (2026-10-23) y `COMPRADOR_003` (2026-10-28) |

La entrevista `COMPRADOR_001`, fechada el 2026-10-17, corresponde a un comprador de San Miguel del Padrón y cuenta con transcripción en `data/raw/entrevistas/comprador_001.md` y audio en `data/raw/audios/COMPRADOR_001.mp4`. Se eliminó el registro `TALLER_001`, recuperado del historial de Git, porque no identificaba entrevistado, cargo ni establecimiento y su clasificación como taller era tentativa.

La entrevista `COMPRADOR_002` corresponde al audio del 2026-10-23 (`WhatsApp Audio 2026-10-23 at 10.32.41 PM.aac`, copiado en `data/raw/audios/COMPRADOR_002.aac`) y se transcribió automáticamente con Vosk; el texto está en `data/raw/entrevistas/comprador_002.md`. La sesión `COMPRADOR_003`, del 2026-10-28, reúne 12 notas de voz y el texto de 11 respuestas aportado por el investigador; su primera parte está en `data/raw/audios/COMPRADOR_003.ogg` y las transcripciones en `data/raw/entrevistas/comprador_003.md` y `comprador_003_partes.md`. El texto de 11 respuestas se había registrado inicialmente como `COMPRADOR_002`; al verificar los audios se reasignó a `COMPRADOR_003`. `faster-whisper`/`ctranslate2` no funciona en este equipo; la transcripción se hizo con `vosk-model-small-es-0.42`.

## Categorías de análisis

- Precios y rangos de precios.
- Modelos y marcas con mayor demanda.
- Preferencias de compra.
- Disponibilidad de repuestos y mantenimiento.
- Diferencias entre motos de combustión y eléctricas.

## Limitaciones

- El número de entrevistas es muy reducido y no es representativo del mercado.
- No se dispone de entrevistas de importadoras.
- Los 14 audios revisados se clasificaron como compradores por su contenido; no se identificaron entrevistas a talleres o importadoras. La atribución debe confirmarse en campo.
- Las transcripciones automáticas de Vosk son ruidosas; solo se registran respuestas claras y el resto queda en `null`.
- La evidencia cualitativa se usa para interpretar los datos cuantitativos, no para estimar volúmenes ni precios.
- No se fabricaron ni completaron respuestas: los campos sin información quedaron vacíos y documentados.
