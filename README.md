# 🏍️ Investigación del Mercado de Motos en Cuba

Proyecto de análisis de datos sobre el mercado de motos en La Habana, desarrollado como parte de la asignatura **Introducción a la Ciencia de Datos**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📖 Descripción

Este repositorio recopila, organiza y analiza anuncios públicos del mercado de motos en La Habana. El dataset público se limita a cuatro categorías oficiales: **motos de combustión**, **motos eléctricas**, **bicicletas eléctricas** (incluye bicimotos) y **patinetes**.

El objetivo es describir la composición de la oferta, comparar precios y medir la demanda relativa a partir de las vistas de los anuncios.

---

## 🎯 Objetivo General

Analizar la oferta publicada de motos en La Habana para describir su composición, sus precios y su demanda relativa.

## 🎯 Objetivos Específicos

1. Determinar el peso de cada una de las cuatro categorías dentro de la oferta.
2. Comparar los precios medianos y los rangos intercuartílicos por categoría.
3. Identificar las marcas con mayor presencia en los anuncios.
4. Medir la demanda relativa mediante las vistas de los anuncios.
5. Generar un informe reproducible y gráficos que apoyen las conclusiones.

---

## ❓ Preguntas de Análisis

1. ¿Cómo se distribuye la oferta entre las cuatro categorías?
2. ¿Qué categorías y marcas concentran más anuncios y más demanda?
3. ¿Cómo se comparan los precios entre categorías?

---

## 🔬 Metodología

1. **Recolección:** anuncios públicos de Revolico (La Habana).
2. **Depuración:** normalización de títulos, precios y monedas; eliminación de duplicados por identificador y por repetición exacta.
3. **Clasificación:** asignación a una de las cuatro categorías oficiales.
4. **Análisis:** estadísticas descriptivas de precios en USD y de vistas por categoría.
5. **Visualización:** composición, precios, demanda, evolución de cortes y marcas.
6. **Interpretación:** lectura de resultados y limitaciones.

La decisión de alcance y las reglas de clasificación están documentadas en [`docs/metodologia/DECISIONES_ARQUITECTURA.md`](docs/metodologia/DECISIONES_ARQUITECTURA.md).

---

## 📚 Fuente de Datos

| Fuente | Descripción |
|---|---|
| 📢 **Revolico** | Anuncios clasificados públicos de La Habana |

Los cortes históricos disponibles son del **22/10/2026** y **26/10/2026**, con 30 anuncios cada uno. El histórico depurado acumula **6.101 anuncios**.

---

## 🗂️ Estructura del Proyecto

```
Mercado-de-Motos/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── data_raw/
│   └── revolico/                 # Cortes crudos depurados
│
├── data_clean/
│   ├── anuncios_limpios.json     # Dataset histórico consolidado
│   ├── anuncios_limpios.csv
│   ├── manifiesto.json
│   ├── cortes/                   # Cortes del 22 y 26 de octubre
│   ├── motos_combustion/
│   ├── motos_electricas/
│   ├── bicicletas_electricas/
│   └── patinetes/
│
├── docs/
│   └── metodologia/              # Decisiones de arquitectura y método
│
├── notebooks/                    # Análisis exploratorio
├── reports/                      # Informe ejecutivo, métricas y gráficos
├── hands-off/                    # Resumen para presentación
├── journal/                      # Bitácora de desarrollo
├── presentacion/                 # Material de presentación
├── referencias/                  # Bibliografía
├── tests/                        # Validación automatizada
│
└── src/
    ├── analisis/
    │   ├── etl_mercado.py        # ETL auxiliar de data_raw a data_clean/_etl
    │   └── generar_reporte.py    # Informe, métricas y gráficos
    ├── scraping/
    │   └── revolico/             # Scraper y utilidades
    ├── contactos.py              # Saneamiento de datos de contacto
    └── verificar_datos.py        # Validación de categorías y conteos
```

---

## 🛠️ Tecnologías Utilizadas

- **Python** — lenguaje principal.
- **Requests** — descarga de datos.
- **BeautifulSoup** — extracción de anuncios.
- **Pandas / NumPy** — manipulación y análisis.
- **Matplotlib / Seaborn** — visualización.
- **Jupyter Notebook** — análisis interactivo.
- **Git y GitHub** — control de versiones.

---

## 📈 Resultados

### Composición del histórico depurado

| Categoría | Anuncios | Precio mediano (USD) | P25 (USD) | P75 (USD) | Vistas medianas |
|---|---:|---:|---:|---:|---:|
| Motos de Combustión | 1.099 | 2.250 | 1.900 | 2.593 | 8 |
| Motos Eléctricas | 2.201 | 2.050 | 1.300 | 2.630 | 6 |
| Bicicletas Eléctricas | 2.576 | 1.150 | 670 | 1.650 | 7 |
| Patinetes | 225 | 750 | 730 | 800 | 5 |

### Último corte (26/10/2026)

| Categoría | Anuncios |
|---|---:|
| Motos de Combustión | 9 |
| Motos Eléctricas | 3 |
| Bicicletas Eléctricas | 17 |
| Patinetes | 1 |
| **Total** | **30** |

### Marcas con más anuncios

| Marca | Anuncios |
|---|---:|
| TOPMAQ | 506 |
| JMD | 227 |
| MOUNTAIN | 187 |
| VEDCA | 173 |
| CHALLENGER | 170 |
| YOAZAKY | 165 |
| BUCATTI | 131 |
| MOTICO | 129 |

### Hallazgos principales

1. **La oferta es mayoritariamente eléctrica.** Las motos eléctricas y las bicicletas eléctricas suman la mayor parte del histórico; las motos de combustión son el bloque minoritario.
2. **Diferencial de precios.** Las motos de combustión tienen el precio mediano más alto (2.250 USD), seguidas por las motos eléctricas (2.050 USD). Las bicicletas eléctricas (1.150 USD) y los patinetes (750 USD) son las opciones de menor precio.
3. **Concentración de marcas.** TOPMAQ lidera con 506 anuncios, seguida por JMD (227) y MOUNTAIN (187).
4. **Demanda relativa.** Las motos de combustión y las bicicletas eléctricas concentran las medianas de vistas más altas (8 y 7), aunque la diferencia con las motos eléctricas (6) es moderada.
5. **Corte reciente.** En el corte del 26/10/2026, las bicicletas eléctricas son la categoría con más anuncios (17), seguidas por las motos de combustión (9).

> Informe completo: [`reports/README.md`](reports/README.md) · Resumen ejecutivo: [`hands-off/`](hands-off/)

---

## ✅ Conclusiones

1. **Composición.** El mercado publicado está dominado por la oferta eléctrica, especialmente por motos y bicicletas eléctricas.
2. **Precios.** La combustión mantiene el precio mediano más alto; las bicicletas eléctricas y los patinetes son las alternativas más económicas.
3. **Marcas.** TOPMAQ, JMD y MOUNTAIN concentran una parte importante de la oferta.
4. **Limitaciones.** Los datos miden oferta publicada y vistas, no ventas cerradas; no permiten afirmar crecimiento de ventas ni causalidad.

---

## 🚀 Trabajo Futuro

- Ampliar la serie temporal con nuevos cortes.
- Incorporar más fuentes públicas de anuncios.
- Automatizar la recolección y la actualización del informe.
- Incorporar modelos de detección de anomalías de precios.
- Desarrollar un tablero interactivo para explorar los datos.

---

## 👤 Autor

**Harold Ricardo Ponce**
Asignatura: *Introducción a la Ciencia de Datos*

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
