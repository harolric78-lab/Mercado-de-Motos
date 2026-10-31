# Reporte de unificación de evidencia cualitativa

**Fecha:** 2026-10-30
**Alcance:** unificación de entrevistas, observaciones y evidencia fotográfica del proyecto.

---

## 1. Entrevistas detectadas

| Tipo de fuente | Detectadas | Ubicación original |
|---|---:|---|
| Talleres | 1 | `datos/entrevistas/entrevista_motos_mas_vendidas.txt` (historial Git) |
| Importadoras | 0 | — |
| Usuarios | 0 | — |

Detalle de la entrevista detectada:

- **Identificador:** `TALLER_001`
- **Fecha:** 2026-10-22
- **Ubicación:** La Habana, Cuba
- **Entrevistado:** no identificado en el registro original
- **Origen:** commits `b6ec4b9` (creación), `41192fa` (encabezado) y `ad58b2b` (conversión a texto plano); eliminada del árbol de trabajo en `2dfa7cd`.
- **Clasificación:** tentativa como taller, porque el registro original no especifica el tipo de fuente.

## 2. Entrevistas migradas

| Archivo de destino | Registros | Estado |
|---|---:|---|
| `docs/entrevistas/talleres.json` | 1 | Migrada con texto original conservado |
| `docs/entrevistas/importadoras.json` | 0 | Estructura vacía documentada |
| `docs/entrevistas/usuarios.json` | 0 | Estructura vacía documentada |

No se fabricaron entrevistas ni respuestas. Los campos sin información quedaron vacíos y la ausencia se documentó en cada archivo y en `docs/entrevistas/README.md`.

## 3. Archivos convertidos a JSON

| Origen | Destino | Formato |
|---|---|---|
| `datos/entrevistas/entrevista_motos_mas_vendidas.md` | `docs/entrevistas/talleres.json` | Markdown → JSON |
| `datos/entrevistas/entrevista_motos_mas_vendidas.txt` | `docs/entrevistas/talleres.json` | Texto plano → JSON |

Se conservó el campo `texto_original` para mantener la trazabilidad entre la fuente y el registro normalizado.

## 4. Imágenes reorganizadas

| Origen | Destino | Archivos |
|---|---|---:|
| `docs/images/Importadora de motos/` | `docs/images/importadoras/` | 4 |
| `docs/images/Tiendas de motos electricas y de combustion/` | `docs/images/tiendas/` | 3 |
| — | `docs/images/talleres/` | 0 (creada vacía con `.gitkeep`) |

Total de imágenes reorganizadas: **7**. Todas con metadatos EXIF del 2026-10-08.

## 5. Documentación generada

| Archivo | Contenido |
|---|---|
| `docs/entrevistas/README.md` | Propósito, metodología, conteo, categorías y limitaciones |
| `docs/images/evidencia_campo.md` | Origen, organización, propósito y relación con entrevistas y hallazgos |
| `docs/metodologia/REPORTE_UNIFICACION.md` | Este reporte |

Además, se actualizó el `README.md` principal con la sección **Fuentes Cualitativas** y el árbol de estructura.

## 6. Ausencias documentadas

- No existen entrevistas a importadoras.
- No existen entrevistas a usuarios.
- No existen fotografías de talleres.
- El catálogo VEDCA detectado en el historial (`datos/importadora_vedca/vedca_catalogo_20261026_100817.json`) es un listado de productos, no una entrevista, por lo que no se migró.
- La entrevista `TALLER_001` no identifica entrevistado, cargo ni establecimiento exacto.

## 7. Validación

- JSON de `docs/entrevistas/` validado sintácticamente.
- Estructura de carpetas verificada.
- `python src/verificar_datos.py` ejecutado sin errores.
- `pytest -q` ejecutado sin errores.
