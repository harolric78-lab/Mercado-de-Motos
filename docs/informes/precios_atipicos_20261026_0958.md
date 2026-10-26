# Precios anormalmente altos (outliers) - Revolico, La Habana

- **Datos de origen:** `revolico_limpio_20261026_095603.json`
- **Generado (La Habana):** 2026-10-26 09:58
- **Metodos:** IQR (factor 1.5) y Z-score (umbral 3.0)

## Resumen por grupo

| Grupo | Anuncios con precio | Mediana | Límite IQR (sup.) | Atípicos |
|-------|--------------------:|--------:|------------------:|---------:|
| Bicicletas electricas | 17 | 1300 | 3025 | 0 |
| Motos de combustion | 6 | 2600 | 3449 | 1 |
| Motos electricas | 4 | 2150 | 3835 | 0 |

## Atípicos más extremos (por encima del límite)

| Grupo | Marca | Título | Precio (USD) | Mediana del grupo | Z-score | Enlace |
|-------|-------|--------|-------------:|------------------:|--------:|--------|
| Motos de combustion | SIN_MARCA | Motos por cantidad | 1670.0 | 2600 | -1.99 | [ver](https://www.revolico.com/item/motos-por-cantidad-58383759) |

