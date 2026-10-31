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
| Talleres | [`talleres.json`](talleres.json) | 1 | Migrada desde el historial de Git |
| Importadoras | [`importadoras.json`](importadoras.json) | 0 | Estructura vacía documentada |
| Usuarios | [`usuarios.json`](usuarios.json) | 0 | Estructura vacía documentada |

La única entrevista real disponible es `TALLER_001`, fechada el 2026-10-22. El registro original no identifica al entrevistado ni el tipo exacto de fuente; la clasificación como taller es tentativa y debe confirmarse.

## Categorías de análisis

- Precios y rangos de precios.
- Modelos y marcas con mayor demanda.
- Preferencias de compra.
- Disponibilidad de repuestos y mantenimiento.
- Diferencias entre motos de combustión y eléctricas.

## Limitaciones

- El número de entrevistas es muy reducido y no es representativo del mercado.
- No se dispone de entrevistas de importadoras ni de usuarios.
- La entrevista migrada no identifica al entrevistado, su cargo ni el lugar exacto.
- La evidencia cualitativa se usa para interpretar los datos cuantitativos, no para estimar volúmenes ni precios.
- No se fabricaron ni completaron respuestas: los campos sin información quedaron vacíos y documentados.
