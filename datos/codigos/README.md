# Códigos Python utilizados

Copia de los scripts de Python usados en el proyecto **Investigación del Mercado de Motos en Cuba** (asignatura Introducción a la Ciencia de Datos), reunidos en una sola carpeta para consulta y entrega.

> **Nota:** estas copias son de **referencia/entrega**. Los scripts que realmente se ejecutan (y que resuelven rutas y dependencias) viven en [`../../src/`](../../src/).

---

## 1. Recolección de datos (scraping)

| Archivo | Origen | Para qué sirve | Comando |
|---|---|---|---|
| `pipeline.py` | `src/scraping/revolico/` | Pipeline completo de Revolico: scrape → limpieza → métricas → informes → gráficos → README | `python src/scraping/revolico/pipeline.py --n 30` |
| `scrape.py` | `src/scraping/revolico/` | Extrae los anuncios de Revolico (La Habana) a `datos/raw/` | `python src/scraping/revolico/scrape.py` |
| `clean.py` | `src/scraping/revolico/` | Normaliza y filtra (lista blanca, precio mínimo) → `datos/processed/` | `python src/scraping/revolico/clean.py` |
| `analyze.py` | `src/scraping/revolico/` | Métricas de precios por categoría e informe `precios_categorias` | `python src/scraping/revolico/analyze.py` |
| `common.py` | `src/scraping/revolico/` | Utilidades compartidas (rutas, sello de fecha, logger, CSV/JSON) | — |
| `vedca.py` | `src/scraping/` | Catálogo oficial de VEDCA (vedca.cu), 7 vehículos sin precios | `python src/scraping/vedca.py --delay 1.0` |
| `islagrande.py` | `src/scraping/` | Precios en USD de la tienda Islagrande (VEDCA) | `python src/scraping/islagrande.py --delay 1.0` |

## 2. Limpieza y normalización

| Archivo | Origen | Para qué sirve | Comando |
|---|---|---|---|
| `contactos.py` | `src/` | Elimina teléfonos y correos de textos (`sanear_contactos`); usado por scrapers y ETL. También sanea ficheros: `python src/contactos.py fichero.json` | — |
| `limpiar_revolico.py` | `src/limpieza_datos/` | Limpieza de datos crudos de Revolico (monedas, duplicados, categorías) | `python src/limpieza_datos/limpiar_revolico.py` |

## 3. Análisis

| Archivo | Origen | Para qué sirve | Comando |
|---|---|---|---|
| `etl_mercado.py` | `src/analisis/` | ETL consolidado → `datos/clean/anuncios_limpios.json` | `python src/analisis/etl_mercado.py` |
| `informe_mercado.py` | `src/analisis/` | Informe ejecutivo de mercado (`reports/README.md` + gráficos) | `python src/analisis/informe_mercado.py` |
| `precios_atipicos.py` | `src/analisis/` | Detección de precios fuera de rango (IQR + Z-score) | `python src/analisis/precios_atipicos.py --umbral-z 3` |
| `top30_recientes.py` | `src/analisis/` | Tabla de los 30 anuncios más recientes | `python src/analisis/top30_recientes.py` |

## 4. Visualización

| Archivo | Origen | Para qué sirve | Comando |
|---|---|---|---|
| `grafico_evolucion.py` | `src/visualizacion/` | Gráfico de evolución 2024–2026 (eléctricas vs. combustión), SVG sin dependencias externas | `python src/visualizacion/grafico_evolucion.py` |

---

## Requisitos

- Python 3.x con `requests` (scraping) y `matplotlib` (informes y notebook EDA), en [`../../requirements.txt`](../../requirements.txt).
- Ejecutar los comandos desde la **raíz del proyecto** (`Mercado-de-Motos/`).

## Orden típico de ejecución

```bash
python src/scraping/revolico/pipeline.py --n 30     # Revolico (todo el flujo)
python src/scraping/vedca.py                        # Catálogo VEDCA
python src/scraping/islagrande.py                   # Precios Islagrande
python src/analisis/etl_mercado.py                  # ETL consolidado
python src/analisis/informe_mercado.py              # Informe ejecutivo
```
