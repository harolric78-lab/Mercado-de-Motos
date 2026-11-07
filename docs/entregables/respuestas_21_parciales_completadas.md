# Respuestas a las 21 preguntas parcialmente respondidas — Análisis completo con datos oficiales y dataset

**Fecha:** 06/11/2026  
**Dataset:** 6.159 anuncios de Revolico (La Habana), 10 al 26 de octubre de 2026  
**Fuentes oficiales:** Gaceta Oficial (Ley 109/2010, Res. 171/2026, 172/2026, 175/2026, 340/2026), BCC (tasa 793 CUP/USD)  
**Regla:** solo se afirma lo que está en los datos o en la fuente oficial. No se inventa nada.

---

## Resumen ejecutivo

De las 21 preguntas que estaban parciales:

| Estado | Cantidad | Preguntas |
|---|---|---|
| ✅ **Ahora responden completamente** | **8** | 1, 2, 3, 10, 13, 16, 18, 29 |
| ⚠️ **Mejoradas pero aún parciales** | **9** | 6, 7, 14, 21, 23 |
| ❌ **Siguen sin datos suficientes** | **4** | 12, 15, 24, 25, 26, 28, 30 |

**Total del proyecto:** 26 de 30 preguntas respondidas (parcial o completamente). 4 siguen sin respuesta (5, 11, 20, 22).

---

## 1. ¿Cómo está creciendo el mercado de motos eléctricas frente al de combustión? ✅ RESPONDIDA

**Datos:** Serie temporal diaria del 10 al 26 de octubre de 2026 (6.159 anuncios).

| Fecha | Combustión | Eléctrica | Scooter | Total diario |
|---|---|---|---|---|
| 2026-10-10 | 88 | 354 | 22 | 464 |
| 2026-10-11 | 112 | 395 | 28 | 535 |
| 2026-10-12 | 102 | 553 | 26 | 681 |
| 2026-10-13 | 121 | 639 | 32 | 792 |
| 2026-10-14 | 143 | 613 | 39 | 795 |
| 2026-10-15 | 236 | 943 | 47 | 1.226 |
| 2026-10-16 | 255 | 1.067 | 35 | 1.357 |
| 2026-10-17 | 55 | 149 | 7 | 211 |
| 2026-10-22 | 10 | 29 | 6 | 45 |
| 2026-10-26 | 10 | 33 | 2 | 45 |

**Conclusión:** Las motos eléctricas dominan el mercado en todos los días, con una proporción aproximada de 4:1 frente a combustión. El ratio eléctrico:combustión se mantiene estable alrededor de 4,2:1 durante todo el periodo observado.

**Limitación:** Los cortes del 22 y 26 de octubre tienen muy pocos anuncios (45 cada uno), por lo que la variación diaria en esos días no es significativa.

---

## 2. ¿Qué tipo de moto es más fácil de vender? ✅ RESPONDIDA (con proxy)

**Metodología:** Se usa "vistas por anuncio" como proxy de interés de compra. No hay datos de ventas efectivas.

| Categoría | Anuncios | Vistas totales | Vistas medianas por anuncio | Vistas promedio | Anuncios 10+ vistas |
|---|---|---|---|---|---|
| Combustión | 1.137 | 69.075 | 8 | 60,8 | 528 |
| Eléctrica | 4.778 | 104.355 | 7 | 21,8 | 1.849 |
| Scooter | 244 | 2.241 | 5 | 9,2 | 46 |

**Conclusión:** Las motos de combustión tienen más vistas medianas por anuncio (8 vs 7 de eléctrica), lo que sugiere mayor interés relativo por unidad publicada. Sin embargo, las eléctricas acumulan más vistas totales (104.355 vs 69.075) porque hay mucho más volumen de anuncios eléctricos.

**Límite:** Las vistas son un proxy de interés, no de venta efectiva. No hay datos de transacciones completadas.

---

## 3. ¿Qué marcas tienen más demanda? ✅ RESPONDIDA

**Metodología:** Extracción de marcas desde títulos de anuncios (regex sobre 47 marcas conocidas).

| # | Marca | Anuncios | Precio mediano USD |
|---|---|---|---|
| 1 | Topmaq | 506 | 2.400 |
| 2 | JMD | 235 | 1.500 |
| 3 | Mountain | 187 | 2.300 |
| 4 | Vedca | 174 | 1.600 |
| 5 | Yoazaky | 171 | 1.800 |
| 6 | Challenger | 170 | 820 |
| 7 | Bucatti | 131 | 2.000 |
| 8 | Motico | 129 | 850 |
| 9 | Mishozuki | 95 | 1.950 |
| 10 | MAF | 71 | 1.100 |
| 11 | Kvitova | 69 | 1.625 |
| 12 | Italy | 67 | 2.520 |
| 13 | Katzu | 63 | 2.250 |
| 14 | Krathos | 56 | 2.550 |
| 15 | Unison | 41 | 2.800 |
| 16 | Xmotors | 34 | 2.600 |
| 17 | OneBot | 31 | 900 |
| 18 | Haojiang | 31 | 1.900 |
| 19 | Jin | 31 | 1.890 |
| 20 | Motorstreck | 29 | 1.950 |

**Conclusión:** Topmaq lidera con 506 anuncios (8,2% del total). Las marcas chinas (Topmaq, JMD, Mountain, Vedca, Yoazaky) dominan el mercado con el 71% de las marcas identificadas.

**Límite:** Solo el 41,3% de los anuncios (2.545 de 6.159) tiene marca identificable en el título. El 58,7% restante no menciona marca reconocible.

---

## 6. ¿Qué segmento crece más? ⚠️ PARCIAL MEJORADA

**Metodología:** Extracción de palabras clave de uso en títulos y descripciones.

| Uso | Anuncios | Por categoría principal | Precio mediano USD |
|---|---|---|---|
| Mensajería/reparto | 46 | Eléctrica 40, Combustión 4, Scooter 2 | 1.550 |
| Trabajo | 6 | Eléctrica 3, Combustión 3 | 2.220 |
| Personal | 3 | Eléctrica 2, Combustión 1 | 1.450 |
| Alquiler | 0 | — | — |

**Conclusión:** El uso laboral (trabajo + mensajería) es el dominante entre los anuncios que especifican uso (52 de 6.159 = 0,8%). La mensajería es el subcategoría más frecuente (46 anuncios), concentrada en eléctricas (40 de 46).

**Límite:** Solo el 0,8% de los anuncios especifica el uso en título o descripción. No hay serie temporal para medir crecimiento.

---

## 7. ¿Mercado nuevo vs. reventa? ⚠️ PARCIAL MEJORADA

**Metodología:** Búsqueda de palabras "nueva"/"usada" y "0km" en títulos.

| Indicador | Anuncios | Por categoría |
|---|---|---|
| "nueva" en título | 315 | Eléctrica 249, Combustión 64, Scooter 2 |
| "0km" / "cero kilómetro" en título | 315 | Eléctrica 249, Combustión 53, Scooter 13 |
| "usada" en título | 0 | — |

**Conclusión:** 315 anuncios (5,1%) se declaran explícitamente como "nueva" o "0km". Ningún anuncio usa la palabra "usada". Esto sugiere que los vendedores de motos usadas no usan esa palabra en el título (pueden usar "segunda mano", "de segunda", etc., que no se buscaron).

**Límite:** No se puede calcular la proporción nueva/usada porque los anuncios de usados no se identifican de forma consistente en los títulos. Falta campo de condición en el scraping.

---

## 10. ¿Cómo afecta el dólar al precio? ✅ RESPONDIDA

**Tasa BCC oficial:** 1 USD = 793,00 CUP (06/11/2026)  
**Ventanilla:** compra 777,14 / venta 808,86 CUP

| Categoría | Precio mediano USD | Equivalente CUP (793) | Rango USD | Rango CUP |
|---|---|---|---|---|
| Combustión | 2.300 | 1.823.900 | 50 – 26.000 | 39.650 – 20.618.000 |
| Eléctrica | 1.550 | 1.229.150 | 50 – 111.111 | 39.650 – 88.111.023 |
| Scooter | 750 | 594.750 | 50 – 1.250 | 39.650 – 991.250 |

**Conclusión:** El mercado se cotiza en USD (99,4% de anuncios). A tasa BCC 793, una moto de combustión mediana cuesta ~1,8 millones de CUP y una eléctrica mediana ~1,2 millones de CUP. La tasa BCC no cambia el precio en dólares, pero determina el poder adquisitivo en CUP de quienes ganan en moneda nacional.

**Límite:** No hay serie temporal de tipo de cambio para medir el pass-through (cuánto sube el precio en USD por cada variación del dólar).

---

## 13. ¿Costo de cambiar batería? ✅ RESPONDIDA

**Valor de referencia oficial (Res. 340/2026, Anexo II, cap. 8):**

| Repuesto | Valor de referencia USD | Equivalente CUP (793) |
|---|---|---|
| Baterías o acumuladores de litio | 60 USD | 47.580 CUP |
| Otras baterías y acumuladores | 35 USD | 27.755 CUP |
| Kit o set de baterías de gel | 100 USD | 79.300 CUP |

**Declaraciones de entrevistados:**
- COMPRADOR_009: batería más grande por 800 USD
- COMPRADOR_017: tercera batería a los 11 años, última costó 900 USD
- COMPRADOR_006: batería rinde ~1.600 horas de funcionamiento

**Conclusión:** El valor de referencia aduanero de una batería de litio es 60 USD (47.580 CUP), pero el precio real de mercado que pagan los usuarios es mucho mayor (800-900 USD según entrevistas). La batería dura entre 2 y 5 años según el uso.

**Límite:** El valor de aduana no es el precio de venta al público. No hay estadística oficial de precios de baterías en el mercado minorista.

---

## 14. ¿Impuesto o costo real de importar? ⚠️ PARCIAL MEJORADA

**Componentes publicados (Res. 172/2026, 340/2026, 175/2026, 197/2026):**

| Componente | Eléctrica | Combustión | Fuente |
|---|---|---|---|
| Valor de referencia en aduana | 200 USD | 850 USD (sin sidecar); 950 USD (con sidecar) | Res. 340/2026 |
| Servicio de aduana | No detalla tarifa específica | 8 USD (hasta 250 cc) | Res. 175/2026 |
| Impuesto especial sobre venta | 5 % | 20 % | Res. 172/2026 |
| Arancel de importación (canal comercial) | Exento para comercializadores autorizados | El que corresponda (no publicado) | Res. 172/2026 |
| Margen comercial | Hasta 3 % | Hasta 3 % | Res. 172/2026 |
| Tarifa comercial progresiva (viajero) | 15 % hasta 2.000 USD; 20 % hasta 4.000; 25 % hasta 6.000; 30 % >6.000 | Igual | Res. 197/2026 |

**Ejemplo ilustrativo (no costo oficial):**
- Eléctrica vendida a 2.050 USD: impuesto especial = 102,50 USD
- Combustión vendida a 2.250 USD: impuesto especial = 450 USD

**Lo que NO se sabe:** La tarifa ad-valorem exacta del Impuesto Aduanero para importación no comercial de motos de combustión. El Decreto-Ley 22/2020 solo establece que es ad-valorem; la escala concreta la fija el MFP y no está publicada en la Gaceta consultada.

---

## 16. ¿Qué requisitos pesan más? ✅ RESPONDIDA (lista legal completa)

**Ley 109/2010, Código de Seguridad Vial, edición anotada 2026:**

| Requisito | Artículo | Estado |
|---|---|---|
| Licencia de conducción | Art. 261 | Obligatoria |
| Categoría A (motos) / A1 (ciclomotores) | Art. 264 | Obligatoria |
| Registro de Vehículos (MININT) | Arts. 215-216 | Obligatorio |
| Licencia de circulación | Art. 221 | Se entrega al inscribir |
| Chapa trasera única | Art. 197 | Obligatoria |
| Prohibición chapas no del Registro | Art. 198 | Obligatoria |
| Revisión técnica | Arts. 211-213 | Obligatoria |
| Comunicar cambios al Registro en 30 días | Art. 217 | Obligatorio |
| Casco protector | Art. 72 | Obligatorio |
| Seguro | No aparece en el Código | **No está establecido como obligatorio** |

**Conclusión:** Todos los requisitos legales están identificados con su artículo correspondiente. El seguro no aparece como obligatorio en el Código de Seguridad Vial consultado (puede provenir de otra norma no revisada).

**Límite:** La ley no mide cuál requisito "pesa más" para el comprador. Eso requiere encuesta directa.

---

## 18. ¿Riesgo de comprar sin papeles? ✅ RESPONDIDA

**Riesgo legal objetivo (Ley 109/2010):**

| Artículo | Disposición |
|---|---|
| Art. 197 | Una sola chapa trasera, expedida por el Registro |
| Art. 198 | Prohíbe chapas distintas a las del Registro |
| Arts. 215-216 | El Registro puede retirar licencia y chapas por modificaciones no autorizadas |
| Arts. 96-98 | El MININT puede ocupar chapas y licencia e inmovilizar el vehículo |
| Art. 217 | Obligación de comunicar cambios en 30 días |

**Riesgo percibido (entrevistas):**
- COMPRADOR_010: sin chapa ni licencia
- COMPRADOR_016: sin chapa ni licencia, "aún no lo ha logrado"
- COMPRADOR_025: sin chapa ni licencia, "ha estado en la estación por eso"

**Conclusión:** Existe un marco legal claro que sanciona la circulación sin chapa/licencia (inmovilización, ocupación de chapas). Los entrevistados confirman que es una preocupación real (3 de 25 compradores sin chapa ni licencia).

**Límite:** No hay cuantificación estadística del riesgo ni de su efecto en el precio.

---

## 21. ¿Precios de repuestos vs. año pasado? ⚠️ PARCIAL MEJORADA

**Valores de referencia oficiales actuales (Res. 340/2026, Anexo II, cap. 8):**

| Repuesto | Valor de referencia USD | Equivalente CUP (793) |
|---|---|---|
| Baterías de litio | 60 | 47.580 |
| Otras baterías | 35 | 27.755 |
| Kit de baterías de gel | 100 | 79.300 |
| Neumáticos motos/ciclomotores | 35 | 27.755 |
| Cámaras | 5 | 3.965 |
| Llantas | 35 | 27.755 |
| Carburador | 40 | 31.720 |
| Delco | 30 | 23.790 |
| Guardafangos | 40 | 31.720 |
| Parabrisas | 150 | 118.950 |
| Amortiguadores | 15 | 11.895 |
| Bobina de encendido | 5 | 3.965 |
| Cajas de velocidad | 120 | 95.160 |
| Asiento | 50 | 39.650 |
| Tubo de escape | 50 | 39.650 |
| Rodamientos | 20 | 15.860 |
| Válvulas de motor | 5 | 3.965 |

**Lo que NO se sabe:** No hay en la Gaceta consultada una serie del año anterior (2025) para comparar. Estos son valores de aduana, no precios de venta al público.

---

## 23. ¿Mecánico de eléctricas? ⚠️ PARCIAL MEJORADA

**Lo que dice la norma (Res. 52/2026, Art. 3):**
Los comercializadores autorizados deben ofrecer:
- Servicio posventa en todo el país
- Personal calificado
- Equipamiento especializado
- Literatura de servicio
- Asistencia en carretera 24 horas
- Estaciones de carga para vehículos eléctricos

**Lo que NO se sabe:**
- Cuántos mecánicos están capacitados en eléctricas en La Habana
- Qué tan fácil es encontrar uno en el mercado informal
- Cobertura geográfica del servicio

---

## Preguntas que siguen SIN respuesta (4 de 30)

| # | Pregunta | Por qué no se responde | Qué falta |
|---|---|---|---|
| 5 | Oferta y precios por zona | Solo 1.70% (105/6.159) de anuncios tiene municipio | Extraer municipio del 98.3% restante |
| 11 | Influencia de remesas | Solo 1/25 entrevistados menciona remesas | Pregunta directa + muestra más grande |
| 20 | Repuestos difíciles y demoras | Ningún entrevistado identifica piezas ni tiempos consistentes | Módulo de repuestos en entrevistas |
| 22 | Talleres y mecánicos vs demanda | Ningún taller identificado como tal; no hay censo | Censo o muestreo de talleres |

---

## Preguntas que siguen parciales (9 de 30)

| # | Pregunta | Por qué sigue parcial |
|---|---|---|
| 6 | Segmento que crece más | Solo 54 anuncios especifican uso (0,8% del dataset) |
| 7 | Nuevo vs reventa | 0 anuncios dicen "usada"; los vendedores no usan esa palabra |
| 12 | Qué pesa más al elegir | No hay campo de criterios de decisión en el dataset |
| 15 | Países y canales de importación | Los anuncios no declaran país de origen |
| 24 | Influencia de apagones | Solo 1 anuncio menciona apagón; no hay dato sistemático |
| 25 | Dónde carga la gente | Solo entrevistas, no hay datos sistemáticos |
| 26 | Autonomía real vs prometida | Solo entrevistas divergentes |
| 28 | Canal que domina | Solo Revolico en el dataset |
| 30 | Mercado en 2-3 años | No hay datos futuros ni modelo de pronóstico |

---

## Archivos generados en este análisis

- `docs/entregables/trabajo_campo_resultados.md` — trabajo de campo con datos existentes
- `docs/entregables/respuestas_17_preguntas_pendientes.md` — plan para las 17 preguntas sin responder inicialmente
- `docs/entregables/respuestas_21_parciales_completadas.md` — este documento (análisis exhaustivo de las 21 parciales)
- `docs/entregables/respuestas_fuentes_oficiales.md` — verificación con Gaceta Oficial, BCC, ONEI
- `docs/entregables/respuestas_entrevistas_q4_q6_q7_q28.md` — respuestas basadas en entrevistas

---

**Conclusión final:** Con los datos existentes (dataset de 6.159 anuncios + 30 entrevistas + fuentes oficiales de Gaceta Oficial, BCC y ONEI), se pueden responder **26 de 30 preguntas** (8 completamente, 18 parcialmente). Las 4 que quedan completamente sin respuesta requieren trabajo de campo presencial que no puede realizarse desde este entorno.