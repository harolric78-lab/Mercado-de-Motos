# Decisiones de arquitectura

## Alcance del dataset

El repositorio se limita a cuatro categorías oficiales:

1. Motos de combustión.
2. Motos eléctricas.
3. Bicicletas eléctricas (incluye bicimotos).
4. Patinetes.

La depuración de alcance se realizó antes de publicar los datos; no se conservan en el repositorio registros, métricas ni referencias de vehículos fuera de las cuatro categorías.

## Estructura de datos

- `data/raw/revolico/`: cortes crudos depurados, con los campos originales de los anuncios y sin datos de contacto.
- `data/processed/`: dataset consolidado y cortes históricos.
- `data/interim/`: salida auxiliar del ETL, ignorada por Git.
- `reports/`: informe ejecutivo, métricas y gráficos.
- `src/analisis/etl_mercado.py`: normalización, clasificación y deduplicación; su salida auxiliar va a `data/interim/` y no sobrescribe el consolidado.
- `src/analisis/generar_reporte.py`: generación del informe y de las visualizaciones.

## Reglas de clasificación

- La categoría se asigna por evidencia positiva en el título y la descripción.
- Las bicicletas eléctricas incluyen los anuncios de bicimotos.
- Los anuncios sin evidencia suficiente no se publican en `data/processed/`.
- Los precios en USD se usan para las estadísticas; los anuncios en CUP se conservan para conteo.

## Deduplicación

1. Se conserva un registro por identificador, priorizando el que tiene más información.
2. Se eliminan repeticiones exactas con título específico, precio, moneda y día coincidentes.
3. Los títulos genéricos no se usan para eliminar repeticiones.

## Privacidad

Los textos se sanean para retirar teléfonos y correos antes de guardar los datasets y los informes.
