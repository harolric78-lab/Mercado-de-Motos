# Journal — Bitácora de Desarrollo

Registro cronológico de los avances, decisiones técnicas, modificaciones y entregables del proyecto **Investigación del Mercado de Motos en Cuba**.

---

## 📅 16 de octubre de 2026
- **Inicialización del repositorio:** creación del repositorio y commit inicial (`c11813d`).

---

## 📅 17 de octubre de 2026
- **Migración de contenidos:** importación de fotografías y README desde el repositorio previo `Mercado-de-Motos-Cuba`.
- **Estructuración profesional:** organización de carpetas (`src/`, `datos/`, `docs/`, `notebooks/`, `graficos/`, `reports/`).
- **Scraper de Revolico:** extracción automatizada de anuncios de La Habana y almacenamiento en CSV y JSON.
- **Definición de alcance:** cuatro categorías oficiales (motos de combustión, motos eléctricas, bicicletas eléctricas y patinetes) y eliminación de datos personales.
- **Análisis exploratorio inicial:** procesamiento de los 30 anuncios más recientes, tabla de anuncios y gráfico de evolución.
- **Limpieza y anomalías:** scripts de normalización, estandarización de monedas y detección de precios atípicos.
- **Notebooks:** creación de `eda_motos.ipynb`.

---

## 📅 22 de octubre de 2026
- **Organización de entregables:** creación de `journal/` y `hands-off/`.
- **Entrevistas:** reorganización de la estructura de datos y registro de la entrevista cualitativa.
- **Automatización de reportes:** ejecución del ETL, informes de precios y distribución por categorías, y gráficos en `reports/graficos/`.

---

## 📅 23–24 de octubre de 2026
- **Consolidación y documentación:** actualización de la documentación principal, integración de la bitácora y verificación general del proyecto.

---

## 📅 26 de octubre de 2026
- **Nuevo corte de Revolico:** 30 anuncios recientes de La Habana, con actualización de datos, métricas, informes y gráficos.
- **Documentación:** actualización de resultados, conclusiones, fuentes y estructura del proyecto.
- **Entregable ejecutivo:** creación del resumen ejecutivo con cifras clave y hallazgos.

---

## 📅 27 de octubre de 2026 — Unificación de estructura
- **Estructura unificada:** se eliminó la carpeta `data/` y todo el pipeline quedó en `datos/`.
- **Código actualizado:** rutas de scrapers, ETL, informes y skill de scraping.
- **Verificación:** ETL e informe regenerados sin errores y `py_compile` correcto.

---

## 📅 28 de octubre de 2026 — Depuración de alcance y nueva estructura
- **Backup externo:** copia completa del repositorio antes de la limpieza, con verificación SHA256 de todos los archivos.
- **Depuración de alcance:** el repositorio se limita a las cuatro categorías oficiales; se retiraron datasets, informes, gráficos y referencias de vehículos fuera de alcance.
- **Nueva estructura de datos:**
  - `data_raw/revolico/` para los cortes crudos depurados.
  - `data_clean/` para el histórico consolidado, los archivos por categoría y los cortes del 22 y 26 de octubre.
- **ETL y reportes:** se actualizaron `src/analisis/etl_mercado.py` y `src/analisis/generar_reporte.py`; se regeneraron el informe, las métricas y los gráficos.
- **Resultado del histórico depurado:** 6.101 anuncios.
  - Motos de Combustión: 1.099.
  - Motos Eléctricas: 2.201.
  - Bicicletas Eléctricas: 2.576.
  - Patinetes: 225.
- **Corte del 26/10/2026:** 30 anuncios (9 de combustión, 3 motos eléctricas, 17 bicicletas eléctricas y 1 patinete).
- **Documentación:** README principal, informe, resumen ejecutivo, metodología y journal actualizados.
- **Validación:** datasets con cuatro categorías, sin referencias de alcance fuera del proyecto; compilación de `src/` y pruebas básicas.
- **Publicación:** cambios preparados; push pendiente de confirmación.

---

## 📅 31 de octubre de 2026 — Refactor de estructura profesional
- **Limpieza:** eliminado el clon anidado `Mercado-de-Motos/Mercado-de-Motos/`, cachés de pruebas y entornos virtuales de la raíz.
- **Nueva estructura de datos:** `data/raw/revolico/` para cortes crudos, `data/processed/` para el dataset consolidado y los cortes, y `data/interim/` para la salida auxiliar del ETL (ignorada por Git).
- **Depuración:** retirados los históricos duplicados y las carpetas derivadas por categoría; el consolidado canónico es `data/processed/anuncios_limpios.*`.
- **Código y reportes:** actualizadas las rutas en scrapers, ETL, validación, notebook y generador de reportes; informe y métricas estandarizados como `reports/informe_mercado.md` y `reports/metricas/resumen_mercado.*`.
- **Entorno:** creado `Mercado-de-Motos/.venv` con las dependencias de `requirements.txt`.
- **Validación:** dataset de 6.101 anuncios y pruebas automáticas en verde.
