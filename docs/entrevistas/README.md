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
| Compradores | [`compradores.json`](compradores.json) | 2 | `COMPRADOR_001` (2026-11-01) y `COMPRADOR_002` (2026-11-03) |

La entrevista `COMPRADOR_001`, fechada el 2026-10-17, corresponde a un comprador de San Miguel del Padrón y cuenta con transcripción en `data/raw/entrevistas/comprador_001.md` y audio en `data/raw/audios/COMPRADOR_001.mp4`. Se eliminó el registro `TALLER_001`, recuperado del historial de Git, porque no identificaba entrevistado, cargo ni establecimiento y su clasificación como taller era tentativa.

La entrevista `COMPRADOR_002`, añadida el 2026-11-03, se incorporó a partir de un texto aportado por el investigador y clasificado como comprador. Su transcripción está en `data/raw/entrevistas/comprador_002.md`. La correspondencia con `data/raw/audios/COMPRADOR_002.aac` y los datos de perfil/fecha quedan pendientes de verificar. La transcripción automática con `faster-whisper` no pudo ejecutarse porque `ctranslate2` falla con Python 3.14.

## Categorías de análisis

- Precios y rangos de precios.
- Modelos y marcas con mayor demanda.
- Preferencias de compra.
- Disponibilidad de repuestos y mantenimiento.
- Diferencias entre motos de combustión y eléctricas.

## Limitaciones

- El número de entrevistas es muy reducido y no es representativo del mercado.
- No se dispone de entrevistas de importadoras.
- La clasificación de los audios nuevos como compradores se basa en el contenido de la transcripción y debe confirmarse en campo.
- La evidencia cualitativa se usa para interpretar los datos cuantitativos, no para estimar volúmenes ni precios.
- No se fabricaron ni completaron respuestas: los campos sin información quedaron vacíos y documentados.
