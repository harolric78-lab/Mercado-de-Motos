# Journal — Bitácora de Desarrollo

Registro cronológico de avances, decisiones técnicas, modificaciones y entregables del proyecto **Investigación del Mercado de Motos en Cuba**.

---

## 📅 06 de noviembre de 2026 — Cierre de jornada de análisis y documentación

### Objetivos planteados
- Responder las 30 preguntas de investigación con datos oficiales y dataset disponible.
- Corregir el scraper de Revolico para resolver MunicipalityType/ProvinceType (referencias Apollo).
- Mantener municipio y provincia durante todo el ETL (eliminar hardcodeo de "La Habana").
- Generar gráficos basados en datos reales del dataset procesado (6.159 anuncios).
- Crear entregables finales: respuestas a las 30 preguntas, storytelling, plan de refactorización.
- Preparar documentación de cierre de jornada (journal, handoff, reporte técnico).

### Trabajo realizado

#### 1. Corrección del scraper de Revolico
- **`src/scraping/revolico/common.py`**: agregadas constantes `CATEGORIAS_PRINCIPALES` (combustion, electric, scooter), mapeo `SUBCATEGORIAS_POR_CATEGORIA`, y funciones `cargar_catalogo_geo()` y `resolver_lugar_desde_ref()` para resolver referencias Apollo tipo `{"__ref":"MunicipalityType:39"}`.
- **`src/scraping/revolico/scrape.py`**: corregida función `nombre_lugar()` para resolver refs Apollo tipo diccionario; agregados campos de trazabilidad (`sello_extraccion`, `archivo_origen`, `ref_provincia`, `ref_municipio`, `municipio_no_identificado`) en `construir_registro()` y `scrape()`.
- **`src/analisis/etl_mercado.py`**: eliminado hardcodeo de `"ubicacion": "La Habana"`; se leen provincia/municipio del scraping o se resuelven desde refs Apollo crudos; agregadas columnas `categoria_principal`, `provincia`, `municipio`, `ref_provincia`, `ref_municipio`, `municipio_no_identificado`, `sello_extraccion`, `archivo_origen_scraping`; trazabilidad completa preservada.
- **`src/scraping/revolico/contactos.py`**: sin cambios (mantiene saneado de PII).

#### 2. Verificación con fuentes oficiales
- Gaceta Oficial (Ley 109/2010, Res. 171/2026, 172/2026, 175/2026, 340/2026, 197/2026), BCC (tasa 793 CUP/USD), ONEI.
- Confirmado: 5%/20% es Impuesto Especial, no arancel; exención de arancel a eléctricos en canal autorizado; valores de referencia en aduana; requisitos legales (licencia, registro, chapa, revisión técnica).

#### 3. Análisis de las 30 preguntas de investigación
- 5 respondidas con datos (🟢): 4, 8, 9, 17, 27.
- 21 respondidas parcialmente (🟡): 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30.
- 4 sin respuesta (🔴): 5, 11, 20, 22.
- Documentos generados: `respuestas_30_preguntas.md`, `respuestas_17_preguntas_pendientes.md`, `respuestas_21_parciales_completadas.md`, `respuestas_entrevistas_q4_q6_q7_q28.md`, `respuestas_fuentes_oficiales.md`.

#### 4. Storytelling y trabajo de campo
- `storytelling_mercado_motos.md`: relato en 8 capítulos con datos, personajes, escenarios y epílogo de límites.
- `trabajo_campo_resultados.md`: análisis de extracción de municipios (105 de 6.159 anuncios, 1.70%), análisis de entrevistas para Q4/Q6/Q7/Q28, conclusiones sobre las 4 preguntas sin respuesta.

#### 5. Plan de refactorización del scraper
- `plan_refactor_scraper_revolico.md`: arquitectura propuesta, estrategia de descubrimiento, modelo de datos, estrategia geográfica, plan ETL, plan de validación, roadmap por fases, probabilidad de recuperación de municipios sin re-scrapear (1.41%).

#### 6. Gráficos regenerados con datos reales
- Borrados: `01_composicion.png`, `02_precios.png`, `03_demanda.png`, `04_evolucion.png`, `05_marcas.png` (antiguos, no coincidían con dataset actual).
- Generados: `01_composicion.png`, `02_precios.png`, `03_marcas.png`, `04_evolucion.png`, `05_municipios.png` (basados en 6.159 anuncios, 3 categorías principales).
- `reports/informe_mercado.md` reescrito con datos reales y nuevos gráficos.

#### 7. Validación
- `pytest -q`: 2 passed.
- `src/verificar_datos.py`: dataset válido, 6.159 anuncios, sin errores.
- `py_compile`: `common.py`, `scrape.py`, `etl_mercado.py` sin errores de sintaxis.

### Problemas encontrados
- El listado SSR de Revolico ya no contiene `AdType` (descubrimiento de anuncios roto; carga por cliente/CSR).
- `nombre_lugar()` no resolvía refs Apollo `{"__ref":"MunicipalityType:N"}` (provincia/municipio vacíos en crudos).
- ETL hardcodeaba `"ubicacion": "La Habana"` perdiendo información geográfica.
- Solo 1.70% de anuncios tiene municipio identificable (105 de 6.159).
- 4 preguntas de las 30 no pueden responderse con datos disponibles (5, 11, 20, 22).
- Transcripción con `faster-whisper`/`ctranslate2` rota en Python 3.14 (access violation).

### Soluciones aplicadas
- Corregido `nombre_lugar()` para resolver `{"__ref":"..."}` contra catálogo Apollo.
- ETL lee provincia/municipio reales; `ubicacion` construida dinámicamente (no hardcodeada).
- Creado `geo_catalogo.json` con 16 provincias y 48 municipios de La Habana desde Apollo del listado.
- Gráficos regenerados con dataset actual (6.159 anuncios, 3 categorías).
- Documentación de las 30 preguntas con veredicto actualizado (5/21/4).

### Aprendizajes obtenidos
- Los valores de referencia aduaneros (Res. 340/2026) no son precios de mercado; distinguir es clave para no sobreestimar costos.
- El 5%/20% es Impuesto Especial sobre precio de venta, no arancel de importación; confusión común en entrevistas.
- Solo el 41.3% de anuncios declara marca reconocible; el ranking de marcas tiene sesgo de no respuesta.
- Los anuncios miden oferta publicada, no ventas efectivas; las vistas son proxy, no demanda real.

### Estado actual del proyecto
- **Dataset:** 6.159 anuncios válidos, 3 categorías principales, geolocalización parcial (1.70%).
- **ETL:** funcional, con trazabilidad completa y sin pérdida de municipio/provincia.
- **Pruebas:** 2 tests pasando, verificar_datos.py sin errores.
- **Documentación:** 8 documentos de respuestas, storytelling, plan de refactorización, trabajo de campo.
- **Git:** commit `40728cc` subido a `master` (8 archivos de respuestas).

### Próximos pasos recomendados (P0)
1. Ejecutar nuevo corte de Revolico para refrescar el dataset (último: 26/10/2026).
2. Solicitar a Aduana/MFP la tarifa ad-valorem exacta de importación no comercial de motos de combustión.
3. Crear módulo de repuestos en entrevistas para preguntas 19-21.
4. Censo o muestreo de talleres para preguntas 22-23.
5. Añadir campo de condición (nueva/usada) al scraping para pregunta 7.

---

## 📅 06 de noviembre de 2026 — Cierre de jornada (esta entrada)

*Este documento se actualiza al finalizar cada sesión de trabajo. Última actualización: 06/11/2026.*

---

*Validación: `pytest -q` (2 passed), `src/verificar_datos.py` (dataset válido), `py_compile` (sin errores).*
