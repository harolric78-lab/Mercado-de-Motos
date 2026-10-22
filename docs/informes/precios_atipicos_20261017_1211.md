# Precios anormalmente altos (outliers) - Revolico, La Habana

- **Datos de origen:** `revolico_limpio_20261017_1209.json`
- **Generado (La Habana):** 2026-10-17 12:11
- **Metodos:** IQR (factor 1.5) y Z-score (umbral 3.0)

## Resumen por grupo

| Grupo | Anuncios con precio | Mediana | Límite IQR (sup.) | Atípicos |
|-------|--------------------:|--------:|------------------:|---------:|
| otro | 2095 | 1550 | 3350 | 84 |
| Motos electricas | 1379 | 2400 | 4275 | 5 |
| Motos de combustion | 953 | 2300 | 3665 | 95 |
| Bicicletas electricas | 821 | 590 | 1375 | 5 |
| Bicimotos electricas | 287 | 1450 | 3050 | 0 |
| Patinetes electricos | 166 | 750 | 976 | 24 |
| Electricas sin clasificar | 139 | 1490 | 8115 | 5 |
| Motos deportivas de combustion | 100 | 2300 | 3350 | 3 |
| Scooters de combustion | 22 | 2300 | 2765 | 5 |

## Atípicos más extremos (por encima del límite)

| Grupo | Marca | Título | Precio (USD) | Mediana del grupo | Z-score | Enlace |
|-------|-------|--------|-------------:|------------------:|--------:|--------|
| otro | SIN_MARCA | Compro bicimoto de cualquier modelo | 111111 | 1550 | 35.67 | [ver](https://www.revolico.com/item/compro-bicimoto-de-cualquier-modelo-57325467) |
| Motos de combustion | SIN_MARCA | Venta de motor | 50000 | 2300 | 22.59 | [ver](https://www.revolico.com/item/venta-de-motor-58098685) |
| otro | SIN_MARCA | Carro Honda | 48000 | 1550 | 15.1 | [ver](https://www.revolico.com/item/carro-honda-57299625) |
| otro | SIN_MARCA | Dongfeng | 45000 | 1550 | 14.12 | [ver](https://www.revolico.com/item/dongfeng-58134074) |
| otro | SIN_MARCA | Carro | 35000 | 1550 | 10.86 | [ver](https://www.revolico.com/item/carro-57772392) |
| Electricas sin clasificar | SIN_MARCA | DONGFENG ELÉCTRICO! COMO NUEVO (3,000 KM) (2026) | 35000 | 1490 | 5.94 | [ver](https://www.revolico.com/item/dongfeng-electrico-como-nuevo-3000-km-2026-58101501) |
| Electricas sin clasificar | SIN_MARCA | VENDO DONDENG VIGO FULL ELECTRICO 2026 54006023 | 35000 | 1490 | 5.94 | [ver](https://www.revolico.com/item/dondeng-vigofull-electrico-54006023-56952049) |
| Electricas sin clasificar | SIN_MARCA | SE VENDE DONGFENG ELÉCTRICO! | 35000 | 1490 | 5.94 | [ver](https://www.revolico.com/item/se-vende-dongfeng-electrico-58146565) |
| otro | SIN_MARCA | VENDO BESTUNE JOY 03 2026 54O06023 | 33500 | 1550 | 10.37 | [ver](https://www.revolico.com/item/vendo-bestune-joy-03-202654o06023-57518973) |
| Motos de combustion | SIN_MARCA | Moto BMW S1000RR 2025 | 26000 | 2300 | 11.19 | [ver](https://www.revolico.com/item/moto-bmw-s1000rr-2025-57642463) |
| Motos electricas | SIN_MARCA | EN VENTA , Cargador d moto electrica 60v 45 Ah en perfecto e | 20000 | 2400 | 19.58 | [ver](https://www.revolico.com/item/en-venta-cargador-d-moto-electrica-60v-45-ah-en-perfecto-estado-precio-20-000-contactarme-o-whatsapp-al-5-236-58180295) |
| Electricas sin clasificar | SIN_MARCA | Compro baterías de litio de uso | 20000 | 1490 | 3.16 | [ver](https://www.revolico.com/item/compro-baterias-de-litio-de-uso-58126425) |
| Motos deportivas de combustion | KAWASAKI | SE VENDE KAWASAKI NINJA ZX-10R 2021 1000 CC 4 cilindros | 20000 | 2300 | 6.4 | [ver](https://www.revolico.com/item/se-vende-kawasaki-ninja-zx-10r-2021-1000-cc-4-cilindros-57978582) |
| Motos deportivas de combustion | KAWASAKI | KAWASAKI NINJA ZX-10R 2021 | 20000 | 2300 | 6.4 | [ver](https://www.revolico.com/item/kawasaki-ninja-zx-10r-2021-57952746) |
| Electricas sin clasificar | SIN_MARCA | Se vende Vehículo eléctrico exclusivo del año 2025.Modelo Ki | 14000 | 1490 | 2.05 | [ver](https://www.revolico.com/item/se-vende-vehiculo-electrico-exclusivo-del-ano-2025modelo-kimura-57746447) |
| Motos deportivas de combustion | KAWASAKI | Kawasaki ninja zx6r del 2024 | 12500 | 2300 | 3.61 | [ver](https://www.revolico.com/item/kawasaki-ninja-zx6r-del-2024-57641584) |
| Motos de combustion | SIN_MARCA | HONDA CBR 600RR 2012 | 12000 | 2300 | 4.55 | [ver](https://www.revolico.com/item/honda-cbr-600rr-2012-53703576) |
| Motos de combustion | SIN_MARCA | HONDA CBR 600RR 2012 | 12000 | 2300 | 4.55 | [ver](https://www.revolico.com/item/honda-cbr-600rr-2012-57081280) |
| Motos de combustion | SIN_MARCA | Se vende Gelly ck soy la durña 11500 | 11500 | 2300 | 4.31 | [ver](https://www.revolico.com/item/se-vende-gelly-ck-soy-la-durna-11500-58165183) |
| Motos de combustion | SIN_MARCA | Moto combustión IZUKI | 11111 | 2300 | 4.12 | [ver](https://www.revolico.com/item/moto-combustion-izuki-58043456) |
| otro | SIN_MARCA | Bls | 10000 | 1550 | 2.71 | [ver](https://www.revolico.com/item/bls-57601030) |
| Motos de combustion | SIN_MARCA | Vendo o ago negocio honda CBR 600rr 2024 | 10000 | 2300 | 3.6 | [ver](https://www.revolico.com/item/vendo-o-ago-negocio-honda-cbr-600rr-2024-58181939) |
| Motos de combustion | SIN_MARCA | MOTO Suzuki GSXR 750CC 2008 * | 10000 | 2300 | 3.6 | [ver](https://www.revolico.com/item/moto-suzuki-gsxr-750cc-2008-57642484) |
| Motos de combustion | SIN_MARCA | Suzuki GSXR 7 | 10000 | 2300 | 3.6 | [ver](https://www.revolico.com/item/suzuki-gsxr-7-58141793) |
| Motos de combustion | SIN_MARCA | Honda cbr 650r acepto el pago x zelle | 10000 | 2300 | 3.6 | [ver](https://www.revolico.com/item/honda-cbr-650r-58168487) |
| Motos de combustion | SIN_MARCA | Vendo honda CBR 600rr 2024 con solo 5 mil kilómetros interes | 10000 | 2300 | 3.6 | [ver](https://www.revolico.com/item/vendo-honda-cbr-600rr-2024-con-solo-5-mil-kilometros-interesados-al-wassapt-58070414) |
| otro | SIN_MARCA | Rariro Classic Car | 9000 | 1550 | 2.39 | [ver](https://www.revolico.com/item/rariro-classic-car-56627570) |
| Motos de combustion | SIN_MARCA | Vendo o negocio | 8500 | 2300 | 2.88 | [ver](https://www.revolico.com/item/vendo-o-negocio-58118330) |
| Motos de combustion | SIN_MARCA | MOTO DE COMBUSTIBLE | 7000 | 2300 | 2.17 | [ver](https://www.revolico.com/item/moto-de-combustible-58118933) |
| otro | SIN_MARCA | Es tu oportunidad No la dejes pasar Tu mejor inversión Para  | 6600 | 1550 | 1.61 | [ver](https://www.revolico.com/item/es-tu-oportunidad-no-la-dejes-pasar-tu-mejor-inversion-para-tu-comodidad-llama-ya-57004623) |
| Motos de combustion | SIN_MARCA | Tenía #40 | 6500 | 2300 | 1.94 | [ver](https://www.revolico.com/item/tenia-40-57147059) |
| otro | MOUNTAIN | TRICICLO Híbrido MOUNTAIN Potencia, resistencia y capacidad  | 6450 | 1550 | 1.56 | [ver](https://www.revolico.com/item/triciclo-hibrido-mountain-potencia-resistencia-y-capacidad-para-trabajo-pesado-con-panel-solar-57193227) |
| Motos electricas | SIN_MARCA | -Motor eléctrico 2.000 W -Potencia para el transporte y el t | 6200 | 2400 | 4.42 | [ver](https://www.revolico.com/item/motor-electrico-2000-w-potencia-para-el-transporte-y-el-trabajo-diario-sistema-de-baterias-72-v-58-ah-6-baterias-58170524) |
| otro | JMD | JMD CON CABINA Y TECHO - 1800W - 100km - 1000kg - EXTENSOR 5 | 6190 | 1550 | 1.47 | [ver](https://www.revolico.com/item/jmd-con-cabina-y-techo-1800w-100km-1000kg-extensor-5000w-con-tanque-11l-57964403) |
| otro | SIN_MARCA | Vendo en la habana | 6000 | 1550 | 1.41 | [ver](https://www.revolico.com/item/vendo-en-la-habana-58028867) |
| Motos de combustion | MAF | TRICICLO DE COMBUSTIÓN MAF 250CC Potencia, | 6000 | 2300 | 1.7 | [ver](https://www.revolico.com/item/triciclo-de-combustion-maf-250cc-potencia-58095326) |
| Motos de combustion | SIN_MARCA | Etz 250 alemán | 6000 | 2300 | 1.7 | [ver](https://www.revolico.com/item/etz-250-aleman-58179865) |
| Motos de combustion | MAF | TRICICLO DE COMBUSTIÓN MAF 250CC | 6000 | 2300 | 1.7 | [ver](https://www.revolico.com/item/triciclo-de-combustion-maf-250cc-58175749) |
| Motos de combustion | MAF | TRICICLO DE COMBUSTIÓN MAF 250CC | 6000 | 2300 | 1.7 | [ver](https://www.revolico.com/item/triciclo-de-combustion-maf-250cc-58046423) |
| Motos de combustion | SIN_MARCA | Motoneta | 6000 | 2300 | 1.7 | [ver](https://www.revolico.com/item/motoneta-58030694) |

