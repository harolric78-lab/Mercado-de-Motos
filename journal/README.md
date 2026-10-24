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
