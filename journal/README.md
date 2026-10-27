# Journal - Bitácora de Desarrollo

Registro cronológico de los avances, decisiones técnicas, modificaciones y entregables del proyecto **Investigación del Mercado de Motos en Cuba**.

---

## 📅 16 de octubre de 2026
- **Inicialización del repositorio:** Creación del repositorio y commit inicial (`c11813d`).

---

## 📅 17 de octubre de 2026
- **Migración de contenidos:** Importación de fotografías y README desde el repositorio previo `Mercado-de-Motos-Cuba`.
- **Estructuración profesional:** Organización de carpetas (`src/`, `datos/`, `docs/`, `notebooks/`, `graficos/`, `reports/`).
- **Scraper de Revolico:** Implementación del script de extracción automatizada de anuncios en La Habana y almacenamiento de datos crudos en formato CSV y JSON.
- **Normalización de categorías:** Definición de categorías principales (Motos de combustión, Motos eléctricas, Bicicletas eléctricas y Patinetes eléctricos), excluyendo triciclos y removiendo datos personales (teléfonos/direcciones).
- **Análisis exploratorio inicial (EDA):**
  - Procesamiento de los 30 anuncios más recientes.
  - Creación de la tabla de anuncios recientes con precios, marcas y enlaces de Revolico.
  - Generación del gráfico de evolución del mercado (2024-2026) comparando eléctricas vs. combustión.
- **Limpieza de datos y detección de anomalías:** Implementación de scripts en Python para la limpieza automatizada, estandarización de monedas y detección de precios atípicos (*outliers*).
- **Notebooks:** Creación del notebook interactivo `eda_motos.ipynb`.

---

## 📅 22 de octubre de 2026
- **Organización de entregables:** Creación de las carpetas `journal/` y `hands-off/` para bitácoras y entregables ejecutivos.
- **Gestión de entrevistas:** Reorganización de la estructura de datos (`datos/entrevistas/`), sustituyendo la carpeta de encuestas por registros de entrevistas cualitativas.
- **Registro de entrevistas:** Adición de la entrevista sobre precios y modelos más vendidos, incluyendo metadatos de fecha, entrevistado y lugar.
- **Automatización de reportes (ETL & Informes):**
  - Ejecución de procesos ETL para consolidar datos limpios.
  - Generación de informes de precios atípicos y distribución por categorías.
  - Creación de gráficos avanzados en `reports/graficos/` (composición de segmentos, demanda vs. precio, índice de demanda, top por segmento).

---

## 📅 23 - 24 de octubre de 2026
- **Consolidación y documentación:** Actualización de la documentación principal, integración de la bitácora en el `journal` y verificación general del estado del proyecto para su presentación final.

---

## 📅 26 de octubre de 2026
- **Actualización del corte de Revolico (09:56):** nuevo scrapeo de los 30 anuncios más recientes de La Habana con la skill `revolico-scraper` (raw → processed → limpio → métricas → informes `tabla_top30`, `precios_atipicos`, `precios_categorias` → gráficos → README). Se reemplazaron los datos del 22/10 (archivos anteriores movidos a `datos/_reemplazados/20261026_095603/`). Resultado: 8 anuncios de combustión, 21 eléctricos y 1 patinete.
- **Catálogo VEDCA (10:08):** nuevo scraper `src/scraping/vedca.py` para vedca.cu. 22 productos consultados, 7 vehículos en lista blanca (5 eléctricos, 2 patinetes). La fábrica **no publica precios**; salida en `docs/informes/vedca_catalogo_20261026_100817.md`.
- **Precios Islagrande (11:45 → 18:55):** nuevo scraper `src/scraping/islagrande.py` (tienda online de VEDCA, moneda USD). 33 productos consultados, 15 en lista blanca, **14 precios válidos** (601–2 096 USD). Correcciones posteriores: precios implausibles (< 100 USD, p. ej. 5,06 USD) marcados `precio_valido: false`, precios "antes" incoherentes descartados y productos repetidos por sede deduplicados en el informe.
- **Corrección de documentación:** revertido un error tipográfico en la tabla de rentabilidad de `reports/README.md` (compra P25 de ITALY RX Combat: 480 → 2 480 USD).
- **README:** se completaron las secciones de **Resultados/Hallazgos** y **Conclusiones** (respondiendo las dos preguntas de análisis), se actualizó la tabla de fuentes (Revolico, VEDCA, Islagrande, entrevistas) y el árbol de estructura del proyecto (`data/`, `journal/`, `hands-off/`, `reports/`).
- **Entregable ejecutivo:** creado `hands-off/resumen_ejecutivo_20261026.md` con cifras clave, hallazgos y recomendaciones.

---

## 📅 26 de octubre de 2026 (corrección de privacidad y corte consolidado)
- **Sanitización de datos de contacto:** nuevo módulo `src/contactos.py` (`sanear_contactos`) que elimina teléfonos cubanos (`+53...`, `5 994-8751`, `7 656-2154`), etiquetas ("WhatsApp al ...") y correos de cualquier texto, preservando timestamps, IDs de anuncio y URLs. Se aplicó a todos los scrapers (`islagrande.py`, `vedca.py`, `revolico/scrape.py`) y al ETL (`etl_mercado.py`).
- **Limpieza de la base histórica:** saneados in place 26 ficheros `.json`/`.csv` bajo `data/` y `datos/` (raw, processed, clean, tiendas_online, _reemplazados). Verificación final: **0 contactos restantes**, JSON válidos.
- **ETL + informe regenerados con el corte del 26/10:** el ETL ahora lee también los cortes de la skill en la raíz de `data/raw/` (`revolico_raw_*.json`). Nuevas cifras: **6 643 brutos → 6 278 anuncios únicos** (5 714 con precio USD, 91,0 %), ventana 10–26 de octubre (17 días, 3 cortes: 17, 22 y 26). El informe (`reports/README.md`) y sus gráficos se regeneraron; el encabezado y la ventana ahora se calculan desde los datos.
- **Cifras actualizadas:** README principal y `hands-off/resumen_ejecutivo_20261026.md` alineados con el nuevo corte (RX Combat 51 anuncios, TOPMAQ 182, JMD bicimoto 175, ROI TOPMAQ 27,9 %).

---

## 📅 27 de octubre de 2026 — Unificación de `data/` y `datos/`
- **Estructura unificada:** eliminada la carpeta `data/`; todo vive ahora en `datos/` (pipeline `raw/ → processed/ → clean/` junto a las fuentes por nombre: `revolico/`, `limpios/`, `tiendas_online/`, `importadora_vedca/`, `entrevistas/`, `codigos/`, etc.). Movimientos con `git mv` para conservar el historial.
- **Código actualizado:** rutas en `common.py` (paths del pipeline), `scrape.py`, `clean.py`, `analyze.py`, `pipeline.py`, `islagrande.py`, `vedca.py`, `etl_mercado.py`, `informe_mercado.py` y `contactos.py`; skill `revolico-scraper` (SKILL.md, README, esquema y scripts) y árbol del README principal.
- **Verificación:** ETL e informe regenerados sin errores con las nuevas rutas (mismas cifras: 6 278 anuncios); `py_compile` de todo `src/` OK; cero referencias residuales a `data/` en el código vivo.
