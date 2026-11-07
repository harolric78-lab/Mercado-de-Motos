# Journal — Bitácora de Desarrollo

Registro cronológico de los avances, decisiones técnicas, modificaciones y entregables del proyecto **Investigación del Mercado de Motos en Cuba**.

---

## 📅 16 de octubre de 2026
- **Inicialización del repositorio:** creación del repositorio y commit inicial (`c11813d`).

---

## 📅 17 de octubre de 2026
- **Migración de contenidos:** importación de fotografías y README desde el repositorio previo `Mercado-de-Motos-Cuba`.
- **Estructuración profesional:** organización de carpetas (`src/`, `datos/`, `docs/`, `notebooks/`, `graficos/`, `reports/`).
- **Scraper de Revolico:** extracción automatizada de anuncios de La Habana y almacenamiento en CSV y JSON.
- **Definición de alcance:** cuatro categorías oficiales (motos de combustión, motos eléctricas, bicicletas eléctricas y patinetes) y eliminación de datos personales.
- **Análisis exploratorio inicial:** procesamiento de los 30 anuncios más recientes, tabla de anuncios y gráfico de evolución.
- **Limpieza y anomalías:** scripts de normalización, estandarización de monedas y detección de precios atípicos.
- **Notebooks:** creación de `eda_motos.ipynb`.

---

## 📅 22 de octubre de 2026
- **Organización de entregables:** creación de `journal/` y `hands-off/`.
- **Entrevistas:** reorganización de la estructura de datos y registro de la entrevista cualitativa.
- **Automatización de reportes:** ejecución del ETL, informes de precios y distribución por categorías, y gráficos en `reports/graficos/`.

---

## 📅 23–24 de octubre de 2026
- **Consolidación y documentación:** actualización de la documentación principal, integración de la bitácora y verificación general del proyecto.

---

## 📅 26 de octubre de 2026
- **Nuevo corte de Revolico:** 30 anuncios recientes de La Habana, con actualización de datos, métricas, informes y gráficos.
- **Documentación:** actualización de resultados, conclusiones, fuentes y estructura del proyecto.
- **Entregable ejecutivo:** creación del resumen ejecutivo con cifras clave y hallazgos.

---

## 📅 27 de octubre de 2026 — Unificación de estructura
- **Estructura unificada:** se eliminó la carpeta `data/` y todo el pipeline quedó en `datos/`.
- **Código actualizado:** rutas de scrapers, ETL, informes y skill de scraping.
- **Verificación:** ETL e informe regenerados sin errores y `py_compile` correcto.

---

## 📅 28 de octubre de 2026 — Depuración de alcance y nueva estructura
- **Backup externo:** copia completa del repositorio antes de la limpieza, con verificación SHA256 de todos los archivos.
- **Depuración de alcance:** el repositorio se limita a las cuatro categorías oficiales; se retiraron datasets, informes, gráficos y referencias de vehículos fuera de alcance.
- **Nueva estructura de datos:**
  - `data_raw/revolico/` para los cortes crudos depurados.
  - `data_clean/` para el histórico consolidado, los archivos por categoría y los cortes del 22 y 26 de octubre.
- **ETL y reportes:** se actualizaron `src/analisis/etl_mercado.py` y `src/analisis/generar_reporte.py`; se regeneraron el informe, las métricas y los gráficos.
- **Resultado del histórico depurado:** 6.101 anuncios.
  - Motos de Combustión: 1.099.
  - Motos Eléctricas: 2.201.
  - Bicicletas Eléctricas: 2.576.
  - Patinetes: 225.
- **Corte del 26/10/2026:** 30 anuncios (9 de combustión, 3 motos eléctricas, 17 bicicletas eléctricas y 1 patinete).
- **Documentación:** README principal, informe, resumen ejecutivo, metodología y journal actualizados.
- **Validación:** datasets con cuatro categorías, sin referencias de alcance fuera del proyecto; compilación de `src/` y pruebas básicas.
- **Publicación:** cambios preparados; push pendiente de confirmación.

---

## 📅 31 de octubre de 2026 — Refactor de estructura profesional
- **Limpieza:** eliminado el clon anidado `Mercado-de-Motos/Mercado-de-Motos/`, cachés de pruebas y entornos virtuales de la raíz.
- **Nueva estructura de datos:** `data/raw/revolico/` para cortes crudos, `data/processed/` para el dataset consolidado y los cortes, y `data/interim/` para la salida auxiliar del ETL (ignorada por Git).
- **Depuración:** retirados los históricos duplicados y las carpetas derivadas por categoría; el consolidado canónico es `data/processed/anuncios_limpios.*`.
- **Código y reportes:** actualizadas las rutas en scrapers, ETL, validación, notebook y generador de reportes; informe y métricas estandarizados como `reports/informe_mercado.md` y `reports/metricas/resumen_mercado.*`.
- **Entorno:** creado `Mercado-de-Motos/.venv` con las dependencias de `requirements.txt`.
- **Validación:** dataset de 6.101 anuncios y pruebas automáticas en verde.

---

## 📅 3 de noviembre de 2026 — Módulo cualitativo y hand-off
- **Captura y transcripción:** creados `src/cualitativo/nueva_entrevista.py` y `src/cualitativo/transcribir.py`.
- **Hand-off:** creado `docs/entregables/HANDOFF.md` con estado, pendientes y comandos de reproducción.
- **Validación:** JSON de entrevistas validado; `src/verificar_datos.py`, `pytest -q` y `py_compile` sin errores.

---

## 📅 4 de noviembre de 2026 — Reinicio de entrevistas
- **Borrado de entrevistas anteriores:** se vaciaron `compradores.json`, `talleres.json` e `importadoras.json`.
- **Material crudo eliminado:** las transcripciones de `data/raw/entrevistas/` y los audios de `data/raw/audios/` de las entrevistas anteriores.
- **Documentación limpiada:** actualizados `docs/entrevistas/README.md`, `README.md`, `explicacion_pipeline.md`, `docs/entregables/HANDOFF.md`, `docs/images/evidencia_campo.md` y este journal; retirados los reportes obsoletos.
- **Entorno de transcripción:** instalados `vosk` y `av` en `.venv` y descargado `vosk-model-small-es-0.42` en `modelos/` (ignorado por Git).
- **Nuevas entrevistas:** se revisaron los 21 audios de las cinco carpetas y se descartaron todos los que duplicaban la sesión antigua. Quedaron **9 audios nuevos** en `COMPRADOR_001` y `COMPRADOR_002`. Además se recuperó `COMPRADOR_003` como entrevista en texto (sin audio).
- **Entrevista 6:** se transcribió `Entrevista de comprador 6` (157,5 s); su audio se verificó como no duplicado y se registró como `COMPRADOR_004`.
- **Importadora Solimport:** se transcribió la entrevista de 23,6 min y se registró como `IMPORTADORA_001`, con datos de importación, aranceles, formación de precios y demanda.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 — Continuación de transcripciones
- **Comprador 5:** se transcribió `Entrevita comprador 5/audio_2026-11-04_12-29-52.ogg` (98,3 s) y se registró como `COMPRADOR_005`.
- **Comprador 7:** se transcribió `Entrvista comprador 7/WhatsApp Ptt 2026-11-04 at 9.21.14 PM.ogg` (112,8 s) y se registró como `COMPRADOR_006`.
- **Comprador 8:** se transcribió `Entrevista comprador 8/WhatsApp Ptt 2026-11-05 at 8.25.19 AM.ogg` (79,5 s) y se registró como `COMPRADOR_007`.
- **Comprador 9:** se transcribió `Entrevista comprador 9/WhatsApp Ptt 2026-11-05 at 7.21.36 AM.ogg` (142,6 s) y se registró como `COMPRADOR_008`.
- **Duplicado descartado:** el audio de `Entrevista de comprador 6` tiene el mismo SHA256 que `COMPRADOR_004`; no se volvió a transcribir.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Lote de compradores 10-14 y taller
- **Compradores 10 a 14:** se transcribieron cinco audios y se registraron como `COMPRADOR_009` a `COMPRADOR_013` (165,6 s; 229,5 s; 90,4 s; 311,1 s y 96,3 s). `COMPRADOR_011` y `COMPRADOR_012` tienen audio del 2026-10-23.
- **Taller 1:** se transcribió `Entrevistas de taller 1/WhatsApp Ptt 2026-11-05 at 10.43.36 AM.ogg` (77,2 s) y se registró como `TALLER_001`; el audio se asigna a taller por la carpeta de origen, pero no confirma claramente que el entrevistado sea un taller.
- **Mapeo de carpetas:** 10→009, 11→010, 12→011, 13→012 y 14→013.
- **Datos:** se registraron solo respuestas claras; el resto quedó en `null` y en `preguntas_pendientes`.
- **Análisis:** creado `docs/entrevistas/analisis_lote_2026-11-05.md` con fichas, lectura transversal, contradicciones e implicaciones del lote.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Compradores 15-17
- **Compradores 15 a 17:** se transcribieron `Entrevistas comprador  15`, `Entrevista de comprador 16` y `Entrevista comprador 17` y se registraron como `COMPRADOR_014`, `COMPRADOR_015` y `COMPRADOR_016` (208,3 s; 60,8 s y 206,7 s). `COMPRADOR_014` tiene audio del 2026-11-04.
- **Mapeo de carpetas:** 15→014, 16→015 y 17→016.
- **Datos:** solo respuestas claras; `COMPRADOR_015` es muy corto y ruidoso.
- **Análisis:** se amplió `docs/entrevistas/analisis_lote_2026-11-05.md` con el anexo de `COMPRADOR_014` a `COMPRADOR_016`.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Comprador 18 y taller 2
- **Comprador 18:** se transcribieron cuatro notas de voz (`WhatsApp Audio 2026-11-05 at 2.24.58 PM.ogg`, `...2.24.59...`, `...2.25.00...` y `...2.25.01...`; 92,6 s; 38,4 s; 41,3 s y 33,9 s) y se unieron en `COMPRADOR_017`.
- **Taller 2:** se transcribió `Entrevista de taller 2/WhatsApp Ptt 2026-11-05 at 2.38.06 PM.ogg` (101,0 s) y se registró como `TALLER_002`.
- **Datos:** solo respuestas claras; ambos audios son ruidosos y la identidad de taller de `TALLER_002` está por confirmar.
- **Análisis:** se amplió `docs/entrevistas/analisis_lote_2026-11-05.md` con el anexo de `COMPRADOR_017` y `TALLER_002`.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Compradores 19-24 y talleres 3-4
- **Compradores 19 a 24:** se transcribieron seis audios y se registraron como `COMPRADOR_018` a `COMPRADOR_023` (103,3 s; 93,2 s; 77,6 s; 50,6 s; 71,9 s y 119,8 s).
- **Duplicado descartado:** la carpeta 19 contenía además `WhatsApp Ptt 2026-11-05 at 8.25.19 AM.ogg`, idéntico a `COMPRADOR_007`; no se volvió a transcribir.
- **Talleres 3 y 4:** se transcribieron `Entrevista taller 3` (39,1 s) y `Entrevista taller 4` (80,1 s) y se registraron como `TALLER_003` y `TALLER_004`.
- **Datos:** solo respuestas claras; varios audios son cortos y ruidosos, y la identidad de taller sigue por confirmar.
- **Análisis:** se amplió `docs/entrevistas/analisis_lote_2026-11-05.md` con el anexo de `COMPRADOR_018` a `COMPRADOR_023` y `TALLER_003`-`TALLER_004`.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Comprador 25
- **Comprador 25:** se transcribió `Entrevista comprador 25/WhatsApp Ptt 2026-11-05 at 4.30.57 PM.ogg` (60,9 s) y se registró como `COMPRADOR_024`.
- **Datos:** se registran solo respuestas claras: uso laboral, ocupación vinculada al comercio y una pieza robada/dañada; tipo de moto, canal, precio y autonomía quedan en `preguntas_pendientes`.
- **Cierre:** con esta entrevista se completa la serie de carpetas 19-25: 24 compradores, 4 talleres y 1 importadora (29 entrevistas).
- **Análisis:** se amplió `docs/entrevistas/analisis_lote_2026-11-05.md` con la sección 10.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Comprador 25 (texto)
- **Comprador 25:** se integró como `COMPRADOR_025` una entrevista en texto (sin audio): 40 años, diseñador de luces, Plaza de la Revolución (Vedado).
- **Datos:** eléctrica comprada a un conocido por 1.000 USD; uso laboral y diario; carga diaria (a veces dos veces); autonomía real que ha disminuido; sin chapa ni licencia; prefiere combustión a futuro.
- **Cierre:** el registro queda en 25 compradores, 4 talleres y 1 importadora (30 entrevistas).
- **Análisis:** se amplió `docs/entrevistas/analisis_lote_2026-11-05.md` con la sección 11.
- **Nota:** el journal se movió de `docs/journal/README.md` a `docs/journal.md`.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Cobertura de las 30 preguntas
- **Documento:** se incorporaron `docs/entregables/preguntas.txt` (30 preguntas de investigación) y `docs/entregables/como_responde_el_proyecto.md`, que cruza cada pregunta con el dataset, las entrevistas y los informes.
- **Resultado:** 4 preguntas resueltas con datos (4, 8, 9 y 27), 17 parciales o solo cualitativas (1, 2, 3, 6, 10, 12, 13, 15, 16, 18, 19, 24, 25, 26, 28, 29 y 30) y 9 pendientes (5, 7, 11, 14, 17, 20, 21, 22 y 23).
- **Brechas identificadas:** municipio/zona, condición nueva/usada, país de importación, muestra de remesas, verificación de aranceles, módulo de repuestos y nuevo corte de Revolico.
- **Documentación:** actualizados `docs/entregables/README.md`, el hand-off y esta bitácora.
- **Ubicación:** `HANDOFF.md` y `journal.md` se movieron a la raíz del repositorio `Mercado-de-Motos`.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 5 de noviembre de 2026 - Carpetas `journal/` y `handoff/`
- **Organización:** se crearon las carpetas `journal/` y `handoff/` en la raíz del repositorio.
- **Ubicación final:** `journal/journal.md` y `handoff/HANDOFF.md`.
- **Referencias:** actualizados `README.md`, `explicacion_pipeline.md`, `docs/entrevistas/guia_entrevista.md`, `docs/entregables/README.md`, `docs/entregables/reporte_tecnico.md` y el propio hand-off.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 6 de noviembre de 2026 - Storytelling del mercado
- **Documento:** se creó `docs/entregables/storytelling_mercado.md`, un relato en 9 capítulos que cruza los 6.101 anuncios con las 30 entrevistas.
- **Estructura:** prólogo, composición de la oferta, precios, marcas, vistas, vida cotidiana, batería, papeles/importación, talleres, escenarios de futuro y epílogo de límites.
- **Aportes:** personajes basados en entrevistas reales (`COMPRADOR_012`, `014`, `017`, `018`, `025` e `IMPORTADORA_001`), cifras con fuente, escenarios A/B, anexo de datos y guion breve de 7 láminas.
- **Regla:** no se añadieron datos fuera de las fuentes del proyecto; las cifras por confirmar se mantienen señaladas.
- **Documentación:** actualizados `docs/entregables/README.md` y el hand-off.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.

---

## 📅 6 de noviembre de 2026 - Verificación con fuentes oficiales
- **Documento:** se creó `docs/entregables/respuestas_fuentes_oficiales.md`, que contrasta las 30 preguntas con la Gaceta Oficial (2020-2026), el BCC y la ONEI.
- **Hallazgo clave:** el 5 % (eléctricas) y el 20 % (combustión) que menciona la importadora **no son el arancel**, sino el Impuesto Especial a Productos y Servicios sobre el precio de venta (Res. 172/2026). La Res. 172/2026 exonera del Impuesto Aduanero a los comercializadores autorizados que importan eléctricos para venderlos en USD.
- **Datos oficiales:** tasa BCC de 793,00 CUP/USD (06/11/2026); valores de referencia en aduana (eléctrica 200 USD; combustión 850 sin sidecar y 950 con sidecar); valores mínimos de usados (Res. 171/2026: 265.000 / 132.500 / 66.250 CUP para motos y triciclos); valores de repuestos (Res. 340/2026).
- **Requisitos legales (Ley 109/2010, edición 2026):** licencia obligatoria (Art. 261), categorías A/A1 (Art. 264), Registro de Vehículos (Arts. 215-216), chapa trasera única (Art. 197), revisión técnica (Arts. 211-213) y notificación de cambios en 30 días (Art. 217). El seguro no aparece como obligatorio en el Código.
- **Cadena regulatoria:** Decreto 119→163, Res. 226→104, Res. 60→17, Res. 397→171, Res. 398→172, Res. 399→173, Res. 400→174, Res. 401→175, Res. 180→52, Res. 364→340 y DL 101→DL 132.
- **Resultado:** cobertura actualizada a **5 🟢** (4, 8, 9, 17 y 27), **21 🟡** y **4 🔴** (5, 11, 20 y 22). La 17 pasa a verde; la 7, 14, 21 y 23 pasan a parciales.
- **Límite:** la tarifa ad-valorem exacta de la importación no comercial de motos de combustión no está publicada en la Gaceta consultada; hay que solicitarla a la Aduana o al MFP.
- **Documentación:** actualizados `docs/entregables/como_responde_el_proyecto.md`, `docs/entregables/preguntas_reformuladas.md`, `docs/entregables/README.md` y el hand-off.
- **Validación:** `json.load`, `src/verificar_datos.py`, `pytest -q` y `py_compile`.
