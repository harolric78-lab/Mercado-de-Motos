# 🏍️ Análisis del Mercado de Motos en Cuba

Proyecto de análisis de datos sobre la oferta publicada de vehículos ligeros en La Habana, desarrollado para la asignatura **Introducción a la Ciencia de los Datos**. Integra recolección automatizada, limpieza, análisis exploratorio y generación reproducible de reportes.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📖 Introducción

La movilidad urbana constituye uno de los principales desafíos para la población cubana. Las motocicletas y otros vehículos ligeros representan una alternativa cada vez más utilizada debido a su menor consumo energético, facilidad de desplazamiento y disponibilidad en el mercado informal.

Este proyecto utiliza anuncios publicados en Revolico para estudiar las características del mercado de:

- Motos de combustión
- Motos eléctricas
- Bicicletas eléctricas (incluye bicimotos)
- Patinetes

La categoría `bicicletas_electricas` se conserva porque agrupa los anuncios de bicimotos, que en la práctica compiten directamente con las motos eléctricas. Su tratamiento se detalla en [`docs/metodologia/DECISIONES_ARQUITECTURA.md`](docs/metodologia/DECISIONES_ARQUITECTURA.md).

Además, el estudio se complementa con observaciones de campo, entrevistas y visitas a talleres e importadoras para contextualizar los resultados obtenidos.

Los hallazgos permiten identificar patrones de oferta, comportamiento de precios y tendencias observables dentro de este segmento del mercado.

---

## 🎯 Objetivo General

Analizar la oferta de motos de combustión, motos eléctricas, bicicletas eléctricas y patinetes anunciados en La Habana mediante técnicas de recopilación, procesamiento y análisis de datos, con el propósito de identificar patrones de precios, composición del mercado y tendencias relevantes.

---

## 🎯 Objetivo Principal

Analizar el mercado de **motos de combustión**, **motos eléctricas**, **bicicletas eléctricas** y **patinetes** en La Habana para comprender:

- la composición del mercado;
- el comportamiento de los precios;
- la oferta disponible;
- las tendencias observadas.

---

## 🔍 Preguntas de Investigación

1. ¿Cómo está compuesto el mercado de vehículos ligeros anunciados en La Habana?
2. ¿Qué diferencias existen entre los precios de las motos de combustión y las motos eléctricas?
3. ¿Qué marcas aparecen con mayor frecuencia?
4. ¿Qué categorías presentan mayor presencia dentro de la oferta observada?
5. ¿Qué tendencias pueden identificarse a partir de los anuncios publicados?
6. ¿Cómo influyen factores como disponibilidad, mantenimiento y repuestos en las preferencias de los usuarios?

---

## 📊 Dataset

La fuente cuantitativa principal del estudio es Revolico (La Habana).

El dataset consolidado contiene **6.101 anuncios** capturados entre el **10 y el 26 de octubre de 2026**. Cada registro puede incluir información como:

- Título y descripción del anuncio
- Categoría
- Marca
- Modelo
- Precio
- Moneda (`USD` / `CUP`)
- Precio normalizado en USD
- Fecha de captura
- Número de visualizaciones
- URL del anuncio

Archivos principales en [`data_clean/`](data_clean/):

- `anuncios_limpios.csv` / `anuncios_limpios.json` — dataset histórico consolidado.
- `historico_20261010_20261026_clean.csv` / `.json` — histórico del período de captura.
- `manifiesto.json` — conteos y huellas SHA256 de las fuentes.
- `cortes/` — cortes del 22 y 26 de octubre de 2026.
- `motos_combustion/`, `motos_electricas/`, `bicicletas_electricas/`, `patinetes/` — archivos por categoría.

Antes del análisis, los datos fueron sometidos a procesos de limpieza, normalización y validación para garantizar su consistencia. Los precios en USD se usan para las estadísticas; los anuncios en CUP se conservan para el conteo.

---

## 📚 Fuentes de Información

### Fuente cuantitativa

- Revolico (anuncios públicos publicados en La Habana).

### Evidencia cualitativa complementaria

- Entrevistas a usuarios.
- Visitas a talleres.
- Observación en importadoras y puntos de venta.
- Registro fotográfico.

La evidencia cualitativa se utiliza únicamente para complementar e interpretar los resultados obtenidos a partir de los datos recopilados. Solo la fuente **Revolico** se publica como dataset analizable en [`data_clean/`](data_clean/); las entrevistas y visitas se documentan en [`docs/entrevistas/`](docs/entrevistas/) y en [`imagenes/`](imagenes/).

---

## 🗣️ Fuentes Cualitativas

La investigación combina dos tipos de evidencia que se mantienen claramente separadas:

### Datos cuantitativos

- Obtenidos mediante scraping de anuncios públicos de Revolico.
- Almacenados en [`data_raw/`](data_raw/) (cortes crudos) y [`data_clean/`](data_clean/) (dataset procesado).
- Sostienen las estadísticas, métricas y gráficos del estudio.

### Evidencia cualitativa

- **Entrevistas:** normalizadas en [`docs/entrevistas/`](docs/entrevistas/), con archivos para talleres, importadoras y usuarios.
- **Observación directa:** visitas a talleres, tiendas e importadoras.
- **Evidencia fotográfica:** registrada en [`imagenes/`](imagenes/) y documentada en [`imagenes/evidencia_campo.md`](imagenes/evidencia_campo.md).
- **Bitácora:** registro cronológico del trabajo de campo en [`journal/`](journal/).

La evidencia cualitativa se usa para interpretar y contextualizar los resultados cuantitativos. No se emplea para estimar volúmenes de ventas ni para sustituir el dataset de anuncios.

> Estado actual: se dispone de **1 entrevista real** (clasificada de forma tentativa como taller) y **7 fotografías** de campo. Las entrevistas de importadoras y usuarios no están disponibles y se conservan como estructuras vacías documentadas.

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
| Interpretación | Informe, métricas y resumen ejecutivo | [`reports/`](reports/) · [`hands-off/`](hands-off/) |

### Ética y uso responsable

- Se respetan las reglas de `robots.txt` y se aplica una pausa entre peticiones (`--delay`).
- Los textos se sanean para retirar teléfonos y correos antes de almacenar los datasets y los informes.
- Solo se publican datos de anuncios públicos, sin información personal identificable.

---

## 📈 Resultados

Resumen del mercado observado (precios en USD):

| Categoría | Anuncios | Mediana | P25 | P75 | Vistas medianas |
|---|---:|---:|---:|---:|---:|
| Motos de combustión | 1.099 | 2.250 | 1.900 | 2.592,5 | 8 |
| Motos eléctricas | 2.201 | 2.050 | 1.300 | 2.630 | 6 |
| Bicicletas eléctricas | 2.576 | 1.150 | 670 | 1.650 | 7 |
| Patinetes | 225 | 750 | 730 | 800 | 5 |

Los resultados completos se generan automáticamente en:

- [`reports/README.md`](reports/README.md) — informe con composición, precios, demanda, cortes y marcas.
- [`reports/metricas/`](reports/metricas/) — métricas del mercado en JSON y CSV.
- [`reports/graficos/`](reports/graficos/) — gráficos de composición, precios, demanda, evolución y marcas.
- [`hands-off/`](hands-off/) — resumen ejecutivo y entregables.

---

## 📂 Estructura del Proyecto

```text
Mercado-de-Motos/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── data_raw/
│   └── revolico/                     # Cortes crudos depurados (JSON y CSV)
│
├── data_clean/
│   ├── anuncios_limpios.csv          # Dataset histórico consolidado
│   ├── anuncios_limpios.json
│   ├── historico_20261010_20261026_clean.csv
│   ├── historico_20261010_20261026_clean.json
│   ├── manifiesto.json               # Conteos y huellas SHA256 de las fuentes
│   ├── cortes/                       # Cortes del 22 y 26 de octubre de 2026
│   ├── motos_combustion/
│   ├── motos_electricas/
│   ├── bicicletas_electricas/
│   └── patinetes/
│
├── docs/
│   ├── entrevistas/
│   │   ├── README.md
│   │   ├── talleres.json
│   │   ├── importadoras.json
│   │   └── usuarios.json
│   └── metodologia/
│       ├── DECISIONES_ARQUITECTURA.md
│       └── REPORTE_UNIFICACION.md
│
├── imagenes/                         # Registro fotográfico de campo
│   ├── evidencia_campo.md
│   ├── importadoras/
│   ├── talleres/
│   └── tiendas/
│
├── journal/                          # Bitácora de desarrollo
│
├── notebooks/
│   └── eda_motos.ipynb               # Análisis exploratorio
│
├── reports/
│   ├── README.md                     # Informe generado automáticamente
│   ├── graficos/                     # composicion, precios, demanda, evolucion y marcas
│   └── metricas/                     # metricas_mercado.json y metricas_mercado.csv
│
├── hands-off/                        # Resumen ejecutivo y entregables
│
├── presentacion/                     # Material de presentación
│
├── referencias/                      # Bibliografía
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

Lee `data_raw/revolico/` y escribe una salida auxiliar en `data_clean/_etl/`. No sobrescribe el dataset consolidado.

---

### Generar Reportes

```bash
python src/analisis/generar_reporte.py
```

Regenera `reports/README.md`, las métricas en `reports/metricas/` y los gráficos en `reports/graficos/`.

---

### Actualizar Datos

```bash
python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0
```

Descarga un nuevo corte de anuncios y lo guarda en `data_raw/revolico/` con sello temporal.

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
- Control de integridad mediante manifiestos (`data_clean/manifiesto.json`).
- Separación entre datos crudos y datos procesados.

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
- El estudio se limita a los datos disponibles durante el período de captura.
- No existen registros oficiales de ventas que permitan contrastar completamente los resultados obtenidos.
- Algunos factores de decisión de compra solo pueden inferirse parcialmente mediante información cualitativa complementaria.
- La fuente principal es un solo portal de anuncios, con una serie temporal corta.

---

## ✅ Conclusiones

Este proyecto demuestra cómo las técnicas de Ciencia de Datos pueden emplearse para estudiar mercados reales a partir de fuentes de información abiertas.

La combinación de recolección automatizada, limpieza de datos, análisis exploratorio y visualización permite obtener una caracterización cuantitativa del mercado de motos en La Habana. Los resultados constituyen una base para futuras investigaciones relacionadas con movilidad, comportamiento de consumo y análisis de mercados digitales en Cuba.

---

## 👤 Autor

**Harold Ricardo Ponce**

**Asignatura:** Introducción a la Ciencia de los Datos

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Consulta el archivo [`LICENSE`](LICENSE) para más información.
