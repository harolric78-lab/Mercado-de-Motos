# 🏍️ Investigación del Mercado de Motos en Cuba

Proyecto de análisis de datos sobre el mercado de motos (eléctricas y de combustión) en Cuba, desarrollado como parte de la asignatura **Introducción a la Ciencia de Datos**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📖 Descripción

Este repositorio recopila, organiza y analiza datos del mercado de motos en Cuba con el fin de comprender su comportamiento, la evolución de las motos eléctricas frente a las de combustión y la detección de precios fuera de lo normal. El proyecto integra información obtenida de anuncios, encuestas, grupos especializados, importadoras y talleres.

---

## 🎯 Objetivo General

Analizar el mercado de motos en Cuba para describir su evolución y detectar patrones de precios anormalmente altos, comparando las motos eléctricas con las de combustión.

## 🎯 Objetivos Específicos

1. Determinar cómo está creciendo el mercado de motos eléctricas frente al de combustión.
2. Identificar las motos con precios anormalmente altos dentro del mercado cubano.
3. Caracterizar las fuentes de oferta (importadoras, talleres y anuncios) y su impacto en los precios.
4. Construir una base de datos limpia y comparable a partir de fuentes heterogéneas.
5. Generar gráficos y conclusiones que respondan a las preguntas de análisis.

---

## ❓ Preguntas de Análisis

1. ¿Cómo está creciendo el mercado de motos eléctricas frente al de combustión?
2. ¿Qué motos tienen precios anormalmente altos?

---

## 🔬 Metodología

El proyecto sigue un flujo de trabajo típico de ciencia de datos:

1. **Recolección de datos:** obtención de datos desde anuncios, encuestas, grupos especializados, importadoras y talleres.
2. **Limpieza y normalización:** tratamiento de valores faltantes, homogenización de marcas, modelos y monedas, y eliminación de duplicados.
3. **Análisis exploratorio (EDA):** estadísticas descriptivas, distribuciones de precios y comparación entre tipos de moto.
4. **Visualización:** generación de gráficos que apoyan las conclusiones.
5. **Interpretación:** redacción de resultados, conclusiones y trabajo futuro.

---

## 📚 Fuentes de Datos

| Fuente | Descripción | Cantidad |
|--------|-------------|----------|
| 📢 **Revolico** | Anuncios clasificados de La Habana (30 más recientes) | 30 |
| 🏭 **VEDCA** | Catálogo oficial de fábrica (vedca.cu), sin precios publicados | 7 vehículos |
| 🛒 **Islagrande** | Tienda online de VEDCA con precios en USD | 14 precios válidos |
| 📝 **Entrevistas** | Entrevistas a vendedores y propietarios | 1 |
| 👥 **Grupos especializados** | Grupos de Telegram u otros foros | — |
| 🛠️ **Talleres** | Talleres de reparación y venta | — |

> **Corte del 26/10/2026:** Revolico 30 anuncios — 8 de combustión, 21 eléctricos (incluye bicicletas) y 1 patinete. VEDCA publica 7 vehículos en catálogo **sin precios** (la venta es por tienda o fábrica). Islagrande lista 14 precios válidos entre **601 y 2 096 USD**.

> Los datos crudos y limpios se almacenan en [`datos/`](datos/) (por fuente) y en [`data/`](data/) (pipeline automatizado `raw/ → processed/ → clean/`).

---

## 🗂️ Estructura del Proyecto

```
Mercado-de-Motos/
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/                       # Documentación del proyecto
│   ├── metodologia/            # Descripción del método de trabajo
│   └── informes/               # Informes parciales y finales (fechados)
│
├── datos/                      # Datasets por fuente (versionados)
│   ├── revolico/               # Anuncios extraídos de Revolico
│   ├── limpios/                # Datos limpios y normalizados
│   ├── entrevistas/            # Entrevistas cualitativas
│   ├── tiendas_online/         # Precios de tiendas (Islagrande)
│   ├── importadoras/           # Importadoras (carpeta general, pendiente)
│   ├── importadora_vedca/      # Catálogo VEDCA (y solimport/pendiente)
│   ├── telegram/               # Grupos especializados (pendiente)
│   ├── talleres/               # Datos de talleres (pendiente)
│   ├── codigos/                # Scripts Python utilizados (copias de entrega)
│   └── _reemplazados/          # Versiones anteriores reemplazadas
│
├── data/                       # Pipeline automatizado de la skill revolico-scraper
│   ├── raw/                    # Datos crudos (evidencia)
│   ├── processed/              # Datos procesados
│   └── clean/                  # Datos consolidados
│
├── imagenes/                   # Fotografías de referencia
│
├── graficos/                   # Gráficos generados por el análisis
├── reports/                    # Informe ejecutivo de mercado + gráficos
├── journal/                    # Bitácora de desarrollo
├── hands-off/                  # Entregables listos para presentar
│
├── notebooks/                  # Notebooks de análisis (EDA)
│
├── src/                        # Código fuente del proyecto
│   ├── scraping/               # revolico/, vedca.py, islagrande.py
│   ├── limpieza_datos/         # Limpieza y normalización
│   ├── analisis/               # Análisis estadístico (ETL, outliers, top30)
│   └── visualizacion/          # Generación de gráficos
│
├── presentacion/               # Presentación del proyecto
│
└── referencias/                # Bibliografía y material de referencia
```

---

## 🛠️ Tecnologías Utilizadas

- **Python** — lenguaje principal del análisis.
- **Requests** — descarga de datos desde la web.
- **BeautifulSoup** — extracción (scraping) de anuncios.
- **Pandas / NumPy** — manipulación y análisis de datos.
- **Matplotlib / Seaborn** — visualización de datos.
- **Jupyter Notebook** — desarrollo interactivo del análisis.
- **Git y GitHub** — control de versiones.

---

## 📈 Resultados

### Motos más demandadas por categoría (Revolico — La Habana)

Datos de los **30 anuncios más recientes** publicados en Revolico (La Habana). La marca "más demandada" es la de mayor cantidad de anuncios en su categoría.

| Categoría | Marca más demandada | Rango de precio (USD) | Anuncios | Enlace Revolico |
|-----------|---------------------|----------------------:|---------:|-----------------|
| Moto de combustión | ITALY | 1 670 – 2 800 | 8 | [ver](https://www.revolico.com/item/motos-por-cantidad-58383759) |
| Moto eléctrica | TORVAN | 1 680 – 2 580 | 4 | [ver](https://www.revolico.com/item/moto-electrica-volta-x-57960251) |
| Bicicleta eléctrica | VEDCA | 450 – 2 000 | 17 | [ver](https://www.revolico.com/item/bicimoto-58121135) |
| Patinete eléctrico | — | 340 | 1 | [ver](https://www.revolico.com/item/patineta-electrica-pegable-57907517) |


### Hallazgos principales (corte del 26 de octubre de 2026)

1. **Las motos eléctricas dominan la oferta publicada.** En el corte histórico de 6 249 anuncios (10–22 de octubre), el **82,0 %** de la oferta es eléctrica (motos eléctricas 37,1 %, bicimotos 27,9 %, bicicletas eléctricas 13,4 % y patinetes 3,6 %) frente al **18,0 %** de combustión. En los 30 anuncios más recientes la proporción se mantiene: 21 eléctricos vs. 8 de combustión.
2. **Diferencial de precio.** En los 30 anuncios más recientes, la mediana de combustión es **2 600 USD** frente a **1 450 USD** de las eléctricas (rango total: 340–2 800 USD). En el corte histórico: 2 220 USD (combustión) vs. 2 000 USD (eléctricas).
3. **Precios atípicos.** El detector IQR/Z-score del 26/10 **no encontró precios extremadamente altos**: el único anuncio marcado es un lote de combustión a **1 670 USD**, por debajo del rango habitual del grupo. El máximo del corte histórico es 6 600 USD (motos eléctricas).
4. **Marcas dominantes.** Combustión: **ITALY** (RX Combat, 50 anuncios). Eléctricas: **TOPMAQ** (181), seguida de VEDCA (110) y MOUNTAIN (103). Bicimotos y patinetes: **JMD**. En los anuncios más recientes también aparecen TORVAN y VEDCA.
5. **Precio de fábrica vs. mercado.** VEDCA **no publica precios** en su catálogo (7 vehículos): la referencia de tienda la da Islagrande, con eléctricas entre **601 y 2 096 USD**, y una Hongli HL-125 de 125 cc a 1 474 USD.
6. **Rentabilidad.** Con costo operativo del 10 %, el arbitraje local es estrecho: el ROI supera el 20 % solo comprando por debajo del P10 (TOPMAQ 28,1 %; Suzuki GN125 23,4 %). Detalle en [`reports/README.md`](reports/README.md).

> Informes completos: [`docs/informes/`](docs/informes/) · Entregable ejecutivo: [`hands-off/`](hands-off/)

---

## ✅ Conclusiones

1. **¿Cómo está creciendo el mercado de motos eléctricas frente al de combustión?** Sobre la oferta publicada, las eléctricas ya son **cuatro de cada cinco anuncios** (82 % vs. 18 %) y mantienen esa proporción en los anuncios más recientes. La evidencia es de **oferta activa**, no de ventas cerradas: no hay todavía una serie temporal de transacciones que permita medir el crecimiento de las ventas.
2. **¿Qué motos tienen precios anormalmente altos?** En el corte reciente **no hay precios extremadamente altos**: el rango llega a 2 800 USD y el único atípico detectado está por debajo (1 670 USD). En el corte histórico el máximo es 6 600 USD en una moto eléctrica, sin cola de precios fuera de control.
3. **Síntesis de mercado.** El mercado de La Habana lo mueven **TOPMAQ** (eléctricas) y **JMD** (bicimotos/patinetes) en volumen, e **ITALY** en combustión. Los precios son altos y estables; la oportunidad de negocio está en **comprar por debajo del P10**, **importar** o **diferenciarse con servicio**, no en el arbitraje directo.

> Desarrollo completo en [`reports/README.md`](reports/README.md) (informe ejecutivo con rankings, precios, rentabilidad y riesgos).

---

## 🚀 Trabajo Futuro

- Ampliar el tamaño de la muestra y diversificar las fuentes de datos.
- Incorporar datos de grupos especializados (Telegram y otros foros).
- Automatizar la recolección mediante scraping periódico.
- Incorporar modelos de detección de anomalías para precios.
- Desarrollar un tablero (dashboard) interactivo para explorar los datos.

---

## 👤 Autor

**Harold Ricardo Ponce**
Asignatura: *Introducción a la Ciencia de Datos*

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
