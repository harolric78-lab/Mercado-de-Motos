# Scraper de Revolico — Mercado de Motos en Cuba

Script de extracción (scraping) de anuncios de **Revolico** para el proyecto de análisis del mercado de motos en Cuba.

## ¿Qué extrae?

Anuncios de la provincia **La Habana** de las categorías:

- **Motos de Combustión** (`vehiculos-motos-de-combustion`)
- **Bicicletas** (`vehiculos-bicicletas`) — incluye bicicletas eléctricas

> No se incluyen triciclos.

Filtra por fecha de publicación/actualización **desde la semana pasada hasta hoy**, en hora de **La Habana** (`America/Havana`).

## Campos obtenidos

| Campo | Descripción |
|-------|-------------|
| `id` | Identificador del anuncio |
| `categoria` | Nombre de la categoría |
| `titulo` | Título del anuncio |
| `precio` / `moneda` | Precio y divisa (USD, CUP, etc.) |
| `es_electrica` | Detecta si es eléctrica por palabras clave |
| `url` | Enlace al anuncio |
| `fecha_utc` | Fecha de actualización en UTC |
| `fecha_habana` | Fecha de actualización en hora de La Habana |
| `provincia` / `municipio` | Ubicación |
| `imagenes` / `vistas` | Nº de imágenes y visitas |
| `telefono1` / `telefono2` | Teléfonos de contacto |
| `promocionado` | Si el anuncio es promocionado |

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

```bash
python scraper_revolico.py                 # últimos 7 días
python scraper_revolico.py --dias 14       # últimos 14 días
python scraper_revolico.py --max-paginas 5 # limitar páginas por categoría
```

## Salida

Los datos crudos se guardan en `datos/revolico/`:

- `anuncios_revolico_AAAAMMDD_HHMM.csv` — para Excel / análisis
- `anuncios_revolico_AAAAMMDD_HHMM.json` — datos crudos completos

## Notas técnicas

- El sitio está hecho con Next.js; los datos se leen del objeto `__NEXT_DATA__` (`__APOLLO_STATE__`).
- La paginación se controla con el parámetro `page` (100 anuncios por página).
- Los anuncios vienen ordenados por `updated_on_to_order` descendente, por lo que el scraper se detiene al alcanzar la fecha de corte.
- Se añade una pausa entre peticiones para no saturar el sitio.

## Aviso

Este script es solo para fines académicos (asignatura *Introducción a la Ciencia de Datos*). Respeta los términos de uso de Revolico.
