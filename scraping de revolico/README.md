# Scraper de Revolico — Mercado de Motos en Cuba

Script de extracción (scraping) de anuncios de **Revolico** para el proyecto de análisis del mercado de motos en Cuba.

## ¿Qué extrae?

Anuncios de la provincia **La Habana** de las categorías (juntas, por defecto):

| Clave | Categoría | Slug |
|-------|-----------|------|
| `motos` | Motos de Combustión | `vehiculos-motos-de-combustion` |
| `electricas` | Motos Eléctricas | `vehiculos-motos-electricas-y-triciclos` |

Opcionalmente se puede añadir:

| Clave | Categoría | Slug |
|-------|-----------|------|
| `bicicletas` | Bicicletas | `vehiculos-bicicletas` |

> **No se incluyen triciclos** (se filtran por título: `triciclo`, `trimoto`).

Por defecto solo se incluyen anuncios **con imagen** (`images=on`, equivalente a `hasImage:true`). Usa `--sin-imagenes` para incluirlos todos.

Filtra por fecha de publicación/actualización **desde la semana pasada hasta hoy**, en hora de **La Habana** (`America/Havana`).

## Campos obtenidos

| Campo | Descripción |
|-------|-------------|
| `id` | Identificador del anuncio |
| `categoria` | Nombre de la categoría |
| `categoria_clave` | Clave interna de la categoría |
| `titulo` | Título del anuncio |
| `precio` | Precio del anuncio |
| `moneda` | Divisa (USD, CUP, etc.) |
| `es_electrica` | Detecta si es eléctrica por palabras clave |
| `url` | Enlace al anuncio |
| `fecha_utc` | Fecha de actualización en UTC |
| `fecha_habana` | Fecha de actualización en hora de La Habana |
| `imagenes` | Nº de imágenes |
| `vistas` | Nº de visitas |
| `promocionado` | Si el anuncio es promocionado |

> No se guardan números de teléfono ni direcciones.

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

```bash
python scraper_revolico.py                     # motos + electricas, 7 días, con imagen
python scraper_revolico.py --dias 14           # últimos 14 días
python scraper_revolico.py --categorias motos  # solo motos de combustión
python scraper_revolico.py --categorias motos,electricas,bicicletas
python scraper_revolico.py --sin-imagenes      # incluir anuncios sin foto
python scraper_revolico.py --max-paginas 5     # limitar páginas por categoría
```

## Salida

Los datos se guardan en `datos/revolico/`:

| Archivo | Descripción |
|---------|-------------|
| `anuncios_revolico_AAAAMMDD_HHMM.csv` | Datos tabulados, para Excel / análisis |
| `anuncios_revolico_AAAAMMDD_HHMM.json` | Datos crudos completos |
| `resumen_revolico_AAAAMMDD_HHMM.md` | Resumen tabulado por categoría (cantidad y precios) |

## Notas técnicas

- El sitio está hecho con Next.js; los datos se leen del objeto `__NEXT_DATA__` (`__APOLLO_STATE__`).
- La paginación se controla con el parámetro `page` (100 anuncios por página).
- Los anuncios vienen ordenados por `updated_on_to_order` descendente, por lo que el scraper se detiene al alcanzar la fecha de corte.
- Se añade una pausa entre peticiones para no saturar el sitio.

## Aviso

Este script es solo para fines académicos (asignatura *Introducción a la Ciencia de Datos*). Respeta los términos de uso de Revolico.
