# Código Python del proyecto

Copia de referencia de los scripts `.py` utilizados durante el proyecto.

## Contenido

- `src/`: pipeline cuantitativo (scraping, ETL, reportes) y cualitativo (captura y transcripción).
- `prueba_datos.py`: copia de `tests/test_datos.py`; se renombró para que `pytest` no recoja la prueba dos veces.
- `analisis_entrevistas/`: scripts auxiliares usados para inspeccionar audios, normalizar el lote de entrevistas y validar su estructura.
  - `normalizar_lote.py`: construye los registros JSON a partir de las transcripciones `.md`.
  - `validar_entrevistas.py`: comprueba IDs, bloques del esquema, hashes y totales.
  - `info_taller.py`: obtiene duración y SHA256 de los audios de una carpeta.

## Nota

Los scripts activos siguen en `src/` y `tests/`. Estas copias son un respaldo de consulta; sus rutas relativas asumen la raíz del repositorio.
