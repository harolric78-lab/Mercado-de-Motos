# Hand-off — Estado Técnico del Proyecto

**Actualizado:** 06 de noviembre de 2026  
**Proyecto:** Análisis del Mercado de Motos en La Habana (Introducción a la Ciencia de los Datos)  
**Repositorio:** `Mercado-de-Motos` (repositorio Git anidado dentro de `Proyecto de ICD Motos en cuba (2)`)  
**Rama activa:** `master`  
**Último commit:** `40728cc` — docs: agregar respuestas de las 30 preguntas de investigación con datos oficiales y dataset  

---

## 1. Resumen Ejecutivo

El proyecto tiene un pipeline cuantitativo terminado (scraping, limpieza, ETL, validación, métricas, gráficos e informe) y un módulo cualitativo con 30 entrevistas (25 compradores, 4 talleres, 1 importadora). De las 30 preguntas de investigación, **26 están respondidas** (5 completamente, 21 parcialmente) y **4 quedan sin respuesta** (5, 11, 20, 22) por falta de datos de campo.

El scraper de Revolico fue corregido para resolver referencias Apollo de municipio/provincia y el ETL ya no hardcodea la ubicación. Los gráficos se regeneraron con datos reales del dataset (6.159 anuncios, 3 categorías principales).

---

## 2. Completado

| Área | Estado | Notas |
|---|---|---|
| Scraping Revolico | Terminado | 3 cortes: 17, 22 y 26 de octubre de 2026 |
| Dataset consolidado | Terminado | 6.159 anuncios, 3 categorías principales |
| ETL y validación | Terminado | `src/analisis/etl_mercado.py`, `src/verificar_datos.py` |
| Métricas y gráficos | Terminado | 5 gráficos regenerados con datos reales |
| Informe | Terminado | `reports/informe_mercado.md` actualizado |
| Entrevistas | Terminado | 25 compradores, 4 talleres, 1 importadora (30 totales) |
| Cobertura de preguntas | Terminado | 26/30 respondidas (5 🟢, 21 🟡, 4 🔴) |
| Fuentes oficiales | Verificadas | Gaceta Oficial, BCC, ONEI (06/11/2026) |
| Documentación de respuestas | Terminada | 8 documentos en `docs/entregables/` |
| Storytelling | Terminado | `docs/entregables/storytelling_mercado_motos.md` |
| Plan de refactorización | Terminado | `docs/entregables/plan_refactor_scraper_revolico.md` |

### Correcciones implementadas
- `nombre_lugar()` resuelve refs Apollo `{"__ref":"MunicipalityType:N"}`.
- ETL lee provincia/municipio reales; eliminado hardcodeo de `"La Habana"`.
- Columnas de trazabilidad: `sello_extraccion`, `archivo_origen`, `ref_provincia`, `ref_municipio`, `municipio_no_identificado`.
- Catálogo geo: `data/raw/revolico/geo_catalogo.json` (16 provincias, 48 municipios La Habana).
- Gráficos: 5 regenerados con datos actuales del dataset.

### Integraciones configuradas
- BCC: tasa oficial 793 CUP/USD (06/11/2026).
- Gaceta Oficial: Res. 340/2026 (valores referencia), 172/2026 (impuesto especial), 175/2026 (servicios aduana), 197/2026 (tarifa comercial), 171/2026 (valores mínimos usados).
- Ley 109/2010 (Edición 2026): requisitos legales (licencia, registro, chapa, revisión técnica).

---

## 3. En Progreso

| Tarea | Estado | Riesgo | Bloqueador |
|---|---|---|---|
| Nuevo corte de Revolico | Pendiente | Medio | Dataset sin actualizar desde 26/10/2026 |
| Campo municipio en scraping | Pendiente | Alto | Revolico SSR no expone municipio; requiere CSR o API interna |
| Campo condición (nueva/usada) | Pendiente | Medio | No existe en dataset actual |
| Tarifa ad-valorem combustión | Pendiente | Alto | No publicada en Gaceta; requiere consulta a Aduana/MFP |
| Módulo de repuestos | Pendiente | Medio | No hay datos de disponibilidad/demora |
| Censo de talleres | Pendiente | Alto | 4 talleres entrevistados, identidad no confirmada |

### Riesgos detectados
- **Descubrimiento de anuncios roto:** el listado SSR de Revolico ya no contiene `AdType`; los anuncios cargan por cliente (CSR). El scraper actual no puede descubrir nuevos anuncios automáticamente.
- **Datos históricos sin geolocalización:** 98.3% de anuncios (6.054 de 6.159) no tienen municipio.
- **Transcripción con faster-whisper rota:** acceso violation en Python 3.14; solo Vosk funciona con precisión limitada.
- **Muestra cualitativa pequeña:** 25 compradores, 4 talleres (identidad no confirmada), 1 importadora; no representativa estadísticamente.

---

## 4. Pendiente

### Próximas tareas prioritarias (P0)
1. **Ejecutar nuevo corte de Revolico** para refrescar el dataset (medir crecimiento, variación de precios, reventa).
2. **Solicitar a Aduana o MFP la tarifa ad-valorem exacta** de importación no comercial de motos de combustión (pregunta 14).
3. **Crear módulo de repuestos** en entrevistas a talleres y compradores (preguntas 19-21).
4. **Censo o muestreo de talleres** por municipio para medir capacidad y cobertura (preguntas 22-23).
5. **Añadir campo de condición (nueva/usada)** al scraping (pregunta 7).

### Mejoras sugeridas
- Implementar scraping con Playwright o reverse-engineering del endpoint cliente de Revolico para descubrimiento de anuncios.
- Añadir campo de país de importación en el scraping (pregunta 15).
- Añadir pregunta directa de remesas al cuestionario de entrevistas (pregunta 11).
- Implementar geolocalización de direcciones en anuncios para preguntas 5 y 22.

### Optimizaciones futuras
- Automatizar validación de datos en cada ejecución del scraper (pruebas de humo).
- Versionar esquema de datos para detectar cambios en la estructura de Revolico.
- Crear dashboard interactivo con las métricas del proyecto.

---

## 5. Cómo reproducir

```bash
cd Mercado-de-Motos
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python src/verificar_datos.py          # validar dataset
python src/analisis/etl_mercado.py     # ETL -> data/processed/
python src/analisis/generar_reporte.py # métricas, gráficos e informe
python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0
pytest -q                              # pruebas
```

---

## 6. Archivos clave

| Ruta | Contenido |
|---|---|
| `data/processed/anuncios_limpios.csv` | Dataset consolidado (6.159 anuncios) |
| `data/raw/revolico/geo_catalogo.json` | Catálogo de provincias y municipios |
| `src/scraping/revolico/scrape.py` | Scraper de Revolico (corregido) |
| `src/scraping/revolico/common.py` | Utilidades, clasificador, resolutor geo |
| `src/analisis/etl_mercado.py` | ETL con trazabilidad y geolocalización |
| `src/verificar_datos.py` | Validación del dataset |
| `tests/test_datos.py` | Pruebas automáticas |
| `reports/informe_mercado.md` | Informe final con gráficos |
| `reports/graficos/` | 5 gráficos PNG con datos reales |
| `docs/entregables/` | 8 documentos de respuestas y análisis |
| `docs/journal.md` | Bitácora de desarrollo (este documento) |
| `docs/handoff.md` | Este documento |

---

*Hand-off listo para continuar la jornada siguiente. Última validación: `pytest -q` (2 passed), `src/verificar_datos.py` (dataset válido).*
