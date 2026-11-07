# Reporte Técnico — Análisis del Mercado de Motos en La Habana

**Fecha:** 06 de noviembre de 2026  
**Proyecto:** Análisis del Mercado de Motos en La Habana (Introducción a la Ciencia de los Datos)  
**Repositorio:** `Mercado-de-Motos`  
**Último commit:** `40728cc`  

---

## 1. Resumen Ejecutivo

El proyecto tiene un pipeline cuantitativo completo y un módulo cualitativo con 30 entrevistas. De las 30 preguntas de investigación, **26 están respondidas** (5 completamente con datos, 21 parcialmente) y **4 quedan sin respuesta** por falta de datos de campo (municipio, remesas, disponibilidad de repuestos, censo de talleres).

El dataset contiene 6.159 anuncios de Revolico (La Habana), del 10 al 26 de octubre de 2026, clasificados en 3 categorías principales: combustión (1.137), eléctrica (4.778) y scooter/patinete (244). La tasa BCC oficial es 793 CUP/USD.

---

## 2. Arquitectura Actual

### Componentes implementados

| Componente | Ruta | Estado |
|---|---|---|
| Scraper de Revolico | `src/scraping/revolico/scrape.py` | Operativo (descarga listado y detalle) |
| Utilidades y clasificación | `src/scraping/revolico/common.py` | Operativo (clasificador positivo, resolutor geo) |
| Saneado de PII | `src/scraping/revolico/contactos.py` | Operativo (elimina teléfonos/correos) |
| ETL y limpieza | `src/analisis/etl_mercado.py` | Operativo (con trazabilidad y geolocalización) |
| Generación de reportes | `src/analisis/generar_reporte.py` | Operativo (métricas, gráficos, informe) |
| Validación de datos | `src/verificar_datos.py` | Operativo (pruebas de integridad) |
| Pruebas automáticas | `tests/test_datos.py` | Operativo (2 pruebas) |

### Flujo de datos

```
Revolico (sitio web)
    ↓ (scrape.py: buscar_pagina + detalle_anuncio)
data/raw/revolico/*.json (crudo, inmutable)
    ↓ (etl_mercado.py: cargar, limpiar, escribir)
data/processed/anuncios_limpios.csv/json (normalizado, con trazabilidad)
    ↓ (generar_reporte.py)
reports/informe_mercado.md, reports/metricas/, reports/graficos/
```

### Dependencias principales

- Python 3.10+ (entorno `.venv` con Python 3.14)
- pandas, requests, json, re, unicodedata, csv
- matplotlib (gráficos)
- pytest (pruebas)
- Vosk (transcripción cualitativa, Python 3.12 portátil)

---

## 3. Fuentes de Información

### Fuente principal: Revolico
- Portal: `https://www.revolico.com/search`
- Parámetros: `category=vehiculos`, `subcategory`, `province=la-habana`, `page`, `images=on`
- Cortes obtenidos: 17, 22 y 26 de octubre de 2026
- Total: 6.159 anuncios consolidados tras deduplicación

### Fuentes oficiales (Gaceta Oficial, BCC, ONEI)

| Fuente | Identificador | Aporte |
|---|---|---|
| Ley 109/2010 (Ed. 2026) | GOC-2026-ES10 | Licencia, registro, chapa, revisión técnica, casco |
| Gaceta Ordinaria 65/2026 | GOC-2026-O65 | Decreto 163/2026; Res. 171-175, 52/2026 |
| Gaceta Ordinaria 83/2026 | GOC-2026-O83 | DL 132/2026; Res. 197/2026; Res. 340/2026 |
| Gaceta Ordinaria 128/2024 | GOC-2024-O128 | Decreto 119/2024 y normas reemplazadas |
| Decreto-Ley 22/2020 | GOC-2020-EX68 | Marco arancelario aduanas |
| BCC tasas de cambio | bc.gob.cu/tasas-de-cambio | 793 CUP/USD (06/11/2026) |
| ONEI Anuario 2025 cap. 13 | aec2025 | Transporte y seguridad vial (sin parque de motos) |

### Fuentes cualitativas
- 25 entrevistas de compradores (`COMPRADOR_001` a `COMPRADOR_025`)
- 4 entrevistas de talleres (`TALLER_001` a `TALLER_004`, identidad no confirmada)
- 1 entrevista de importadora (`IMPORTADORA_001`, Solimport)
- Transcripción: Vosk (`vosk-model-small-es-0.42`)

---

## 4. Estado del Sistema

### Módulos operativos

| Módulo | Estado | Comentario |
|---|---|---|
| Scraping (listado) | ⚠️ Limitado | SSR no expone `AdType`; descubre anuncios limitado |
| Scraping (detalle) | ✅ Operativo | Descarga ficha individual con provincia/municipio |
| ETL | ✅ Operativo | Limpieza, clasificación, trazabilidad, geolocalización |
| Validación | ✅ Operativo | `verificar_datos.py`, `pytest -q` |
| Reportes | ✅ Operativo | Informe, métricas, 5 gráficos |
| Transcripción cualitativa | ⚠️ Limitado | Vosk funciona; faster-whisper roto |

### Módulos pendientes

| Módulo | Estado | Bloqueador |
|---|---|---|
| Descubrimiento automático de anuncios | Pendiente | SSR roto; requiere CSR/API interna |
| Censo de talleres | Pendiente | Trabajo de campo presencial |
| Módulo de repuestos | Pendiente | Trabajo de campo en talleres |
| Pregunta directa de remesas | Pendiente | Cuestionario de entrevistas |

### Problemas conocidos

1. **Transcripción con faster-whisper/ctranslate2 rota:** `EXIT=-1073741819` (access violation) en Python 3.12 y 3.14. Vosk funciona con precisión limitada en audios ruidosos.
2. **`requirements.txt` no incluye `faster-whisper`, `av` ni `vosk`:** requieren instalación aparte.
3. **Anuncios miden oferta publicada, no ventas efectivas.**
4. **Serie temporal corta:** 3 capturas (17, 22, 26 oct); fuente cuantitativa es un solo portal.
5. **Clasificación por palabras clave:** posibles errores en títulos ambiguos.

---

## 5. Métricas Técnicas

### Commits y archivos

| Métrica | Valor |
|---|---|
| Último commit | `40728cc` |
| Archivos modificados en sesión | 19 |
| Archivos nuevos (untracked) | 13 |
| Archivos de respuestas creados | 8 |
| Gráficos regenerados | 5 |

### Archivos de respuestas entregados

| Archivo | Contenido |
|---|---|
| `docs/entregables/respuestas_30_preguntas.md` | Veredicto completo de las 30 preguntas (5/21/4) |
| `docs/entregables/respuestas_17_preguntas_pendientes.md` | Análisis de las 17 preguntas inicialmente sin respuesta |
| `docs/entregables/respuestas_21_parciales_completadas.md` | Análisis exhaustivo de las 21 preguntas parciales |
| `docs/entregables/respuestas_entrevistas_q4_q6_q7_q28.md` | Respuestas basadas en 30 entrevistas |
| `docs/entregables/respuestas_fuentes_oficiales.md` | Verificación con Gaceta Oficial, BCC y ONEI |
| `docs/entregables/storytelling_mercado_motos.md` | Narrativa del mercado con datos y personajes |
| `docs/entregables/trabajo_campo_resultados.md` | Resultados de extracción de municipios y trabajo de campo |
| `docs/entregables/plan_refactor_scraper_revolico.md` | Plan de refactorización del scraper |

### Cobertura funcional alcanzada

| Métrica | Valor |
|---|---|
| Preguntas respondidas (datos) | 5 de 30 (16.7%) |
| Preguntas respondidas (parcial) | 21 de 30 (70.0%) |
| Preguntas sin respuesta | 4 de 30 (13.3%) |
| Total respondidas (parcial o completa) | 26 de 30 (86.7%) |
| Anuncios con municipio | 105 de 6.159 (1.70%) |
| Anuncios con marca identificada | 2.545 de 6.159 (41.3%) |
| Pruebas automáticas pasando | 2 de 2 (100%) |

---

## 6. Decisiones Técnicas Tomadas

1. **Clasificación jerárquica en 3 categorías principales:** combustión, electric, scooter. Cada anuncio pertenece a exactamente una categoría. Validada en ETL para evitar duplicación.
2. **No hardcodeo de ubicación:** el ETL lee provincia/municipio del scraping o resuelve desde refs Apollo; nunca asume "La Habana".
3. **Trazabilidad completa:** cada registro tiene `sello_extraccion`, `archivo_origen`, `ref_provincia`, `ref_municipio`, `hash_contenido` (implícito en estructura).
4. **No inventar datos:** campos vacíos se dejan como `null`/vacío y se documentan en `preguntas_pendientes`.
5. **No publicar PII:** teléfonos, correos y nombres no se guardan; audios en `.gitignore`.
6. **Valores de referencia aduanero ≠ precio de mercado:** documentado como límite en Res. 340/2026.

---

*Reporte técnico listo para archivar. Última validación: `pytest -q` (2 passed), `src/verificar_datos.py` (dataset válido, 6.159 anuncios).*
