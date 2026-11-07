# Historial de commits por módulo

**Repositorio:** `Mercado-de-Motos` — rama `master`
**Periodo cubierto:** 2026-10-16 a 2026-11-06
**Total de commits:** 57
**Último commit:** `200f7f2` — *docs: agregar storytelling del mercado con datos y entrevistas*

Este documento agrupa el historial por **módulos funcionales**, no solo por fecha. Un mismo commit puede tocar más de un módulo; aquí se clasifica por su propósito principal.

---

## 1. Resumen por módulo

| Módulo | Commits | Periodo | Qué contiene |
|---|---:|---|---|
| **A. Infraestructura y análisis cuantitativo** | 31 | 2026-10-16 → 2026-10-31 | Scraper de Revolico, ETL, limpieza, clasificación en 4 categorías, métricas, gráficos e informes del dataset |
| **B. Módulo cualitativo (entrevistas)** | 17 | 2026-10-26 → 2026-11-05 | Formato de entrevistas, transcripción con Vosk, normalización JSON, 30 entrevistas, validación y análisis |
| **C. Documentación y entregables** | 6 | 2026-10-22 → 2026-11-06 | Journal, HANDOFF, reporte técnico, cobertura de preguntas, storytelling e informes en PDF |
| **D. Estructura, refactor y mantenimiento** | 3 | 2026-10-22 → 2026-11-06 | Renombrado de carpetas, copia de scripts en `codigo/` y organización de `journal/` y `handoff/` |

> Nota: algunos commits de documentación acompañan a los módulos A y B (por ejemplo, actualizar conteos al cerrar un lote de entrevistas). Se listan en el módulo C solo los que tienen la documentación como objetivo principal.

---

## 2. Módulo A — Infraestructura y análisis cuantitativo

**Objetivo:** construir el dataset de anuncios, limpiarlo, clasificarlo y generar métricas e informes.

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-10-16 | `c11813d` | Commit inicial del proyecto |
| 2026-10-17 | `f037bf9` | Migración de contenido, fotos y README |
| 2026-10-17 | `0cb9ed1` | Reestructuración profesional + scraper de Revolico y datos crudos |
| 2026-10-17 | `f72256c` | Categoría “Motos Eléctricas”, privacidad y resumen tabulado |
| 2026-10-17 | `636aae8` | Análisis de los 30 anuncios más recientes |
| 2026-10-17 | `1e3e31f` | Tabla de los 30 anuncios más recientes con enlace |
| 2026-10-17 | `f3ecf8d` | Tabla de motos más demandadas y gráfico de evolución |
| 2026-10-17 | `caa00c0` | Corrección de la tabla de fuentes (Revolico, 6.466 anuncios) |
| 2026-10-22 | `92c4a0c` | Limpieza de datos, precios atípicos y notebook de EDA |
| 2026-10-24 | `b6ec4b9` | Entrevista de precios y motos más vendidas |
| 2026-10-24 | `41192fa` | Encabezado (fecha, entrevistado, lugar) en la entrevista |
| 2026-10-24 | `b4baa2d` | Journal, reportes, datos y scripts actualizados |
| 2026-10-24 | `761c952` | Eliminación del gráfico de evolución 2024–2026 del README |
| 2026-10-24 | `107d049` | Carpetas de importadoras (vedca, solimport, pendiente) |
| 2026-10-26 | `1d04af6` | Scrapers de VEDCA, Islagrande y pipeline de Revolico |
| 2026-10-26 | `4ceb8e3` | Corte de Revolico al 26/10 con informes y gráficos |
| 2026-10-26 | `848ea57` | Catálogo oficial de VEDCA (7 vehículos) |
| 2026-10-26 | `f62b817` | Precios de Islagrande (14 precios válidos) |
| 2026-10-26 | `5bc7114` | README: fuentes, estructura, hallazgos y conclusiones |
| 2026-10-26 | `68417ec` | Journal del 26/10 y resumen ejecutivo |
| 2026-10-26 | `41485ba` | Carpeta `datos/codigos` con scripts Python |
| 2026-10-26 | `4f6a307` | Saneado de teléfonos y correos en datos y código |
| 2026-10-26 | `9b40bb1` | Corte 26/10: ETL e informe regenerados |
| 2026-10-26 | `341206d` | Unificación de `data/` y `datos/` |
| 2026-10-29 | `2dfa7cd` | Depuración de alcance: cuatro categorías y dataset consolidado |
| 2026-10-30 | `7a80672` | README: reorganización académica y guía de ejecución |
| 2026-10-30 | `2939ca6` | README: análisis de La Habana, cuatro categorías y métricas reales |
| 2026-10-31 | `63166b2` | Actualización de README |
| 2026-10-31 | `5c48b11` | Reorganización de estructura de datos y reportes |
| 2026-10-31 | `ea7beb1` | Organización de imágenes del proyecto |
| 2026-10-31 | `89896ea` | Consolidación de la estructura documental |

**Resultado del módulo:** dataset de **6.101 anuncios** (3 archivos fuente, 6.344 registros brutos), 4 categorías, métricas de precios y demanda, 5 gráficos y `reports/informe_mercado.md`.

---

## 3. Módulo B — Cualitativo (entrevistas)

**Objetivo:** recolectar, transcribir, normalizar y analizar entrevistas a compradores, talleres e importadoras.

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-10-26 | `ad58b2b` | Conversión de la entrevista de markdown a texto plano |
| 2026-11-01 | `c229b2a` | Entrevista `USER_001` en `usuarios.json` |
| 2026-11-02 | `d55334c` | Módulo cualitativo y transcripción de `USER_001` |
| 2026-11-03 | `d593531` | Normalización de compradores e integración de `COMPRADOR_002` |
| 2026-11-03 | `cc6a3ff` | Journal, handoff y conteos de entrevistas |
| 2026-11-04 | `746cdae` | Transcripción con Vosk y corrección de atribución |
| 2026-11-04 | `cb775b0` | Reinicio del registro de entrevistas |
| 2026-11-04 | `b5edca8` | Integración de entrevistas nuevas y de Solimport |
| 2026-11-05 | `0792930` | `COMPRADOR_005` y `COMPRADOR_006` |
| 2026-11-05 | `455b2dd` | `COMPRADOR_007` y `COMPRADOR_008` |
| 2026-11-05 | `bf60864` | `COMPRADOR_009` a `COMPRADOR_013` y `TALLER_001` |
| 2026-11-05 | `11e3494` | Análisis del lote 009–013 y taller |
| 2026-11-05 | `9c04923` | `COMPRADOR_014` a `COMPRADOR_016` y análisis del lote |
| 2026-11-05 | `2c89370` | `COMPRADOR_017` y `TALLER_002` |
| 2026-11-05 | `21fac9b` | `COMPRADOR_018` a `COMPRADOR_023`, `TALLER_003` y `TALLER_004` |
| 2026-11-05 | `8e1ac7d` | `COMPRADOR_024` y cierre de la serie de carpetas 19–25 |
| 2026-11-05 | `31dc23d` | `COMPRADOR_025` (texto), journal a `docs/journal.md` y reporte técnico |

**Resultado del módulo:** **30 entrevistas** integradas — 25 compradores, 4 talleres y 1 importadora — normalizadas en `docs/entrevistas/*.json`, con transcripciones en `data/raw/entrevistas/` y análisis transversal en `docs/entrevistas/analisis_lote_2026-11-05.md`.

### Hitos del módulo

- **Transcripción local con Vosk** (`vosk-model-small-es-0.42`) tras descartar `faster-whisper`/`ctranslate2` por fallo del entorno.
- **Control de duplicados** por SHA256; se descartó un audio de la carpeta 19 idéntico a `COMPRADOR_007`.
- **Entrevistas en texto** (`COMPRADOR_003` y `COMPRADOR_025`) registradas con `transcripcion_automatica: false`.
- **Regla de integridad:** solo respuestas explícitas; lo no inteligible queda en `null` y en `preguntas_pendientes`.

---

## 4. Módulo C — Documentación y entregables

**Objetivo:** dejar el proyecto legible, trazable y entregable.

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-10-22 | `208944b` | Creación de las carpetas `journal` y `hands-off` |
| 2026-10-30 | `ca8ea47` | Unificación de entrevistas y evidencia cualitativa; reorganización de imágenes |
| 2026-11-05 | `daedd3d` | Handoff y journal fuera del repo + cobertura de las 30 preguntas |
| 2026-11-05 | `686cf9c` | Retorno de `HANDOFF.md` y `journal.md` a la raíz del repositorio |
| 2026-11-06 | `1e192c4` | Reporte técnico e informe del proyecto en PDF (`docs/entregables/`) |
| 2026-11-06 | `200f7f2` | Storytelling del mercado con datos, personajes de entrevistas y guion de presentación |

**Entregables principales:**

- `README.md` — presentación, objetivos, dataset y hallazgos.
- `explicacion_pipeline.md` — explicación del flujo de datos.
- `handoff/HANDOFF.md` — estado del proyecto, pendientes y comandos.
- `journal/journal.md` — bitácora cronológica.
- `docs/entregables/reporte_tecnico.md` — procesamiento de entrevistas.
- `docs/entregables/Reporte_Tecnico_Proyecto_Mercado_Motos.pdf` — documentación técnica oficial.
- `docs/entregables/Informe_Proyecto_Mercado_Motos.pdf` — informe para el profesor y lectores.
- `docs/entregables/preguntas.txt` y `como_responde_el_proyecto.md` — 30 preguntas y su cobertura.
- `docs/entregables/storytelling_mercado.md` — relato del mercado en 9 capítulos, personajes y guion de presentación.

---

## 5. Módulo D — Estructura y mantenimiento

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-10-22 | `fb704c9` | Renombrado de `datos/encuestas` a `datos/entrevistas`; limpieza de `docs/encuestas` y `docs/entrevistas` |
| 2026-11-05 | `bc9be63` | Copia de todos los `.py` en `codigo/` (respaldo reproducible) |
| 2026-11-06 | `aa259f8` | Creación de `journal/` y `handoff/`; `journal.md` y `HANDOFF.md` movidos a sus carpetas |

**Resultado:** separación entre datos crudos, procesados, código, documentación y reportes; scripts de normalización y validación disponibles en `codigo/analisis_entrevistas/`.

---

## 6. Línea de tiempo resumida

| Fecha | Hito |
|---|---|
| 2026-10-16 | Inicio del repositorio |
| 2026-10-17 | Primer scraper de Revolico y estructura del proyecto |
| 2026-10-22 | Limpieza de datos, precios atípicos y EDA |
| 2026-10-26 | Corte de Revolico, scrapers de importadoras y reportes |
| 2026-10-29 | Consolidación del dataset a cuatro categorías (6.101 anuncios) |
| 2026-11-01 | Inicio del módulo cualitativo |
| 2026-11-04 | Reinicio del registro de entrevistas y transcripción con Vosk |
| 2026-11-05 | Cierre del lote: 30 entrevistas (25 + 4 + 1) |
| 2026-11-06 | Entrega de los dos PDF (reporte técnico e informe) |
| 2026-11-06 | Reorganización de `journal/` y `handoff/` en carpetas propias |
| 2026-11-06 | Storytelling del mercado con datos y entrevistas |

---

## 7. Estado actual del repositorio

- **Dataset:** 6.101 anuncios depurados.
- **Entrevistas:** 30 (25 compradores, 4 talleres, 1 importadora).
- **Validación:** `src/verificar_datos.py` (6.101 OK), `pytest -q` (2 passed), `validar_entrevistas.py` (30 entrevistas; solo errores preexistentes documentados).
- **Documentación:** en la raíz (`README.md`, `explicacion_pipeline.md`), en `handoff/HANDOFF.md`, `journal/journal.md` y en `docs/`.
- **Entregables PDF:** en `docs/entregables/`.

---

*Documento generado automáticamente a partir de `git log`. Los hashes son los identificadores cortos del repositorio.*
