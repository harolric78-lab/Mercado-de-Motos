# Explicación del pipeline

| Campo | Valor |
|---|---|
| Proyecto | Análisis del Mercado de Motos en La Habana |
| Asignatura | Introducción a la Ciencia de los Datos |
| Fuente principal | Revolico (La Habana) |
| Período de captura | 10–26 de octubre de 2026 |
| Dataset consolidado | 6.101 anuncios |
| Categorías oficiales | Motos de combustión, motos eléctricas, bicicletas eléctricas, patinetes |

---

## 1. Tabla maestra del pipeline

| # | Etapa | Objetivo | Entrada | Proceso | Implementación | Salida | Validación |
|---:|---|---|---|---|---|---|---|
| 1 | Obtención de datos | Descargar anuncios públicos | Revolico (HTML/JSON embebido) | Paginación, extracción de estado, filtrado y deduplicación | `src/scraping/revolico/scrape.py` | `data/raw/revolico/*.json` y `*.csv` | Logs y bloque `_scraping` |
| 2 | Limpieza | Eliminar PII y normalizar campos | Datos crudos | Saneado de contactos, texto, precios, monedas y URLs | `src/contactos.py`, `src/scraping/revolico/common.py` | Campos normalizados | `sanear_contactos()`, `parse_precio()` |
| 3 | Transformación | Consolidar y clasificar | `data/raw/revolico/*.json` | Deduplicación, clasificación y esquema único | `src/analisis/etl_mercado.py` | `data/interim/` | Conteos por categoría |
| 4 | Análisis Exploratorio | Describir el mercado | `data/processed/anuncios_limpios.json` | Composición, precios, marcas y demanda | `notebooks/eda_motos.ipynb` | Tablas descriptivas | Filtros USD y `precio_valido` |
| 5 | Visualización | Comunicar resultados | Dataset consolidado | 5 gráficos automáticos | `src/analisis/generar_reporte.py` | `reports/graficos/*.png` | Exportación a 150 dpi |
| 6 | Interpretación | Generar informe y métricas | Métricas calculadas | Redacción automática del informe | `generar_reporte.py`, `reports/`, `docs/entregables/` | `reports/informe_mercado.md`, métricas | Cifras consistentes |
| 7 | Validación | Garantizar integridad | Dataset consolidado | Comprobaciones y pruebas | `src/verificar_datos.py`, `tests/test_datos.py` | Salida de validación | Total, conteos, IDs y cortes |
| 8 | Evidencia cualitativa | Contextualizar los datos | Trabajo de campo | Entrevistas, observación y fotos | `docs/entrevistas/`, `docs/images/` | JSON y registro fotográfico | Campos vacíos documentados |

---

## 2. Recolección de datos

| Aspecto | Detalle |
|---|---|
| Portal | `https://www.revolico.com` |
| Categoría del sitio | `vehiculos` |
| Provincia | `la-habana` |
| Subcategoría 1 | `vehiculos-motos-de-combustion` |
| Subcategoría 2 | `vehiculos-motos-electricas` |
| Categorías derivadas | `bicicletas_electricas` y `patinetes` (por clasificación) |
| Petición | `GET /search?category=vehiculos&subcategory=<sub>&province=la-habana&page=<n>&images=on` |
| Extracción | `__NEXT_DATA__`, scripts `application/json` o chunks `__APOLLO_STATE__` |
| Objetos leídos | Entradas `AdType:*` del estado Apollo |
| Paginación | Hasta `--max-paginas` por subcategoría |
| Corte de paginación | Se detiene si una página no aporta anuncios nuevos |
| Orden de candidatos | `updatedOnToOrder` descendente |
| Deduplicación temprana | Por `id` |
| Pausa entre peticiones | `time.sleep(--delay)` |
| PII eliminada | `phoneInfo`, `contactInfo`, `email` |
| Textos saneados | `sanear_contactos()` antes de guardar |
| Salida JSON | `data/raw/revolico/revolico_raw_<sello>.json` |
| Salida CSV | `data/raw/revolico/revolico_raw_<sello>.csv` |
| Log | `logs/revolico_<sello>.log` |

### 2.1 Parámetros CLI

| Parámetro | Default | Función |
|---|---:|---|
| `--n` | 30 | Anuncios válidos objetivo |
| `--extra` | 10 | Margen para descartes |
| `--max-paginas` | 3 | Páginas por subcategoría |
| `--max-candidatos` | 150 | Máximo de fichas revisadas |
| `--delay` | 1.0 | Pausa entre peticiones (s) |
| `--sin-imagenes` | — | Incluye anuncios sin foto |
| `--proyecto` | auto | Raíz del proyecto |
| `--salida` | `data/raw/revolico` | Carpeta de salida |

### 2.2 Reglas de clasificación

| Prioridad | Categoría | Evidencia requerida |
|---:|---|---|
| 1 | Patinetes | `patinete` / `patineta` / `monopatin` + evidencia eléctrica |
| 2 | Bicicletas eléctricas | `bicicleta` / `bicimoto` / `ebike` + evidencia eléctrica |
| 3 | Motos de combustión | `combustion` / `gasolina` / `cc` + evidencia de moto |
| 4 | Motos eléctricas | Evidencia de moto + evidencia eléctrica |
| — | Descarte | Accesorio o repuesto sin evidencia fuerte de vehículo completo |

### 2.3 Volumen recolectado

| Captura | Anuncios |
|---|---:|
| 2026-10-17 | 6.246 |
| 2026-10-22 | 46 |
| 2026-10-26 | 52 |
| **Total crudo** | **6.344** |
| Únicos por `id`/`url` | 6.310 |
| Repetidos entre capturas | 34 |

### 2.4 Nota de ética

| Declarado en README | Implementado en código |
|---|---|
| Respeto a `robots.txt` | No se consulta ni parsea `robots.txt` |
| Uso responsable | `User-Agent`, `--delay`, límites de páginas y candidatos |
| Privacidad | Eliminación de PII y saneado de textos |

---

## 3. Limpieza

| Operación | Función | Regla | Resultado |
|---|---|---|---|
| Correos | `EMAIL` | Regex de correo electrónico | Texto sin correos |
| Teléfonos `+53` | `TEL_53` | Prefijo internacional cubano | Texto sin teléfonos |
| Teléfonos etiquetados | `TEL_ETIQUETA` | “teléfono/WhatsApp/celular” + número | Texto sin número |
| Líneas locales | `TEL_LOCAL` | Móviles y líneas cubanas | Texto sin número |
| Acentos | `quitar_acentos()` | Normalización NFKD | Texto comparable |
| Texto general | `norm()` | Minúsculas, sin acentos ni puntuación | Texto normalizado |
| Títulos | `normalizar_titulo()` | NFKC, sin emojis ni caracteres de control | Título legible |
| Precios | `parse_precio()` | Resuelve `,` y `.`; descarta `<= 0` | `float` o `None` |
| Moneda | `detecta_moneda()` | Campo, título o `DESCONOCIDA` | Código de divisa |
| URL | `url_valida()` | Patrón `revolico.com/item/...` | `True` / `False` |
| Marca | `detecta_marca()` | Variantes contra `MARCAS_CANONICAS` | Marca canónica |
| Año | `extraer_anio()` | Años `20xx` | Entero o `None` |
| Cilindrada | `extraer_cc()` | `cc` / `cm3` | Entero o `None` |
| Potencia | `extraer_watts()` | `w` / `watts` | Entero o `None` |
| Voltaje | `extraer_voltaje()` | `v` | Entero o `None` |

> **Nota:** no hay conversión CUP→USD. `precio_usd` solo se llena cuando la moneda es `USD`; los anuncios en CUP se conservan para conteo.

---

## 4. Transformación (ETL)

| Fase | Función | Regla | Resultado |
|---|---|---|---|
| Carga | `cargar()` | Lee todos los `data/raw/revolico/*.json` | Registros con campos internos |
| Deduplicación por ID | `limpiar()` | Conserva el de mayor puntuación | Un registro por `id` |
| Puntuación | `limpiar()` | `(descripción × 2) + vistas + (imágenes × 0.1)` | Registro más completo |
| Deduplicación exacta | `limpiar()` | Mismo título, precio, moneda y día | Sin repeticiones exactas |
| Excepción | `limpiar()` | Títulos genéricos no se deduplican | Se conservan |
| Clasificación | `clasificar()` | Palabras clave en título + descripción | Una de las 4 categorías |
| Esquema | `limpiar()` | 22 campos normalizados | Registro consolidado |
| Escritura | `escribir()` | JSON + CSV + carpetas por categoría | `data/interim/` |

### 4.1 Esquema de salida

| Grupo | Campos |
|---|---|
| Identificación | `id`, `fuente`, `archivo_origen`, `url` |
| Contenido | `titulo`, `descripcion` |
| Categoría | `categoria`, `categoria_clave`, `categoria_nombre`, `categoria_sitio` |
| Precio | `precio`, `moneda`, `precio_usd`, `precio_valido`, `precio_atipico` |
| Fecha | `fecha_iso`, `fecha_habana`, `fecha_dia` |
| Demanda | `vistas`, `imagenes` |
| Marca/modelo | `marca`, `modelo`, `marca_mostrar`, `modelo_mostrar` |
| Ubicación | `ubicacion` |

### 4.2 Dataset consolidado publicado

| Categoría | Anuncios | Porcentaje |
|---|---:|---:|
| Motos de combustión | 1.099 | 18,0 % |
| Motos eléctricas | 2.201 | 36,1 % |
| Bicicletas eléctricas | 2.576 | 42,2 % |
| Patinetes | 225 | 3,7 % |
| **Total** | **6.101** | **100 %** |

---

## 5. Análisis Exploratorio (EDA)

| Análisis | Método | Resultado |
|---|---|---|
| Carga | Pandas sobre `anuncios_limpios.json` | DataFrame consolidado |
| Composición | `value_counts()` por `categoria_nombre` | Conteo y porcentaje |
| Precios | Filtro `moneda == USD`, `precio_usd.notna()`, `precio_valido` | `count`, P25, mediana, P75, media, desviación |
| Marcas | `marca_mostrar != SIN_MARCA` | Top 10 |
| Lectura rápida | Resumen del notebook | 6.101 anuncios; predominio de bicicletas eléctricas |

### 5.1 Estadísticas reales por categoría

| Categoría | Anuncios | n precios | Mediana | P25 | P75 | Promedio | Desviación | Vistas medianas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Motos de combustión | 1.099 | 990 | 2.250 | 1.900 | 2.592,5 | 2.209,87 | 595,03 | 8 |
| Motos eléctricas | 2.201 | 1.996 | 2.050 | 1.300 | 2.630 | 1.979,01 | 949,76 | 6 |
| Bicicletas eléctricas | 2.576 | 2.422 | 1.150 | 670 | 1.650 | 1.183,53 | 528,16 | 7 |
| Patinetes | 225 | 198 | 750 | 730 | 800 | 764,89 | 81,06 | 5 |

### 5.2 Marcas más anunciadas

| Marca | Anuncios |
|---|---:|
| Topmaq | 506 |
| JMD | 227 |
| Mountain | 187 |
| Vedca | 173 |
| Challenger | 170 |
| Yoazaky | 165 |
| Bucatti | 131 |
| Motico | 129 |
| Mishozuki | 95 |
| Halcón | 87 |

---

## 6. Visualización

| Archivo | Contenido | Cálculo |
|---|---|---|
| `reports/graficos/01_composicion.png` | Barras horizontales por categoría | Conteo total |
| `reports/graficos/02_precios.png` | Precio mediano con rango P25–P75 | `statistics.quantiles(n=4)` |
| `reports/graficos/03_demanda.png` | Vistas medianas por categoría | Mediana de vistas |
| `reports/graficos/05_marcas.png` | Top 10 de marcas | Búsqueda en título |
| `reports/graficos/04_evolucion.png` | Comparación de cortes | Conteo por categoría y corte |

| Configuración | Valor |
|---|---|
| Backend | `Agg` |
| Paleta | Fija por categoría (`COLORES`) |
| Formato | PNG |
| Resolución | 150 dpi |

---

## 7. Interpretación y reportes

| Artefacto | Ruta | Contenido |
|---|---|---|
| Informe automático | `reports/informe_mercado.md` | Composición, precios, demanda, cortes y marcas |
| Métricas JSON | `reports/metricas/resumen_mercado.json` | Métricas completas |
| Métricas CSV | `reports/metricas/resumen_mercado.csv` | Resumen tabular |
| Resumen ejecutivo | `docs/entregables/resumen_ejecutivo_20261028.md` | Cifras clave y hallazgos |

### 7.1 Cortes históricos

| Corte | Total | Combustión | Eléctricas | Bicicletas | Patinetes |
|---|---:|---:|---:|---:|---:|
| 2026-10-22 | 30 | 7 | 5 | 14 | 4 |
| 2026-10-26 | 30 | 9 | 3 | 17 | 1 |

---

## 8. Evidencia cualitativa

| Fuente | Archivo | Entrevistas reales | Estado |
|---|---|---:|---|
| Talleres | `docs/entrevistas/talleres.json` | 1 (`TALLER_001`) | Migrada desde Git |
| Importadoras | `docs/entrevistas/importadoras.json` | 0 | Estructura vacía documentada |
| Usuarios | `docs/entrevistas/usuarios.json` | 0 | Estructura vacía documentada |

| Campo del esquema | Descripción |
|---|---|
| `tipo_fuente` | Tipo de fuente cualitativa |
| `id` | Identificador único de la entrevista |
| `fecha` | Fecha de la entrevista |
| `ubicacion` | Lugar |
| `entrevistado` | Nombre o seudónimo |
| `cargo` | Rol del entrevistado |
| `temas` | Categorías tratadas |
| `observaciones` | Notas y aclaraciones |
| `respuestas` | Respuestas estructuradas |
| `texto_original` | Texto fuente conservado |

### 8.1 Evidencia fotográfica

| Carpeta | Fotos | Fecha EXIF |
|---|---:|---|
| `docs/images/importadoras/` | 4 | 2026-10-08 |
| `docs/images/tiendas/` | 3 | 2026-10-08 |
| `docs/images/talleres/` | 0 | — |
| **Total** | **7** | — |

| Separación | Rutas |
|---|---|
| Cuantitativo | `data/raw/`, `data/processed/` |
| Cualitativo | `docs/entrevistas/`, `docs/images/`, `docs/journal/` |

---

## 9. Validación y trazabilidad

| Comprobación | Valor esperado | Implementación |
|---|---|---|
| Total del dataset | 6.101 | `src/verificar_datos.py` |
| Motos de combustión | 1.099 | `src/verificar_datos.py` |
| Motos eléctricas | 2.201 | `src/verificar_datos.py` |
| Bicicletas eléctricas | 2.576 | `src/verificar_datos.py` |
| Patinetes | 225 | `src/verificar_datos.py` |
| IDs vacíos | 0 | `src/verificar_datos.py` |
| IDs duplicados | 0 | `src/verificar_datos.py` |
| Consistencia de categoría | `categoria = categoria_clave` | `src/verificar_datos.py` |
| Corte 2026-10-22 | 30 | `src/verificar_datos.py` |
| Corte 2026-10-26 | 30 | `src/verificar_datos.py` |
| Pruebas | 2 | `tests/test_datos.py` |
| Manifiesto | SHA256 de fuentes | `data/processed/manifiesto.json` |

### 9.1 Fuentes del manifiesto

| Fuente | Total | Verificación |
|---|---:|---|
| `revolico_20261017_raw.json` | 6.246 | SHA256 |
| `revolico_raw_20261022_123941.json` | 46 | SHA256 |
| `revolico_raw_20261026_095603.json` | 52 | SHA256 |

---

## 10. Reproducibilidad

| Comando | Función |
|---|---|
| `git clone https://github.com/harolric78-lab/Mercado-de-Motos.git` | Obtener el repositorio |
| `python -m venv .venv` | Crear entorno virtual |
| `.venv\Scripts\Activate.ps1` | Activar en Windows |
| `source .venv/bin/activate` | Activar en Linux/macOS |
| `pip install -r requirements.txt` | Instalar dependencias |
| `python src/verificar_datos.py` | Validar el dataset |
| `python src/analisis/etl_mercado.py` | Ejecutar el ETL |
| `python src/analisis/generar_reporte.py` | Regenerar métricas y gráficos |
| `python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0` | Actualizar datos |
| `pytest -q` | Ejecutar pruebas |
| `jupyter notebook` | Abrir el notebook EDA |

---

## 11. Artefactos del proyecto

| Artefacto | Ruta |
|---|---|
| Datos crudos | `data/raw/revolico/` |
| Dataset consolidado | `data/processed/anuncios_limpios.*` |
| Cortes históricos | `data/processed/cortes/` |
| Manifiesto | `data/processed/manifiesto.json` |
| Scraper | `src/scraping/revolico/scrape.py` |
| Utilidades y clasificación | `src/scraping/revolico/common.py` |
| Saneamiento de contactos | `src/contactos.py` |
| ETL | `src/analisis/etl_mercado.py` |
| Reportes y gráficos | `src/analisis/generar_reporte.py` |
| Notebook EDA | `notebooks/eda_motos.ipynb` |
| Informe | `reports/informe_mercado.md` |
| Métricas | `reports/metricas/` |
| Gráficos | `reports/graficos/` |
| Entrevistas | `docs/entrevistas/` |
| Fotos | `docs/images/` |
| Validación | `src/verificar_datos.py` |
| Pruebas | `tests/test_datos.py` |

---

## 12. Limitaciones metodológicas

| Limitación | Impacto |
|---|---|
| Los anuncios miden oferta publicada | No representan ventas efectivas |
| Las vistas son un proxy | No equivalen a demanda real |
| Serie temporal corta | Solo tres capturas |
| Una sola fuente cuantitativa | Sesgo de plataforma |
| Sin conversión CUP→USD | Anuncios en CUP fuera de las estadísticas de precio |
| Clasificación por palabras clave | Posibles errores en títulos ambiguos |
| Evidencia cualitativa escasa | 1 entrevista y 7 fotos |
| Sin registros oficiales de ventas | No hay contraste externo |
