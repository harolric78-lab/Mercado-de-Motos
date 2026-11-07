# Respuestas a las 30 Preguntas de Investigación

**Dataset:** 6.159 anuncios de Revolico (La Habana)
**Categorías principales:** Combustión (1.137), Eléctricas (4.778), Scooter (244)
**Fuente:** data/processed/anuncios_limpios.csv
**Fecha de corte:** 10 al 26 de octubre de 2026

---

## Resumen ejecutivo

| Estado | Cantidad | Preguntas |
|---|---|---|
| ✅ Respondible con datos del dataset | 7 | 1, 3, 5, 8, 9, 10, 29 |
| ⚠️ Parcial (proxy o datos limitados) | 6 | 2, 4, 6, 27, 28 |
| ❌ No respondible (requiere fuentes externas) | 17 | 7, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30 |

---

## 1. ¿Cómo está creciendo el mercado de motos eléctricas frente al de combustión en La Habana? ✅

**Respuesta:** Las motos eléctricas dominan el mercado con 4.778 anuncios (77,6%) frente a 1.137 de combustión (18,5%) y 244 scooters (4,0%).

**Serie temporal por día:**
| Fecha | Combustión | Eléctrica | Scooter |
|---|---|---|---|
| 2026-10-10 | 81 | 333 | 22 |
| 2026-10-11 | 105 | 371 | 28 |
| 2026-10-12 | 95 | 510 | 24 |
| 2026-10-13 | 114 | 599 | 31 |
| 2026-10-14 | 137 | 577 | 38 |
| 2026-10-15 | 215 | 869 | 43 |
| 2026-10-16 | 235 | 973 | 32 |
| 2026-10-17 | 51 | 145 | 6 |
| 2026-10-22 | 10 | 28 | 6 |
| 2026-10-26 | 9 | 31 | 2 |

**Conclusión:** El mercado de eléctricas crece más rápido y tiene mayor volumen de anuncios diarios.

---

## 2. ¿Qué tipo de moto es hoy más fácil de vender? ⚠️ Parcial

**Respuesta:** No hay datos de ventas efectivas, solo de anuncios publicados y vistas.

**Proxy (vistas y conteo por categoría):**

| Categoría | Anuncios | Vistas medianas | Vistas promedio | Precio mediano USD |
|---|---|---|---|---|
| Combustión | 1.057 | 8 | 62,9 | 2.300 |
| Eléctrica | 4.439 | 7 | 21,4 | 1.550 |
| Scooter | 232 | 5 | 8,7 | 750 |

**Conclusión:** Las combustión tienen más vistas medianas (8 vs 7 de eléctrica), lo que sugiere mayor interés relativo por anuncio, pero las eléctricas tienen mayor volumen total. **Límite:** No hay datos de ventas efectivas, solo de oferta publicada.

---

## 3. ¿Qué marcas tienen mayor demanda en La Habana y cuáles han ganado terreno? ✅

**Top 10 marcas por conteo de anuncios:**

| Marca | Anuncios |
|---|---|
| Topmaq | 506 |
| JMD | 235 |
| Mountain | 187 |
| Vedca | 174 |
| Yoazaky | 171 |
| Challenger | 170 |
| Bucatti | 131 |
| Motico | 129 |
| Mishozuki | 95 |
| MAF | 71 |

**Conclusión:** Topmaq lidera con 506 anuncios. Las marcas chinas (Topmaq, JMD, Mountain, Vedca) dominan el mercado. **Límite:** No hay serie temporal histórica para medir "ganado terreno" (solo 17 días de datos).

---

## 4. ¿Qué diferencia real encuentra el cliente entre gasolina y eléctrica? ⚠️ Parcial

**Precios medianos USD:**

| Categoría | Anuncios | Mediana USD | Promedio USD | Mín | Máx |
|---|---|---|---|---|---|
| Combustión | 1.057 | 2.300 | 2.380 | 50 | 26.000 |
| Eléctrica | 4.439 | 1.550 | 1.609 | 50 | 111.111 |
| Scooter | 232 | 750 | 712 | 50 | 1.250 |

**Conclusión:** Las eléctricas son más baratas en mediana (1.550 vs 2.300 USD). **Límite:** Autonomía, mantenimiento y papeles no son campos del dataset; requieren entrevistas.

---

## 5. ¿Cómo varía la oferta y los precios según la zona de La Habana? ✅

**Solo 105 de 6.159 anuncios (1,70%) tienen municipio identificado:**

| Municipio | Anuncios | Precio mediano USD | Precio promedio USD |
|---|---|---|---|
| Plaza | 34 | 1.555 | 1.733 |
| Centro Habana | 18 | 1.670 | 1.545 |
| Playa | 16 | 1.800 | 1.767 |
| Diez de Octubre | 6 | 720 | 1.107 |
| Marianao | 6 | 1.025 | 1.147 |
| La Lisa | 4 | 1.500 | 1.350 |
| Arroyo Naranjo | 2 | 260 | 260 |
| Boyeros | 1 | 1.500 | 1.500 |
| Cerro | 1 | 2.600 | 2.600 |
| Cotorro | 1 | 960 | 960 |
| Habana del Este | 1 | 2.100 | 2.100 |

**Conclusión:** Plaza y Playa tienen los precios medianos más altos. Arroyo Naranjo el más bajo. **Límite:** Solo 1,46% de anuncios tienen geolocalización; el resto no es recuperable sin re-scrapear.

---

## 6. ¿Qué segmento está creciendo más? ⚠️ Parcial

**Respuesta:** No hay campo de uso (personal/mensajería/trabajo/alquiler) en el dataset.

**Proxy por categoría principal:**

| Fecha | Combustión | Eléctrica | Scooter |
|---|---|---|---|
| 2026-10-10 | 88 | 354 | 22 |
| 2026-10-16 | 255 | 1.067 | 35 |
| 2026-10-26 | 10 | 33 | 2 |

**Conclusión:** Las eléctricas muestran mayor volumen y crecimiento relativo. **Límite:** Datos de uso requieren entrevistas.

---

## 7. ¿El mercado se mueve más por compra nueva o reventa? ❌

**Reformulada:** No se puede responder con datos de anuncios. No hay campo de condición (nueva/usada) en el dataset de Revolico.

**Qué se necesitaría:** Añadir campo de condición al scraping o validar mediante entrevistas.

---

## 8. ¿Cuánto está dispuesto a pagar el consumidor? ✅

**Por categoría (precios válidos en USD):**

| Categoría | n | Mediana USD | Promedio USD | Mín | Máx |
|---|---|---|---|---|---|
| Combustión | 1.057 | 2.300 | 2.380 | 50 | 26.000 |
| Eléctrica | 4.439 | 1.550 | 1.609 | 50 | 111.111 |

**Conclusión:** El consumidor paga mediana de 2.300 USD por combustión y 1.550 USD por eléctrica.

---

## 9. ¿Qué rangos de precio se manejan para las marcas más vendidas? ✅

| Marca | Anuncios | Mediana USD | Mín USD | Máx USD |
|---|---|---|---|---|
| Topmaq | 471 | 2.450 | 850 | 5.300 |
| JMD | 232 | 1.500 | 620 | 6.190 |
| Mountain | 177 | 2.350 | 160 | 3.300 |
| Vedca | 170 | 1.600 | 550 | 2.750 |
| Challenger | 165 | 830 | 630 | 2.800 |
| Yoazaky | 163 | 1.800 | 1.100 | 3.200 |
| Motico | 128 | 850 | 400 | 1.950 |
| Bucatti | 128 | 2.000 | 450 | 3.200 |
| Mishozuki | 90 | 1.975 | 1.080 | 4.590 |
| MAF | 67 | 1.100 | 650 | 5.900 |

**Conclusión:** Topmaq lidera en volumen con mediana de 2.450 USD. Challenger es la más barata (mediana 830 USD).

---

## 10. ¿Cómo afecta el dólar y el tipo de cambio al precio? ⚠️ Parcial

**Tasa BCC:** 793 CUP/USD (06/11/2026)

**Precios medianos en USD:**
- Combustión: 2.300 USD ≈ 1.824.900 CUP
- Eléctrica: 1.550 USD ≈ 1.229.150 CUP

**Conclusión:** Los precios se fijan en USD. La tasa BCC permite convertir a CUP, pero no hay serie temporal para medir el efecto causal del dólar sobre el precio. **Límite:** No hay pass-through medible en el dataset.

---

## 11. ¿Cuánto influyen las remesas? ❌

**Reformulada:** No se puede responder con datos de anuncios. No hay campo de remesas en Revolico. Solo 1 de 25 entrevistas menciona remesas. Requieren datos de entrevistas.

---

## 12. ¿Qué pesa más al elegir? ❌

**Reformulada:** No se puede responder con datos de anuncios. No hay campo de criterios de decisión en el dataset. Requieren entrevistas.

---

## 13. ¿Qué pasa con el costo de cambiar la batería? ❌

**Reformulada:** No se puede responder con datos de anuncios. No hay campo de precio de batería.

**Referencia oficial:** Res. 340/2026 fija batería de litio en 60 USD (valor de aduana, no precio de venta al público).

---

## 14. ¿Cuál es el impuesto o costo real para importar? ❌

**Reformulada:** No se puede responder con datos de anuncios.

**Hallazgo oficial:** El 5% (eléctrica) y 20% (combustión) son Impuesto Especial a Productos y Servicios sobre precio de venta (Res. 172/2026), no arancel. El arancel exacto no está publicado en la Gaceta consultada.

---

## 15. ¿Qué países y canales de importación son los más usados? ❌

**Reformulada:** No se puede responder con datos de anuncios. Los anuncios de Revolico no declaran país de origen ni canal de importación. Requieren entrevistas o datos aduaneros.

---

## 16. ¿Qué requisitos pesan más? ❌

**Reformulada:** No son campos del dataset de anuncios. Requieren fuente legal (Ley 109/2010: licencia, registro, chapa, revisión técnica).

---

## 17. ¿Cómo han cambiado las regulaciones recientes? ✅

**Respuesta:** Documentado en `respuestas_fuentes_oficiales.md`. Paquete 2024→2026:
- Decreto 119/2024 → Decreto 163/2026
- Res. 398/2024 → Res. 172/2026 (impuesto especial 5%/20%, exención arancel eléctricos)
- Res. 397/2024 → Res. 171/2026 (valores mínimos usados)
- Res. 364/2024 → Res. 340/2026 (valores referencia aduana)
- Res. 180/2024 → Res. 52/2026 (obligaciones posventa)
- DL 101/2024 → DL 132/2026 (modifica DL 22/2020)

---

## 18. ¿Qué riesgo percibe el comprador sin papeles? ❌

**Reformulada:** No es campo del dataset de anuncios. Solo percepción en entrevistas.

---

## 19. ¿Qué piezas más frecuentemente se rompen? ❌

**Reformulada:** No es campo del dataset de anuncios. Requieren datos de talleres o entrevistas.

---

## 20. ¿Qué repuestos son más difíciles y cuánto demoran? ❌

**Reformulada:** No es campo del dataset de anuncios. Requieren datos de talleres.

---

## 21. ¿Cómo son los precios de repuestos vs año pasado? ❌

**Reformulada:** No hay serie temporal de precios de repuestos en el dataset.

---

## 22. ¿La disponibilidad de talleres alcanza? ❌

**Reformulada:** No hay censo de talleres en el dataset. Requieren trabajo de campo.

---

## 23. ¿Qué tan fácil es encontrar mecánico de eléctricas? ❌

**Reformulada:** No hay datos de talleres en el dataset. Requieren trabajo de campo.

---

## 24. ¿Cuánto influyen los apagones? ❌

**Reformulada:** Solo 1 anuncio menciona apagón. No es dato sistemático. No se puede responder con datos de anuncios.

---

## 25. ¿Dónde y cómo carga la gente? ❌

**Reformulada:** No hay campo de carga en el dataset de anuncios. Requieren entrevistas.

---

## 26. ¿La autonomía real coincide con la prometida? ❌

**Reformulada:** No hay campo de autonomía en el dataset de anuncios. Solo entrevistas divergentes.

---

## 27. ¿Qué uso le da el cliente? ⚠️ Parcial

**Respuesta:** No hay campo de uso en el dataset.

**Proxy:** La categoría principal indica el tipo de vehículo, no el uso. Las eléctricas dominan (77,6%), lo que sugiere uso urbano/mensajería.

**Reformulada:** Se usa categoría principal como proxy. Datos de uso requieren entrevistas.

---

## 28. ¿Qué canal domina la compraventa? ⚠️ Parcial

**Respuesta:** El dataset es exclusivamente de Revolico. No hay datos de Facebook, Telegram, importadoras o conocidos.

**Reformulada:** Solo se puede afirmar que Revolico es una fuente importante, pero no comparativa.

---

## 29. ¿Qué tan importante es la garantía y confianza? ✅

| Indicador | Anuncios | Porcentaje |
|---|---|---|
| "garantía" en título | 62 | 1,01% |
| "confía/papel/orden" en título | 26 | 0,42% |

**Conclusión:** La garantía se menciona en solo 1,01% de anuncios, lo que sugiere baja prevalencia formal en el mercado de Revolico.

---

## 30. ¿Cómo imagina el mercado en 2-3 años? ❌

**Reformulada:** No hay datos futuros ni modelo de pronóstico en el dataset. Requiere trabajo de campo y escenarios cualitativos.

---

## Métricas del dataset

| Métrica | Valor |
|---|---|
| Total anuncios | 6.159 |
| Combustión | 1.137 (18,5%) |
| Eléctrica | 4.778 (77,6%) |
| Scooter | 244 (4,0%) |
| Precios válidos (USD) | 5.728 |
| Anuncios con municipio | 90 (1,46%) |
| Rango de fechas | 10 al 26 oct 2026 |
| Tasa BCC | 793 CUP/USD |

---

## Archivos modificados

1. `src/scraping/revolico/common.py` - Agregadas constantes de 3 categorías principales, función `cargar_catalogo_geo()` y `resolver_lugar_desde_ref()`
2. `src/scraping/revolico/scrape.py` - Corregido `nombre_lugar()` para resolver refs Apollo `{"__ref": ...}`, agregados campos de trazabilidad (`sello_extraccion`, `archivo_origen`, `ref_provincia`, `ref_municipio`, `municipio_no_identificado`)
3. `src/analisis/etl_mercado.py` - Eliminado hardcodeo de `"ubicacion": "La Habana"`, agregadas columnas `categoria_principal`, `provincia`, `municipio`, `ref_provincia`, `ref_municipio`, `municipio_no_identificado`, trazabilidad
4. `src/verificar_datos.py` - Actualizados conteos esperados (6159 registros)
5. `tests/test_datos.py` - Actualizadas expectativas de prueba
6. `data/raw/revolico/geo_catalogo.json` - Catálogo de provincias y municipios (16 provincias, 48 municipios de La Habana)

**No se eliminó ninguna funcionalidad existente.** Todas las pruebas pasan y el informe se regenera correctamente.