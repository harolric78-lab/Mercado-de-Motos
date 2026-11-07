# 🏍️ Análisis del Mercado de Motos en Cuba

Proyecto de análisis de datos sobre la oferta publicada de vehículos ligeros en La Habana, desarrollado para la asignatura **Introducción a la Ciencia de los Datos**. Integra recolección automatizada, limpieza, ETL, análisis exploratorio y generación reproducible de reportes.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📖 Introducción

La movilidad urbana constituye uno de los principales desafíos para la población cubana. Las motocicletas y otros vehículos ligeros representan una alternativa cada vez más utilizada debido a su menor consumo energético, facilidad de desplazamiento y disponibilidad en el mercado informal.

Este proyecto utiliza anuncios publicados en Revolico para estudiar las características del mercado de:

- **Motos de combustión**
- **Motos eléctricas**
- **Patinetes eléctricos**

Además, el estudio se complementa con observaciones de campo, entrevistas y visitas a talleres e importadoras para contextualizar los resultados obtenidos.

Los hallazgos permiten identificar patrones de oferta, comportamiento de precios y tendencias observables dentro de este segmento del mercado.

---

## 🎯 Objetivo General

Analizar la oferta de motos de combustión, motos eléctricas y patinetes eléctricos anunciados en La Habana mediante técnicas de recopilación, procesamiento y análisis de datos, con el propósito de identificar patrones de precios, composición del mercado y tendencias relevantes.

---

## 🎯 Objetivo Principal

Analizar el mercado de **motos de combustión**, **motos eléctricas** y **patinetes eléctricos** en La Habana para comprender:

- la composición del mercado;
- el comportamiento de los precios;
- la oferta disponible;
- las tendencias observadas.

---

## 🔍 Preguntas de Investigación

El proyecto aborda **30 preguntas de investigación** agrupadas en seis bloques:

| Bloque | Preguntas | Estado |
|---|---|---|
| 1. Mercado y demanda | 1, 2, 3, 4, 5, 6 | 3 completas, 3 parciales |
| 2. Precios y capacidad de pago | 7, 8, 9, 10 | 2 completas, 2 parciales |
| 3. Importación, papeles y regulación | 11, 12, 13, 14, 15, 16, 17, 18 | 3 completas, 5 parciales |
| 4. Repuestos y servicio técnico | 19, 20, 21, 22, 23 | 0 completas, 5 parciales |
| 5. Uso, carga y apagones | 24, 25, 26, 27 | 1 completa, 3 parciales |
| 6. Canales, confianza y futuro | 28, 29, 30 | 0 completas, 3 parciales |

**Veredicto final:** 5 🟢 respondidas con datos · 21 🟡 respondidas parcialmente · 4 🔴 sin respuesta (5, 11, 20, 22).

Los detalles completos se encuentran en [`docs/entregables/respuestas_30_preguntas.md`](docs/entregables/respuestas_30_preguntas.md) y en los documentos de entregables asociados.

---

## 📊 Dataset

El estudio integra **tres fuentes principales de datos**: los anuncios públicos de Revolico, las entrevistas a compradores y la información de instituciones o importadoras. Los anuncios de Revolico constituyen la base cuantitativa de oferta publicada; las entrevistas y las instituciones o importadoras aportan contexto, precios percibidos, disponibilidad y prácticas del mercado.

El dataset consolidado contiene **6.159 anuncios** capturados entre el **10 y el 26 de octubre de 2026**. Cada registro puede incluir información como:

- Título y descripción del anuncio
- Categoría principal (combustión, eléctrica, scooter)
- Marca
- Modelo
- Precio
- Moneda (`USD` / `CUP`)
- Precio normalizado en USD
- Fecha de captura
- Número de visualizaciones
- URL del anuncio
- Ubicación (municipio, provincia) cuando está disponible

Archivos principales en [`data/processed/`](data/processed/):

- `anuncios_limpios.csv` / `anuncios_limpios.json` — dataset histórico consolidado.
- `manifiesto.json` — conteos y huellas SHA256 de las fuentes.
- `cortes/` — cortes del 22 y 26 de octubre de 2026.

Los cortes crudos se conservan en [`data/raw/revolico/`](data/raw/revolico/) y la salida auxiliar del ETL se escribe en `data/interim/` (ignorada por Git).

Antes del análisis, los datos fueron sometidos a procesos de limpieza, normalización y validación para garantizar su consistencia. Los precios en USD se usan para las estadísticas; los anuncios en CUP se conservan para el conteo.

---

## 📚 Fuentes de Información

El proyecto trabaja con **fuentes de datos complementarias**, que se usan de forma separada para preservar la trazabilidad:

| Fuente | Tipo de dato | Aporte al estudio |
|---|---|---|
| Revolico (La Habana) | Cuantitativa | **6.159 anuncios** en 3 cortes (17, 22 y 26 de octubre de 2026): 1.137 de combustión, 4.778 eléctricas, 244 patinetes. Aporta precios en USD, marcas, categorías y vistas. |
| Compradores | Cualitativa | **25 entrevistas** (`COMPRADOR_001` a `COMPRADOR_025`): preferencias entre combustión y eléctrica, gastos, uso, repuestos y percepciones de precio. |
| Importadoras | Cualitativa | **1 entrevista** a Solimport (`IMPORTADORA_001`): catálogo, aranceles, formación de precios, reventa y demanda. |
| Talleres | Cualitativa | **4 entrevistas** (`TALLER_001` a `TALLER_004`): preferencia gasolina/eléctrica, autonomía, repuestos y uso. |
| Fuentes oficiales (Gaceta Oficial, BCC, ONEI) | Oficial | Resoluciones 171-175/2026, 340/2026, 197/2026; Ley 109/2010; tasa BCC 793 CUP/USD. |

Los anuncios de Revolico se publican como dataset analizable en [`data/processed/`](data/processed/). Las entrevistas y la información de instituciones o importadoras se documentan en [`docs/entrevistas/`](docs/entrevistas/), [`docs/images/`](docs/images/) y [`journal/journal.md`](journal/journal.md) para cuidar la privacidad y dejar rastro de la fuente. El hand-off y el journal viven en las carpetas `handoff/` y `journal/` del repositorio.

---

## 🗣️ Fuentes del estudio

La investigación combina datos cuantitativos y cualitativos de tres fuentes que se mantienen claramente separadas:

### 1. Anuncios de Revolico (fuente cuantitativa)

- Obtenidos mediante scraping de anuncios públicos de Revolico.
- Almacenados en [`data/raw/`](data/raw/) (cortes crudos) y [`data/processed/`](data/processed/) (dataset procesado).
- Sostienen las estadísticas, métricas y gráficos del estudio.

### 2. Entrevistas (fuente cualitativa)

- **Compradores:** preferencias, gastos, uso, repuestos y percepciones de precio.
- **Talleres e importadoras:** oferta, precios, disponibilidad y prácticas del mercado.
- Normalizadas en [`docs/entrevistas/`](docs/entrevistas/).
- Transcripciones y audios en [`data/raw/entrevistas/`](data/raw/entrevistas/) y `data/raw/audios/` (los audios no se publican).

### 3. Instituciones o importadoras (fuente cualitativa)

- Entrevista a **Solimport** (`IMPORTADORA_001`): catálogo, aranceles, costos de importación, formación de precios, reventa y demanda.
- Aporta contexto sobre oferta formal, precios, tributos y prácticas comerciales.
- Se documenta en [`docs/entrevistas/`](docs/entrevistas/), [`docs/images/`](docs/images/) (7 fotografías) y [`journal/journal.md`](journal/journal.md).

Las entrevistas y la información de instituciones o importadoras se usan para interpretar y contextualizar los resultados cuantitativos. No se emplean para estimar volúmenes de ventas ni para sustituir el dataset de anuncios, pero sí son **fuentes de dato con valor propio** dentro del estudio.

> Estado actual: el registro de entrevistas se reinició el **2026-11-04** y ya incluye **25 entrevistas de compradores** (`COMPRADOR_001` a `COMPRADOR_025`), **4 de talleres** (`TALLER_001` a `TALLER_004`) y **1 de importadora** (`IMPORTADORA_001`, Solimport). `COMPRADOR_001`, `COMPRADOR_002` y `COMPRADOR_004` a `COMPRADOR_024` se transcribieron con Vosk a partir de audios nuevos; `COMPRADOR_003` y `COMPRADOR_025` se recuperaron como texto sin audio. `COMPRADOR_011` y `COMPRADOR_012` tienen audio del 2026-10-23, `COMPRADOR_014` del 2026-11-04 y `COMPRADOR_017` reúne cuatro audios del 2026-11-05. Se descartaron los audios que duplicaban la sesión antigua. Se conservan **7 fotografías** de importadoras y tiendas y la observación de campo. La transcripción automática disponible es Vosk (`vosk-model-small-es-0.42`); `faster-whisper`/`ctranslate2` no funciona en este equipo.

---

## 🔬 Metodología

El proyecto sigue un flujo típico de Ciencia de Datos:

```text
Obtención de datos
        ↓
Limpieza
        ↓
Transformación
        ↓
Análisis Exploratorio
        ↓
Visualización
        ↓
Interpretación
```

| Etapa | Descripción | Implementación |
|---|---|---|
| Recolección | Descarga automatizada de anuncios públicos de Revolico en La Habana | [`src/scraping/revolico/scrape.py`](src/scraping/revolico/scrape.py) |
| Limpieza | Saneamiento de contactos, normalización de títulos, precios y monedas | [`src/contactos.py`](src/contactos.py) · [`src/analisis/etl_mercado.py`](src/analisis/etl_mercado.py) |
| Transformación | Clasificación por categorías, deduplicación y consolidación del histórico | [`src/analisis/etl_mercado.py`](src/analisis/etl_mercado.py) |
| Análisis Exploratorio | Estadísticas descriptivas de precios y vistas por categoría | [`notebooks/eda_motos.ipynb`](notebooks/eda_motos.ipynb) |
| Visualización | Gráficos de composición, precios, demanda, evolución y marcas | [`src/analisis/generar_reporte.py`](src/analisis/generar_reporte.py) |
| Interpretación | Informe, métricas y resumen ejecutivo | [`reports/`](reports/) · [`docs/entregables/`](docs/entregables/) |

## 📈 Resultados

Resumen del mercado observado (precios en USD):

| Categoría principal | Anuncios | % del total | Precio mediano USD | Equivalente CUP (793) |
|---|---:|---:|---:|---:|
| Motos Eléctricas | 4,778 | 77.6% | 1.550 | 1.229.150 |
| Motos de Combustión | 1.137 | 18.5% | 2.300 | 1.823.900 |
| Patinetes Eléctricos | 244 | 4.0% | 750 | 594.750 |
| **Total** | **6.159** | **100.0%** | — | — |

Los resultados completos se generan automáticamente en:

- [`reports/informe_mercado.md`](reports/informe_mercado.md) — informe con composición, precios, demanda, cortes y marcas.
- [`reports/metricas/`](reports/metricas/) — métricas del mercado en JSON y CSV.
- [`reports/graficos/`](reports/graficos/) — 5 gráficos de composición, precios, marcas, evolución y municipios.
- [`docs/entregables/`](docs/entregables/) — resumen ejecutivo y entregables de las 30 preguntas.

### Gráficos disponibles

| Archivo | Contenido |
|---|---|
| `01_composicion.png` | Composición por categoría principal |
| `02_precios.png` | Precio mediano por categoría (USD) |
| `03_marcas.png` | Top 10 marcas por número de anuncios |
| `04_evolucion.png` | Evolución diaria de anuncios por categoría |
| `05_municipios.png` | Municipios con más anuncios geolocalizados |

---

## 📂 Estructura del Proyecto

```text
Mercado-de-Motos/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── explicacion_pipeline.md
│
├── data/
│   ├── raw/
│   │   └── revolico/                 # Cortes crudos (JSON y CSV)
│   │       └── geo_catalogo.json     # Catálogo de provincias y municipios
│   ├── interim/                      # Salida auxiliar del ETL (ignorada por Git)
│   └── processed/
│       ├── anuncios_limpios.csv      # Dataset histórico consolidado (6.159 anuncios)
│       ├── anuncios_limpios.json
│       ├── manifiesto.json           # Conteos y huellas SHA256 de las fuentes
│       └── cortes/                   # Cortes del 22 y 26 de octubre de 2026
│
├── docs/
│   ├── entregables/                  # 8 documentos de respuestas y entregables
│   │   ├── respuestas_30_preguntas.md
│   │   ├── respuestas_17_preguntas_pendientes.md
│   │   ├── respuestas_21_parciales_completadas.md
│   │   ├── respuestas_entrevistas_q4_q6_q7_q28.md
│   │   ├── respuestas_fuentes_oficiales.md
│   │   ├── storytelling_mercado_motos.md
│   │   ├── trabajo_campo_resultados.md
│   │   ├── plan_refactor_scraper_revolico.md
│   │   └── preguntas_reformuladas.md
│   ├── entrevistas/
│   │   ├── README.md
│   │   ├── talleres.json
│   │   │   ├── importadoras.json
│   │   │   └── compradores.json
│   ├── images/                       # Registro fotográfico de campo
│   │   ├── evidencia_campo.md
│   │   ├── importadoras/
│   │   │   ├── talleres/
│   │   │   └── tiendas/
│   ├── journal.md                    # Bitácora de desarrollo
│   ├── handoff.md                    # Estado del proyecto para continuación
│   ├── technical_report.md           # Reporte técnico de arquitectura y métricas
│   └── metodologia/
│       └── DECISIONES_ARQUITECTURA.md
│
├── notebooks/
│   └── eda_motos.ipynb               # Análisis exploratorio
│
├── reports/
│   ├── informe_mercado.md            # Informe generado automáticamente
│   ├── graficos/                     # 01_composicion ... 05_municipios
│   └── metricas/                     # resumen_mercado.json y resumen_mercado.csv
│
├── src/
│   ├── contactos.py                  # Saneamiento de datos de contacto
│   ├── verificar_datos.py            # Validación de integridad del dataset
│   ├── analisis/
│   │   ├── etl_mercado.py            # Limpieza, clasificación y deduplicación
│   │   └── generar_reporte.py        # Métricas, gráficos e informe
│   ├── scraping/
│   │   └── revolico/
│   │       ├── common.py             # Utilidades y reglas de clasificación
│   │       └── scrape.py             # Scraper de anuncios
│   └── visualizacion/                # Reservado para visualizaciones adicionales
│
└── tests/
    └── test_datos.py                 # Pruebas de validación
```

---

## ⚙️ Reproducción del Proyecto

**Requisitos:** Python 3.10 o superior y Git.

### Instalación

```bash
git clone https://github.com/harolric78-lab/Mercado-de-Motos.git

cd Mercado-de-Motos

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

### Validar el Dataset

```bash
python src/verificar_datos.py
```

Comprueba el total del histórico, los conteos por categoría, los identificadores y los cortes históricos.

---

### Ejecutar ETL

```bash
python src/analisis/etl_mercado.py
```

Lee `data/raw/revolico/` y escribe una salida auxiliar en `data/interim/`. No sobrescribe el dataset consolidado.

---

### Generar Reportes

```bash
python src/analisis/generar_reporte.py
```

Regenera `reports/informe_mercado.md`, las métricas en `reports/metricas/` y los gráficos en `reports/graficos/`.

---

### Actualizar Datos

```bash
python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0
```

Descarga un nuevo corte de anuncios y lo guarda en `data/raw/revolico/` con sello temporal.

---

### Ejecutar Pruebas

```bash
pytest -q
```

---

### Abrir Notebook

```bash
jupyter notebook
```

---

## 🔄 Trazabilidad y Reproducibilidad

El proyecto incorpora mecanismos para garantizar:

- Procedencia de los datos.
- Validación automática.
- Versionado mediante Git y GitHub.
- Reproducibilidad de métricas y gráficos.
- Control de integridad mediante manifiestos (`data/processed/manifiesto.json`).
- Separación entre datos crudos y datos procesados.
- Trazabilidad completa: cada registro incluye `sello_extraccion`, `archivo_origen`, `ref_provincia`, `ref_municipio` y `municipio_no_identificado`.

La metodología completa y las decisiones de diseño se encuentran documentadas en:

```text
docs/metodologia/
```

---

## 🎓 Aplicación de Ciencia de Datos

Durante el desarrollo del proyecto se aplican conceptos fundamentales de Ciencia de Datos:

- Web Scraping
- Ingeniería de Datos
- Procesos ETL
- Limpieza de Datos
- Análisis Exploratorio de Datos (EDA)
- Visualización de Datos
- Validación y pruebas
- Trazabilidad de datos
- Reproducibilidad analítica

---

## ⚠️ Limitaciones

- Los anuncios representan oferta publicada y no ventas efectivas.
- La calidad de los resultados depende de la calidad de los anuncios originales.
- El estudio se limita a los datos disponibles durante el período de captura (10 al 26 de octubre de 2026).
- No existen registros oficiales de ventas que permitan contrastar completamente los resultados obtenidos.
- Algunos factores de decisión de compra solo pueden inferirse parcialmente mediante información cualitativa complementaria.
- La fuente cuantitativa proviene de un solo portal de anuncios, con una serie temporal corta.
- Solo el 1.70% de los anuncios tiene municipio identificable; no se puede hacer análisis detallado por zona sin geolocalización adicional.
- La transcripción con `faster-whisper`/`ctranslate2` no funciona en Python 3.14 (access violation); se usa Vosk con precisión limitada en audios ruidosos.

---

## ✅ Conclusiones

Este proyecto demuestra cómo las técnicas de Ciencia de Datos pueden emplearse para estudiar mercados reales a partir de fuentes de información abiertas.

La combinación de recolección automatizada, limpieza de datos, análisis exploratorio y visualización permite obtener una caracterización cuantitativa del mercado de motos en La Habana. Los resultados constituyen una base para futuras investigaciones relacionadas con movilidad, comportamiento de consumo y análisis de mercados digitales en Cuba.

De las 30 preguntas de investigación, 26 tienen al menos una respuesta parcial o completa basadas en los datos disponibles y fuentes oficiales. Las 4 preguntas restantes (oferta por zona, influencia de remesas, repuestos difíciles y demoras, censo de talleres) requieren trabajo de campo adicional que no pudo realizarse desde este entorno.

---

## 👤 Autor

**Harold Ricardo Ponce**

**Asignatura:** Introducción a la Ciencia de los Datos

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Consulta el archivo [`LICENSE`](LICENSE) para más información.

---

## Entregables PDF

| Documento | Abrir en el navegador | Descargar |
|---|---|---|
| Informe del proyecto | [Abrir PDF](https://raw.githack.com/harolric78-lab/Mercado-de-Motos/master/Informe_Proyecto_Mercado_Motos.pdf) | [Descargar](https://raw.githubusercontent.com/harolric78-lab/Mercado-de-Motos/master/Informe_Proyecto_Mercado_Motos.pdf) |
| Reporte t?cnico | [Abrir PDF](https://raw.githack.com/harolric78-lab/Mercado-de-Motos/master/Reporte_Tecnico_Proyecto_Mercado_Motos.pdf) | [Descargar](https://raw.githubusercontent.com/harolric78-lab/Mercado-de-Motos/master/Reporte_Tecnico_Proyecto_Mercado_Motos.pdf) |
| Presentaci?n visual | [Abrir PDF](https://raw.githack.com/harolric78-lab/Mercado-de-Motos/master/Presentacion_Visual.pdf) | [Descargar](https://raw.githubusercontent.com/harolric78-lab/Mercado-de-Motos/master/Presentacion_Visual.pdf) |
