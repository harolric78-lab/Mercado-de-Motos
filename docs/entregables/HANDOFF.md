# Hand-off — Estado del proyecto

**Actualizado:** 2026-11-05
**Proyecto:** Análisis del Mercado de Motos en La Habana (Introducción a la Ciencia de los Datos)
**Repositorio:** `Mercado-de-Motos` (repositorio Git anidado dentro de `Proyecto de ICD Motos en cuba (2)`)

Este documento resume el estado real del proyecto para que otra persona pueda continuar sin contexto previo. No sustituye al `README.md` ni al `docs/journal/README.md`; los complementa.

---

## 1. Resumen ejecutivo

- El **pipeline cuantitativo está terminado**: scraping de Revolico, limpieza, ETL, validación, métricas, gráficos e informe.
- El **módulo cualitativo se reinició el 2026-11-04** y ya incluye **13 entrevistas de compradores** (`COMPRADOR_001` a `COMPRADOR_013`), **1 de taller** (`TALLER_001`) y **1 de importadora** (`IMPORTADORA_001`, Solimport). `COMPRADOR_001`, `COMPRADOR_002` y `COMPRADOR_004` a `COMPRADOR_013` se transcribieron con Vosk; `COMPRADOR_003` se recuperó como texto.
- La transcripción automática disponible es **Vosk** (`vosk-model-small-es-0.42`); `faster-whisper`/`ctranslate2` no funciona en este entorno (access violation).
- El dataset consolidado no se ha vuelto a scrapear desde el **26/10/2026**.

---

## 2. Estado por área

| Área | Estado | Notas |
|---|---|---|
| Scraping Revolico | Terminado | 3 cortes: 17, 22 y 26 de octubre de 2026 |
| Dataset consolidado | Terminado | 6.101 anuncios, 4 categorías |
| ETL y validación | Terminado | `src/analisis/etl_mercado.py`, `src/verificar_datos.py` |
| Métricas y gráficos | Terminado | `reports/metricas/`, `reports/graficos/` |
| Informe | Terminado | `reports/informe_mercado.md` |
| Entrevistas | En curso | 8 compradores (14 audios nuevos + 1 texto) y 1 importadora (Solimport) |
| Hand-off | Terminado | Este documento |

---

## 3. Qué está terminado

- Dataset histórico consolidado de **6.101 anuncios**:

| Categoría | Anuncios | Mediana USD |
|---|---:|---:|
| Motos de combustión | 1.099 | 2.250 |
| Motos eléctricas | 2.201 | 2.050 |
| Bicicletas eléctricas | 2.576 | 1.150 |
| Patinetes | 225 | 750 |

- Informe, métricas y 5 gráficos regenerables.
- Manifiesto con SHA256 de las fuentes: `data/processed/manifiesto.json`.
- Reinicio del módulo cualitativo: JSON de entrevistas vaciados y material crudo anterior eliminado.
- `COMPRADOR_001`, `COMPRADOR_002` y `COMPRADOR_004` a `COMPRADOR_013` integradas con los audios nuevos, transcritas con Vosk; `COMPRADOR_003` recuperada como texto; `TALLER_001` integrada desde la carpeta `Entrevistas de taller 1`; `IMPORTADORA_001` (Solimport) transcrita con Vosk. Se descartaron los audios y carpetas duplicados de la sesión antigua.
- Estructura, esquema, cuestionario y scripts de captura/transcripción conservados.

---

## 4. Qué está pendiente

1. **Confirmar en campo las respuestas dudosas** de `COMPRADOR_001` a `COMPRADOR_013`, de `TALLER_001` y de `IMPORTADORA_001`: perfiles, vehículos, precios, aranceles y opiniones sobre regulaciones (ver `preguntas_pendientes` en los JSON).
2. **Aclarar `TALLER_001`**: el audio se asignó a taller por la carpeta de origen, pero su contenido no confirma claramente que el entrevistado sea un taller. Conseguir más entrevistas de talleres para consolidar esa fuente.
3. **Nuevo corte de Revolico**: el dataset no se actualiza desde el 26/10/2026.
4. **Cierre de commits**: ver la sección 9.

---

## 5. Cómo reproducir

Requisitos: Python 3.10+ y Git. En este equipo el `.venv` usa Python 3.14. Vosk se ejecutó con un Python 3.12 portátil, porque el `.venv` no tiene `vosk` instalado.

```bash
cd Mercado-de-Motos
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
```

Comandos principales:

```bash
python src/verificar_datos.py                 # validar dataset
python src/analisis/etl_mercado.py            # ETL -> data/interim/
python src/analisis/generar_reporte.py        # métricas, gráficos e informe
python src/scraping/revolico/scrape.py --n 30 --max-paginas 3 --delay 1.0
pytest -q                                     # pruebas
jupyter notebook                              # notebook EDA
```

Pipeline de la skill de scraping:

```bash
python ".opencode/skills/revolico-scraper/scripts/pipeline.py"
```

Transcripción de entrevistas con Vosk (alternativa que funciona en este entorno):

```bash
python src/cualitativo/transcribir_vosk.py "..\Entrevistas\*.ogg" --modelo C:\ruta\a\vosk-model-small-es-0.42 --salida data/raw/entrevistas/COMPRADOR_001.md --sobrescribir
```

La transcripción con `faster-whisper`/`ctranslate2` sigue bloqueada en Python 3.14:

```bash
.venv\Scripts\python.exe src/cualitativo/transcribir.py data/raw/audios/COMPRADOR_001.ogg --id COMPRADOR_001 --modelo small --idioma es
```

Captura asistida de entrevistas:

```bash
python src/cualitativo/nueva_entrevista.py --tipo comprador
```

---

## 6. Reglas del proyecto

- **No inventar ni completar datos**: si un campo no está respondido, se deja `null` o vacío y se documenta en `preguntas_pendientes`.
- **No publicar PII**: no se guardan teléfonos, correos ni nombres. Los audios están en `.gitignore`.
- **Alcance fijo**: solo 4 categorías (combustión, eléctricas, bicicletas eléctricas y patinetes). Triciclos, motocarros y repuestos quedan fuera.
- **No corregir el habla** en las transcripciones.
- **Separar cuantitativo y cualitativo**: `data/` para lo cuantitativo; `docs/entrevistas/` e `docs/images/` para lo cualitativo.

---

## 7. Limitaciones conocidas

- **Transcripción con `faster-whisper`/`ctranslate2` rota**: falla con Python 3.12 y 3.14 (`EXIT=-1073741819`, access violation). Vosk funciona, pero su precisión es limitada en audios ruidosos de WhatsApp.
- `requirements.txt` no incluye `faster-whisper`, `av` ni `vosk`; hay que instalarlos aparte para el módulo cualitativo.
- Las transcripciones de Vosk son ruidosas: solo se registran respuestas claras y el resto queda en `null`.
- Los anuncios miden **oferta publicada**, no ventas efectivas.
- Las vistas son un proxy de demanda, no demanda real.
- Serie temporal corta (3 capturas); la fuente cuantitativa es un solo portal (Revolico), complementada con entrevistas e instituciones.
- Sin conversión CUP→USD: los anuncios en CUP quedan fuera de las estadísticas de precio.
- Clasificación por palabras clave: posibles errores en títulos ambiguos.
- Evidencia cualitativa en curso: 13 entrevistas de compradores, 1 de taller, 1 de importadora y 7 fotos.

---

## 8. Mapa de archivos clave

| Ruta | Contenido |
|---|---|
| `data/raw/revolico/` | Cortes crudos (JSON/CSV) |
| `data/processed/anuncios_limpios.*` | Dataset consolidado |
| `data/processed/manifiesto.json` | Conteos y SHA256 de fuentes |
| `data/raw/entrevistas/` | Transcripciones de entrevistas (`COMPRADOR_001.md` a `COMPRADOR_013.md`, `TALLER_001.md`, `IMPORTADORA_001.md`) |
| `data/raw/audios/` | Audios (ignorados por Git; `COMPRADOR_001/`, `COMPRADOR_002/`, `COMPRADOR_004/` a `COMPRADOR_013/`, `TALLER_001/`, `IMPORTADORA_001/`) |
| `docs/entrevistas/compradores.json` | Entrevistas de compradores normalizadas (`COMPRADOR_001` a `COMPRADOR_013`) |
| `docs/entrevistas/talleres.json`, `docs/entrevistas/importadoras.json` | Talleres con `TALLER_001`; importadoras con `IMPORTADORA_001` (Solimport) |
| `docs/journal/README.md` | Bitácora cronológica |
| `docs/metodologia/` | Decisiones de metodología |
| `docs/entregables/` | Resúmenes ejecutivos y este hand-off |
| `reports/informe_mercado.md` | Informe generado |
| `src/scraping/revolico/` | Scraper |
| `src/analisis/` | ETL y generación de reportes |
| `src/cualitativo/` | Captura y transcripción de entrevistas |
| `src/verificar_datos.py` | Validación del dataset |
| `tests/test_datos.py` | Pruebas |

---

## 9. Próximos pasos priorizados

1. Registrar las nuevas entrevistas aportadas por el investigador.
2. Integrar entrevistas de talleres e importadoras cuando se consigan.
3. Ejecutar un nuevo corte de Revolico cuando se quiera refrescar el dataset.
4. Mantener los commits separados: datos/transcripciones y documentación.

---

## 10. Historial reciente

| Fecha | Cambio |
|---|---|
| 2026-10-26 | Último corte de Revolico (30 anuncios) |
| 2026-10-31 | Refactor de estructura `data/`, `reports/` y `.venv` |
| 2026-11-02 | Módulo cualitativo y script de transcripción |
| 2026-11-03 | Hand-off del proyecto |
| 2026-11-04 | Reinicio de entrevistas; `COMPRADOR_001` a `COMPRADOR_003`; incorporación de `COMPRADOR_004` e `IMPORTADORA_001` (Solimport) |
| 2026-11-05 | Transcripción de `COMPRADOR_005` a `COMPRADOR_008`; duplicado de comprador 6 descartado |
| 2026-11-05 | Transcripción de `COMPRADOR_009` a `COMPRADOR_013` y de `TALLER_001`; total: 13 compradores, 1 taller y 1 importadora |
