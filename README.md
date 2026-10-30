# 🏍️ Investigación del Mercado de Motos en Cuba

Proyecto de análisis de datos sobre la oferta publicada de motos en La Habana, desarrollado para la asignatura **Introducción a la Ciencia de los Datos**. Integra recolección automatizada, limpieza, análisis exploratorio y generación reproducible de reportes.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📖 Presentación

La movilidad en Cuba enfrenta restricciones de transporte público, costos de combustible y limitaciones para importar vehículos. En ese contexto, las motos se consolidan como una alternativa cotidiana de desplazamiento y de actividad económica.

El mercado combina **motos de combustión**, asociadas a mayor potencia y a la disponibilidad de repuestos, con **motos eléctricas**, favorecidas por el menor costo de operación y la recarga domiciliaria. A ellas se suman los **patinetes**, opciones de menor precio orientadas a trayectos cortos. La convivencia de estas tecnologías, junto con la importación y el mercado informal, produce un panorama de precios y oferta que cambia con rapidez.

Este proyecto estudia ese panorama a partir de anuncios públicos y de evidencia cualitativa de campo. Su propósito es describir la composición del mercado, comparar el comportamiento de los precios y aportar una base documentada y replicable para futuras investigaciones.

---

## 🎯 Objetivo Principal

Analizar el mercado de **motos de combustión**, **motos eléctricas** y **patinetes** en Cuba para comprender:

- la composición del mercado;
- el comportamiento de los precios;
- la oferta disponible;
- las tendencias observadas.

> El dataset publicado conserva además la categoría `bicicletas_electricas` (que agrupa bicimotos), utilizada para clasificar los anuncios de origen. Su tratamiento se detalla en la metodología y en [`docs/metodologia/DECISIONES_ARQUITECTURA.md`](docs/metodologia/DECISIONES_ARQUITECTURA.md).

---

## ❓ Preguntas de Investigación

| # | Pregunta |
|---|---|
| 1 | ¿Cómo está compuesto el mercado cubano de motos? |
| 2 | ¿Cómo se comporta el precio de las motos de combustión frente al de las motos eléctricas? |
| 3 | ¿Qué marcas tienen mayor presencia? |
| 4 | ¿Qué factores influyen en las decisiones de compra? |
| 5 | ¿Qué problemas reportan usuarios y talleres? |
| 6 | ¿Cómo afecta la disponibilidad de repuestos? |

---

## 📚 Fuentes de Datos

| Fuente | Datos recopilados | Utilidad |
|---|---|---|
| Revolico (La Habana) | anuncios, precios, monedas, marcas, modelos y vistas | análisis de oferta y precios |
| Entrevistas y visitas de campo | experiencias, preferencias y hábitos de compra | análisis del comportamiento |
| Talleres e importadoras | repuestos, mantenimiento y disponibilidad | análisis técnico y operativo |

Solo la fuente **Revolico** se publica como dataset analizable en [`data_clean/`](data_clean/). Las entrevistas y visitas de campo se documentan como evidencia cualitativa en [`journal/`](journal/) y en el registro fotográfico de [`imagenes/`](imagenes/).

---

## 🔬 Metodología

```
Recolección
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
| Recolección | Descarga de anuncios públicos de Revolico en La Habana | [`src/scraping/revolico/scrape.py`](src/scraping/revolico/scrape.py) |
| Limpieza | Saneamiento de datos de contacto, normalización de títulos, precios y monedas | [`src/contactos.py`](src/contactos.py) · [`src/analisis/etl_mercado.py`](src/analisis/etl_mercado.py) |
| Transformación | Clasificación en categorías, deduplicación y consolidación del histórico | [`src/analisis/etl_mercado.py`](src/analisis/etl_mercado.py) |
| Análisis Exploratorio | Estadísticas descriptivas de precios y vistas por categoría | [`notebooks/eda_motos.ipynb`](notebooks/eda_motos.ipynb) |
| Visualización | Gráficos de composición, precios, demanda, evolución y marcas | [`src/analisis/generar_reporte.py`](src/analisis/generar_reporte.py) |
| Interpretación | Informe, métricas y resumen ejecutivo | [`reports/`](reports/) · [`hands-off/`](hands-off/) |

---

## 📂 Estructura del Proyecto

```
Mercado-de-Motos/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── data_raw/
│   └── revolico/                     # Cortes crudos depurados (JSON y CSV)
│
├── data_clean/
│   ├── anuncios_limpios.json         # Dataset histórico consolidado
│   ├── anuncios_limpios.csv
│   ├── manifiesto.json               # Conteos y huellas SHA256 de las fuentes
│   ├── cortes/                       # Cortes del 22 y 26 de octubre de 2026
│   ├── motos_combustion/
│   ├── motos_electricas/
│   ├── bicicletas_electricas/
│   └── patinetes/
│
├── docs/
│   └── metodologia/
│       └── DECISIONES_ARQUITECTURA.md
│
├── imagenes/                         # Registro fotográfico de campo
│   ├── Importadora de motos/
│   └── Tiendas de motos electricas y de combustion/
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
├── journal/                          # Bitácora de desarrollo
├── presentacion/                     # Material de presentación
├── referencias/                      # Bibliografía
│
├── src/
│   ├── contactos.py                  # Saneamiento de datos de contacto
│   ├── verificar_datos.py            # Validación de integridad del dataset
│   ├── analisis/
│   │   ├── etl_mercado.py            # Limpieza, clasificación y deduplicación
│   │   └── generar_reporte.py        # Métricas, gráficos e informe
│   └── scraping/
│       └── revolico/
│           ├── common.py             # Utilidades y reglas de clasificación
│           └── scrape.py             # Scraper de anuncios
│
└── tests/
    └── test_datos.py                 # Pruebas de validación
```

---

## ⚙️ Cómo Ejecutar el Proyecto

**Requisitos:** Python 3.10 o superior y Git.

```bash
# 1. Situarse en la raíz del proyecto
cd Mercado-de-Motos

# 2. Crear y activar un entorno virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar validaciones

```bash
python src/verificar_datos.py
```

Comprueba el total del histórico, los conteos por categoría, los identificadores y los cortes históricos.

### Ejecutar el ETL (opcional)

```bash
python src/analisis/etl_mercado.py
```

Lee `data_raw/revolico/` y escribe una salida auxiliar en `data_clean/_etl/`. No sobrescribe el dataset consolidado de `data_clean/`.

### Generar reportes

```bash
python src/analisis/generar_reporte.py
```

Regenera `reports/README.md`, las métricas en `reports/metricas/` y los gráficos en `reports/graficos/`.

### Actualizar los datos (opcional)

```bash
python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0
```

Descarga un nuevo corte de anuncios y lo guarda en `data_raw/revolico/` con sello temporal.

### Ejecutar pruebas

```bash
pytest -q
```

### Abrir notebooks

```bash
jupyter notebook
```

---

## 📊 Resultados y Reportes

Los resultados se generan automáticamente y no se duplican en este README. Se encuentran en:

- [`reports/README.md`](reports/README.md) — informe completo con composición, precios, demanda, cortes y marcas.
- [`reports/metricas/`](reports/metricas/) — métricas del mercado en JSON y CSV.
- [`reports/graficos/`](reports/graficos/) — gráficos de composición, precios, demanda, evolución y marcas.
- [`hands-off/`](hands-off/) — resumen ejecutivo y entregables.

Estos archivos incluyen métricas, gráficos, estadísticas descriptivas, análisis por categoría y conclusiones.

---

## 🔍 Trazabilidad y Reproducibilidad

- **Procedencia de los datos:** anuncios públicos de Revolico (La Habana), recolectados en cortes fechados y conservados sin datos de contacto.
- **Fuentes utilizadas:** Revolico como fuente cuantitativa; entrevistas, visitas de campo y registros de talleres e importadoras como evidencia cualitativa documentada.
- **Proceso de limpieza:** normalización de títulos, precios y monedas; eliminación de duplicados por identificador y por repetición exacta; clasificación mediante evidencia positiva en título y descripción.
- **Integridad:** [`data_clean/manifiesto.json`](data_clean/manifiesto.json) registra los conteos y las huellas SHA256 de los archivos de origen.
- **Versionado:** el proyecto se mantiene con Git y GitHub; la bitácora de cambios y decisiones está en [`journal/`](journal/).
- **Replicación:** los scripts son deterministas sobre el dataset publicado y las dependencias están fijadas en [`requirements.txt`](requirements.txt). Cualquier persona puede validar, regenerar métricas y reproducir los gráficos con los comandos de la sección anterior.
- **Privacidad:** los textos se sanean para retirar teléfonos y correos antes de almacenar los datasets y los informes.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python | desarrollo principal |
| Pandas | procesamiento de datos |
| NumPy | análisis numérico |
| Matplotlib | visualizaciones |
| Seaborn | gráficos |
| BeautifulSoup | scraping |
| Requests | descarga de páginas |
| Jupyter | exploración |
| Git/GitHub | control de versiones |

---

## ⚠️ Limitaciones

- **Los anuncios no equivalen a ventas.** El dataset mide oferta publicada y vistas, no transacciones cerradas.
- **Sesgos en entrevistas.** Las muestras son pequeñas y dependen de la disposición y el recuerdo de las personas entrevistadas.
- **Sesgos de participación.** Las entrevistas y los canales informales, como Telegram, sobrerrepresentan a usuarios activos y con mayor acceso digital.
- **Disponibilidad limitada de datos.** La fuente principal es un solo portal de anuncios, con una serie temporal corta y sin registros oficiales de ventas.

---

## 👤 Autor

**Harold Ricardo Ponce**

Asignatura: *Introducción a la Ciencia de los Datos*

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
