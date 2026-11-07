# Plan de Refactorización del Scraper de Revolico

**Proyecto:** Análisis del Mercado de Motos en La Habana (ICD)
**Objetivo:** Corregir y reestructurar el scraper existente conservando arquitectura, datos históricos (6.101 registros) y funcionalidades, para que el dataset resultante pueda responder las 30 preguntas de investigación.
**Estado:** Plan de refactorización incremental. **No se modifica código todavía.**

---

## 0. Contexto y decisiones previas

### Categorías principales (requisito nuevo)
Cada anuncio debe pertenecer **exactamente a una** de las tres categorías principales:

| categoria_principal | Descripción |
|---|---|
| `combustion` | Motos de combustión |
| `electric` | Motos eléctricas |
| `scooter` | Patinetes eléctricos |

### Jerarquía de clasificación
```
categoria_principal (combustion | electric | scooter)
  └── subcategoria (slug de Revolico: vehiculos-motos-de-combustion, vehiculos-motos-electricas, etc.)
```

### Reglas de negocio del ETL
- Ningún anuncio puede pertenecer simultáneamente a más de una `categoria_principal`.
- Si un anuncio no se puede asignar a una sola categoría, se descarta o se deja como `sin_clasificar` (nunca se duplica en dos categorías principales).
- Toda métrica, gráfico y análisis debe poder agregarse por: `categoria_principal`, `subcategoria`, `marca`, `modelo`.

---

## 1. Diagnóstico actual por cada una de las 30 preguntas

El tableau siguiente indica qué responde hoy el proyecto y qué falta para responderla con el nuevo scraper/ETL.

| # | Pregunta | Responde hoy | Qué falta con el scraper actual | Cómo la responde el nuevo scraper/ETL |
|---|---|---|---|---|
| 1 | Crecimiento eléctricas vs combustión | Parcial | Serie temporal y municipio | Precio/conteo por `categoria_principal` a lo largo del tiempo, filtrado por `provincia=La Habana` |
| 2 | Tipo más fácil de vender | Parcial (vistas, no ventas) | Ventas efectivas | Proxy: vistas y conteo de anuncios por `categoria_principal`; se declara límite |
| 3 | Marcas con más demanda y que ganaron terreno | Parcial | Serie temporal + municipio | Conteo de anuncios y vistas por `marca` y `categoria_principal`, comparación entre cortes |
| 4 | Diferencia real gasolina vs eléctrica | Parcial | Papeles, mantenimiento, autonomía | Datos del dataset + entrevistas; municipio para precios por zona |
| 5 | Oferta y precios por zona de La Habana | ❌ No responde | **Municipio por anuncio** | `municipio` resuelto desde `MunicipalityType`; agregación de conteo y precio medio por `municipio` |
| 6 | Segmento que crece más (uso) | Parcial (entrevistas) | Campo de uso en anuncios | Proxy por `categoria_principal` + entrevistas; se declara límite |
| 7 | Mercado nuevo vs reventa | Parcial | Campo condición (nueva/usada) | Se declara límite; el scraper no captura condición salvo que aparezca en título |
| 8 | Disposición a pagar (combustión vs eléctrica) | Sí (medianas) | Municipio | Medianas de `precio_usd` por `categoria_principal` y opcional por `municipio` |
| 9 | Rangos de precio por marca | Sí | Municipio opcional | `precio_usd` por `marca` y `categoria_principal` |
| 10 | Efecto del dólar / tipo de cambio | Parcial (tasa oficial) | Serie histórica de tasa + precio | `precio_usd` + tasa BCC del día de extracción (trazabilidad) |
| 11 | Influencia de remesas | ❌ No responde | Dato de remesas | No está en el dataset de anuncios; solo entrevistas. Se declara límite |
| 12 | Qué pesa más al elegir | Parcial (entrevistas) | Ranking uniforme | Solo entrevistas; se declara límite |
| 13 | Costo de cambiar batería eléctrica | Parcial (entrevista) | Precio de batería en dataset | Se declara límite; valor de referencia oficial (Res. 340/2026) como anexo |
| 14 | Impuesto o costo real de importar | Parcial | Arancel exacto no publicado | Se declara límite; valores de referencia oficiales como anexo |
| 15 | Países y canales de importación | Parcial (entrevistas) | País en anuncios | Los anuncios no declaran país; se declara límite |
| 16 | Requisitos: licencia, chapa, seguro, registro | Parcial (ley) | No es dato de anuncio | Anexo legal (Ley 109/2010); no cambia con el scraper |
| 17 | Cambios regulatorios recientes | Sí (ahora con fuentes oficiales) | — | Documentado en `respuestas_fuentes_oficiales.md` |
| 18 | Riesgo de comprar sin papeles | Parcial (entrevistas) | No es dato de anuncio | Solo entrevistas; se declara límite |
| 19 | Piezas que más se rompen | ❌ No responde | Datos de fallas | No está en el dataset; se declara límite |
| 20 | Repuestos más difíciles y demoras | ❌ No responde | Disponibilidad y tiempos | No está en el dataset; se declara límite |
| 21 | Precios de repuestos vs año pasado | ❌ No responde | Serie temporal de repuestos | No está en el dataset; se declara límite |
| 22 | Disponibilidad de talleres vs demanda | ❌ No responde | Censo de talleres | No está en el dataset; se declara límite |
| 23 | Facilidad de encontrar mecánico eléctricas | ❌ No responde | Datos de talleres eléctricos | No está en el dataset; se declara límite |
| 24 | Influencia de apagones | Parcial (1 anuncio) | Dato sistemático | Se declara límite |
| 25 | Dónde carga la gente | ❌ No responde | Dato de carga | No está en el dataset; se declara límite |
| 26 | Autonomía real vs prometida | Parcial (entrevistas) | Medición real | Solo entrevistas; se declara límite |
| 27 | Uso que le da el cliente | Parcial (entrevistas) | Campo de uso | Proxy por `categoria_principal`; se declara límite |
| 28 | Canal que domina (Revolico, FB, Telegram...) | Parcial (solo Revolico) | Otros canales | El dataset es solo Revolico; se declara límite |
| 29 | Garantía y confianza | Parcial (69 anuncios con "garantía") | Escala de garantía | Conteo de anuncios con "garantía" en título/descripción |
| 30 | Mercado en 2-3 años | ❌ No responde | Pronóstico | No hay datos futuros; escenarios cualitativos |

**Resumen:** Con el nuevo scraper/ETL se pueden responder con datos del dataset las preguntas **1, 3, 5, 8, 9, 10, 29** (y parcialmente 2, 4, 6, 7, 27, 28). El resto depende de entrevistas, fuentes legales o datos no presentes en anuncios de Revolico. El plan se centra en hacer que **todas las preguntas que dependen del dataset de anuncios** puedan responderse, especialmente la **5 (por municipio)** que hoy está rota.

---

## 2. Modelo de datos propuesto

### Tablas del almacén analítico (`data/processed/`)

**`dim_categoria_principal`**
- `categoria_principal_id` (PK): `combustion`, `electric`, `scooter`
- `nombre`: Motos de Combustión / Motos Eléctricas / Patinetes Eléctricos

**`dim_subcategoria`**
- `subcategoria_id` (PK): slug de Revolico
- `nombre`
- `categoria_principal_id` (FK → dim_categoria_principal)
- Regla: cada `subcategoria_id` pertenece a exactamente una `categoria_principal_id`

**`dim_provincia`**
- `provincia_id` (PK)
- `nombre`, `slug`, `ref_apollo` (ej. `ProvinceType:1`)

**`dim_municipio`**
- `municipio_id` (PK)
- `nombre`, `slug`, `ref_apollo` (ej. `MunicipalityType:39`)
- `provincia_id` (FK → dim_provincia)

**`dim_marca`**
- `marca_id` (PK)
- `nombre_canonico`, `nombre_original` (para trazabilidad de variantes)

**`dim_modelo`**
- `modelo_id` (PK)
- `marca_id` (FK)
- `nombre_modelo`, `nombre_original`

**`dim_fecha`**
- `fecha_id` (PK): fecha de extracción (ISO)
- `año`, `mes`, `semana_iso`, `dia_semana`

**`fact_anuncio`** (estado actual de cada anuncio activo)
- `anuncio_id` (PK): id de Revolico
- `url`, `titulo`, `descripcion`
- `categoria_principal_id` (FK) — **único por anuncio**
- `subcategoria_id` (FK)
- `provincia_id` (FK, nullable)
- `municipio_id` (FK, nullable)
- `marca_id` (FK, nullable)
- `modelo_id` (FK, nullable)
- `precio_usd`, `precio_cup`, `moneda`
- `precio_valido`, `precio_atipico`
- `vistas`, `imagenes`, `promocion` (booleano)
- `estado_anuncio` (activo/vendido/eliminado)
- `fecha_primera_aparicion`, `fecha_ultima_actualizacion`, `fecha_eliminacion`
- `sello_extraccion`, `archivo_origen`, `hash_contenido`
- `descripcion_vacia`, `municipio_no_identificado`

**`fact_anuncio_version`** (histórico de cambios)
- `version_id` (PK)
- `anuncio_id` (FK), `fecha_id` (FK)
- Campos versionados: `precio_usd`, `moneda`, `ubicacion`, `descripcion`, `estado_anuncio`

**`fact_eliminacion`**
- `eliminacion_id` (PK)
- `anuncio_id` (FK), `fecha_id` (FK de desaparición)

### Agregaciones soportadas
- Por `categoria_principal` → conteo, precio medio/mediana, vistas
- Por `subcategoria` → mismo desglose
- Por `marca` → conteo, precio medio/mediana, vistas, predominio
- Por `modelo` → mismo desglose (dentro de marca)
- Por `municipio` → conteo de anuncios, precio medio (respuesta a Q5)
- Por `fecha` → serie temporal (respuesta a Q1, Q3, Q14, Q15)

### Validación de unicidad de categoría
En el ETL, antes de insertar en `fact_anuncio`:
```
IF COUNT(DISTINCT categoria_principal_id) > 1 FOR SAME anuncio_id THEN
    REJECT / FLAG as ambiguous
END IF
```
Cada `anuncio_id` tiene exactamente una fila en `fact_anuncio` con una sola `categoria_principal_id`.

---

## 3. Plan de refactorización incremental por archivo

### 3.1 `src/scraping/revolico/scrape.py`
**Funciones a corregir:**
- `nombre_lugar(apollo, ref)`: corregir para resolver `{"__ref":"MunicipalityType:N"}` contra catálogo local poblado desde el listado.
- `construir_registro(...)`: guardar `provincia`, `municipio`, `ref_provincia`, `ref_municipio`, `sello_extraccion`, `archivo_origen`, `hash_contenido` en `_scraping`.
- `buscar_pagina(...)`: manejar descubrimiento CSR (endpoint JSON interno o Playwright) si el SSR no devuelve `AdType`.
- `guardar_raw(...)`: asegurar que columnas `provincia`, `municipio` se escriban con valores resueltos.

**Funciones a mantener sin cambios:**
- `limpiar_pii`, `sanear_contactos`, `extraer_next_data`, `apollo_state`, `anuncios_de_estado`, `detalle_anuncio`, `limpiar_pii`, `guardar_json`, `guardar_csv`, `Logger`.

### 3.2 `src/scraping/revolico/common.py`
**Añadir:**
- `resolver_lugar(apollo, ref, catalogo_provincias, catalogo_municipios)`: resuelve refs Apollo a nombre/slug.
- `cargar_catalogo_geo(apollo)`: extrae `ProvinceType` y `MunicipalityType` del Apollo del listado y construye catálogo local.
- Constantes de las 3 categorías principales y mapeo a subcategorías de Revolico.

**Mantener:**
- `clasificar_vehiculo`, `MOTO`, `ELECTRICA_EVID`, `PATINETE`, `BICICLETA`, `detecta_marca`, `url_valida`, `Logger`, `sello`, `ahora_habana`, `guardar_json`, `guardar_csv`.

### 3.3 `src/scraping/revolico/contactos.py`
**Sin cambios.** Sigue eliminando teléfonos y correos antes de guardar.

### 3.4 `src/analisis/etl_mercado.py`
**Funciones a corregir:**
- `cargar()`: leer `provincia`, `municipio`, `ref_provincia`, `ref_municipio` del registro crudo (campos `_scraping` o planos).
- `limpiar()`: aplicar clasificación jerárquica (`categoria_principal` + `subcategoria`); validar unicidad de categoría principal; no descartar por falta de ubicación (usar `NULL` + flag).
- `escribir()`: escribir columnas `provincia`, `municipio`, `ubicacion` (construida, no hardcodeada), `categoria_principal`, `subcategoria`, columnas de trazabilidad al final.

**Eliminar:**
- `"ubicacion": "La Habana"` hardcodeado (línea 197 actual).

### 3.5 `src/analisis/generar_reporte.py`
**Ajuste posible:** si el esquema de salida añade columnas, asegurar que los reportes de métricas (`resumen_mercado.csv`, gráficos) sigan funcionando y agreguen las nuevas agrupaciones por `categoria_principal`, `municipio`, `marca`, `modelo`.

### 3.6 `src/verificar_datos.py`
**Extender:** validar que ningún `anuncio_id` tenga más de una `categoria_principal`; validar que `municipio`/`provincia` no estén hardcodeados; validar trazabilidad (`archivo_origen`, `sello_extraccion` presentes).

---

## 4. Estrategia geográfica (MunicipalityType / ProvinceType)

### Origen de los datos
- El listado `/search` contiene en Apollo 168 `MunicipalityType` y 16 `ProvinceType` (catálogo de filtros).
- Cada anuncio en su detalle (`AdType`) tiene `municipality: {"__ref":"MunicipalityType:N"}` y `province: {"__ref":"ProvinceType:N"}`.

### Flujo de resolución
1. En el primer corte, cargar el catálogo de provincias y municipios desde el Apollo del listado.
2. Al parsear cada anuncio, si `municipality` es `{"__ref":"MunicipalityType:N"}`, buscar `N` en el catálogo local y devolver `nombre` + `slug`.
3. Si el ref no existe en el catálogo, guardar `ref_apollo` original y marcar `municipio_no_identificado = true`.
4. Guardar también `provincia` resuelta y `ref_provincia`.

### ¿Qué es recuperable sin re-scrapear?
- **86 anuncios (1,41 %)** del dataset histórico tienen `municipality.__ref` en el crudo (archivos 22/26 oct). Son recuperables con alta confianza cruzando con el catálogo.
- **6.015 anuncios (98,59 %)** no tienen campo geográfico (archivo 17 oct, formato plano) y sus páginas de detalle están eliminadas. No son recuperables sin re-scrapear.

---

## 5. Trazabilidad y compatibilidad con los 6.101 registros históricos

### Columnas de trazabilidad (nuevas, al final del esquema)
- `archivo_origen`: nombre del JSON crudo de donde provino el anuncio.
- `sello_extraccion`: fecha/hora de la extracción (ISO).
- `hash_contenido`: hash de título+precio+descripción+municipio para detectar cambios.
- `ref_provincia`, `ref_municipio`: refs originales de Apollo para depuración.

### Compatibilidad histórica
- Los 6.101 IDs históricos se mantienen como PK; no se regeneran.
- Todas las columnas existentes (`es_electrica`, `precio_atipico`, `precio_valido`, `marca`, `modelo`, etc.) se conservan.
- El conteo total tras reprocesar los crudos existentes debe seguir siendo 6.101.
- Las métricas clave (medianas por categoría, conteo total, distribución de categorías) deben coincidir antes y después del refactor (prueba de regresión).

---

## 6. Mapa de preguntas de investigación → dataset → respuesta esperada

Agrupo las 30 preguntas por tipo de dato necesario:

### A. Respondibles con el dataset de anuncios (después del refactor)
1. Crecimiento eléctricas vs combustión → `fact_anuncio` por `categoria_principal` y `fecha`.
3. Marcas con más demanda → `dim_marca` + conteo por `categoria_principal`.
5. Oferta y precios por zona → `dim_municipio` + conteo y precio medio por municipio. **(Nueva capacidad clave)**
8. Disposición a pagar → mediana `precio_usd` por `categoria_principal`.
9. Rangos de precio por marca → `dim_marca` + distribución de precios.
10. Efecto del dólar → `precio_usd` + tasa BCC del día de extracción.
29. Garantía y confianza → conteo de anuncios con "garantía" en título/descripción.

### B. Parciales (dataset + entrevistas)
2, 4, 6, 7, 27, 28.

### C. No respondibles con el dataset de anuncios (requieren entrevistas, campo legal o datos externos)
11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30.

### Estimación final
De las 30 preguntas, **7 pueden responderse con datos del dataset de anuncios** (1, 3, 5, 8, 9, 10, 29), **6 parcialmente** (2, 4, 6, 7, 27, 28), y **17 requieren fuentes externas al dataset de Revolico** (entrevistas, Gaceta Oficial, BCC, ONEI). El refactor del scraper maximiza lo recuperable desde el dataset, especialmente la pregunta 5 (municipio) que hoy está rota.

---

## 7. Riesgos y limitaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Listado SSR roto (CSR) | No se descubren anuncios nuevos desde `/search` | Fase 0: detectar API JSON interna o usar Playwright |
| Anuncios históricos sin geografía | 98,59 % sin municipio recuperable | Dejar `NULL` + flag; no inventar |
| Cambios en estructura Apollo de Revolico | Parser rompe | Pruebas de humo en cada ejecución; versión de esquema |
| PII en datos | Violación de privacidad | `sanear_contactos` antes de guardar; no guardar teléfonos/correos |
| Doble clasificación | Anuncio en dos categorías principales | Validación de unicidad en ETL; descartar ambiguos |

---

## 8. Criterios de éxito (qué se verifica al terminar)

- [ ] `nombre_lugar` resuelve `{"__ref":"MunicipalityType:N"}` correctamente.
- [ ] Ningún registro en `fact_anuncio` tiene más de una `categoria_principal_id`.
- [ ] El ETL no hardcodea `"ubicacion": "La Habana"`; lee provincia/municipio reales.
- [ ] El dataset reprocesado conserva 6.101 registros y las métricas clave coinciden.
- [ ] Las nuevas columnas de trazabilidad (`archivo_origen`, `sello_extraccion`, `hash_contenido`) están presentes.
- [ ] Las métricas se pueden agregar por `categoria_principal`, `subcategoria`, `marca`, `modelo` y `municipio`.
- [ ] `verificar_datos.py` pasa con las nuevas validaciones de geografía y unicidad de categoría.

---

**Siguiente paso:** ejecutar la Fase 0 (inspección de tráfico de Revolico para confirmar si existe API JSON/GraphQL interna o si es necesario Playwright) antes de escribir cualquier código. ¿Desea que proceda con la Fase 0 o prefiere ajustar este plan primero?
