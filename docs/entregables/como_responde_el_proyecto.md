# Cómo responde el proyecto a las 30 preguntas del mercado de motos en La Habana

Documento de trabajo que acompaña a `preguntas.txt`. Explica, para cada pregunta, **con qué evidencia del proyecto se responde**, **qué se encontró** y **qué queda como límite o pendiente**.

## Fuentes del proyecto

| Fuente | Qué aporta | Cobertura |
|---|---|---|
| Dataset de anuncios (`data/processed/anuncios_limpios.csv`) | Precios, categorías, marcas, vistas y menciones en los textos | **6.101 anuncios** de Revolico (La Habana), del **2026-10-10 al 2026-10-26** |
| Entrevistas cualitativas (`docs/entrevistas/`) | Preferencias, gastos, repuestos, apagones, canales y percepciones | **30 entrevistas**: 25 compradores, 4 talleres y 1 importadora |
| Informes (`reports/`) | Tablas y gráficos agregados | `informe_mercado.md`, `resumen_mercado.json`, `graficos/` |
| Análisis cualitativo (`docs/entrevistas/analisis_lote_2026-11-05.md`) | Lectura transversal de las entrevistas | 25 compradores + talleres |

**Leyenda:** 🟢 el proyecto lo responde con datos; 🟡 lo responde parcialmente o solo con entrevistas; 🔴 no lo responde todavía (queda como pendiente).

> Advertencia metodológica: el dataset es una **foto de 17 días** de la oferta publicada en Revolico, no de las ventas reales. Las entrevistas son una muestra pequeña y no probabilística. Por eso varias preguntas se responden como **tendencia o percepción**, no como cifra exacta.

---

## Bloque 1 — Mercado y demanda

### 1. ¿Cómo está creciendo el mercado de motos eléctricas frente al de combustión en La Habana? 🟡

- **Lo que sí muestra el proyecto:** en la oferta de Revolico, la movilidad eléctrica domina. De 6.101 anuncios: **2.201 motos eléctricas (36,1 %)**, **2.576 bicicletas eléctricas (42,2 %)**, **1.099 motos de combustión (18,0 %)** y **225 patinetes (3,7 %)**. Es decir, **78,3 % de los anuncios son eléctricos** (motos + bicis) frente a 18 % de combustión.
- **Lo que aportan las entrevistas:** la importadora (`IMPORTADORA_001`) percibe que “el avance se inclina hacia los equipos eléctricos” y que la combustión se sostiene por la situación del combustible. Varios compradores usan eléctrica a diario.
- **Límite:** con 17 días de datos **no se puede medir crecimiento**. No hay serie temporal suficiente; solo se puede hablar de **composición actual de la oferta**, no de evolución.

### 2. ¿Qué tipo de moto es hoy más fácil de vender: combustión, eléctrica, bicicleta eléctrica o patinete? ¿Por qué? 🟡

- **Lo que muestra el proyecto:** por volumen de oferta, la **bicicleta eléctrica** es la categoría con más anuncios (2.576), seguida de la moto eléctrica (2.201). La combustión tiene menos oferta (1.099).
- **Señal de demanda:** las vistas medianas son parecidas (8 para combustión, 6 para eléctrica, 7 para bicicleta, 5 para patinete), pero el **promedio** de vistas es mucho mayor en combustión (62,4) que en eléctrica (15,2), lo que sugiere anuncios de combustión con picos de interés.
- **Límite:** “más fácil de vender” no se mide con anuncios; haría falta registrar ventas efectivas.

### 3. ¿Qué marcas tienen mayor demanda en La Habana y cuáles han ganado terreno en el último año? 🟡

- **Marcas con más anuncios (global):** Topmaq (506), JMD (227), Mountain (187), Vedca (173), Challenger (170), Yoazaky (165), Bucatti (131), Motico (129), Mishozuki (95), Halcón (87).
- **Por categoría:** en motos eléctricas lidera **Topmaq (303)**, seguida de Vedca (110) y Mountain (101). En combustión aparecen **Italy (64), Katzu (60) y Krathos (54)**. En bicicletas eléctricas mandan **JMD (178), Topmaq (162) y Yoazaky (157)**.
- **Límite importante:** **2.910 de 6.101 anuncios (47,7 %) no declaran marca**. Por eso el ranking refleja lo que se publica, no necesariamente lo que más se vende. Tampoco hay datos del año anterior para decir qué marca “ganó terreno”.

### 4. ¿Qué diferencia real hay entre una moto de gasolina y una eléctrica? 🟢

- **Diferencia técnica (importadora):** el sistema de alimentación, gasolina frente a batería eléctrica.
- **Diferencia económica (dataset):** la mediana de precio es **2.250 USD** en combustión y **2.050 USD** en eléctrica; la eléctrica tiene mayor dispersión (desviación 949,8 frente a 595,0), es decir, precios más heterogéneos.
- **Diferencia de uso (entrevistas):** la combustión se asocia a rendimiento y kilometraje; la eléctrica, a carga nocturna y menor costo por energía, pero con dependencia de la batería y de los apagones.
- **Diferencia de mantenimiento:** en las entrevistas aparecen fallos de piezas, aceite y neumáticos en combustión, y batería, puño de acelerar y plásticos en eléctrica.

### 5. ¿Cómo varía la oferta y los precios según la zona de La Habana? 🔴

- **Lo que hay:** el dataset solo registra `ubicacion = "La Habana"` para los 6.101 anuncios; **no trae municipio**. Las entrevistas mencionan zonas (Diez de Octubre, Plaza de la Revolución/Vedado), pero no de forma sistemática.
- **Conclusión:** el proyecto **todavía no puede responder** esta pregunta por zona. Para hacerlo habría que extraer el municipio de los anuncios o geolocalizarlos.

### 6. ¿Qué segmento está creciendo más: uso personal, mensajería, trabajo o alquiler? 🟡

- **Lo que muestran las entrevistas:** el **uso laboral** es el patrón más repetido. De 25 compradores, 8 declaran uso exclusivo de trabajo, 3 mixto (trabajo/recados) y 2 mensajería/reparto; solo 2 declaran uso personal. Los talleres también describen uso de trabajo.
- **Límite:** el dataset no clasifica el uso; la respuesta es cualitativa y de una muestra pequeña.

### 7. ¿El mercado se mueve más por la compra de motos nuevas o por la reventa? 🔴

- **Lo que hay:** solo **323 anuncios (5,3 %)** usan la palabra “nueva” y **ninguno** dice explícitamente “usada”. Eso no permite separar compra nueva de reventa.
- **Conclusión:** el proyecto no puede medir este punto con el dataset actual; habría que añadir un campo de condición (nueva/usada) al scraping.

---

## Bloque 2 — Precios y capacidad de pago

### 8. ¿Cuánto está dispuesto a pagar el consumidor por una moto? 🟢

- **Precios publicados (mediana):** combustión **2.250 USD** (rango típico 1.900–2.592), eléctrica **2.050 USD** (rango típico 1.300–2.630), bicicleta eléctrica **1.150 USD** (670–1.650) y patinete **750 USD** (730–800).
- **Entrevistas:** un comprador pagó **1.000 USD** por una eléctrica de segunda mano (`COMPRADOR_025`); otro menciona alrededor de **2.000** (`COMPRADOR_018`, moneda por confirmar); una batería de mayor capacidad se compró por **800 USD** (`COMPRADOR_009`).
- **Lectura:** la disposición a pagar se mueve aproximadamente entre **1.000 y 2.500 USD** según tipo y estado, con la bicicleta eléctrica como opción más barata.

### 9. ¿Qué rangos de precio se manejan hoy para las marcas más vendidas? 🟢

Medianas por marca (solo anuncios con precio en USD):

| Marca | Anuncios con precio | Mediana USD |
|---|---:|---:|
| Bucatti | — | 2.450 |
| Topmaq | 470 | 2.365 |
| Mountain | 183 | 2.280 |
| Mishozuki | 97 | 1.900 |
| Yoazaky | 228 | 1.835 |
| Vedca | 169 | 1.600 |
| JMD | 220 | 1.500 |
| Challenger | 168 | 820 |
| Motico | 86 | 850 |
| MAF | 69 | 1.100 |

> Nota: la marca “sin marca” concentra 2.910 anuncios con mediana de 1.200 USD; es una categoría heterogénea.

### 10. ¿Cómo afecta el dólar y el tipo de cambio al precio final de una moto? 🟡

- **Lo que muestra el dataset:** **6.064 de 6.101 anuncios (99,4 %) están en USD**; solo 37 en CUP, y esos se excluyen de las estadísticas de precio. Es decir, el mercado se cotiza prácticamente **en dólares**.
- **Lo que falta:** el proyecto no registra la tasa de cambio ni hace un análisis causal del efecto del dólar. Se puede afirmar que el precio se fija en USD, pero no cuantificar cuánto sube por cada variación del tipo de cambio.

### 11. ¿Cuánto influyen las remesas y los familiares en el exterior en la decisión de compra? 🔴

- El esquema de entrevistas recoge remesas y familiares en el exterior, pero **solo 1 de 25 compradores** dio un dato utilizable. No hay base para estimar influencia.
- **Conclusión:** pendiente de ampliar la muestra o de preguntarlo de forma más directa.

### 12. ¿Qué pesa más al elegir: precio, autonomía, marca o repuestos? 🟡

- **Entrevistas:** el **precio/valor** aparece como motivo principal en varios compradores; también pesan el **rendimiento/kilometraje** (combustión) y la **facilidad de carga nocturna** (eléctrica). Los repuestos aparecen como problema posterior, no siempre como criterio de compra.
- **Límite:** no hay una pregunta de ranking aplicada de forma uniforme, así que no se puede ordenar con precisión.

### 13. ¿Qué pasa con el costo de una eléctrica cuando hay que cambiar la batería? 🟡

- **Evidencia cualitativa:** una batería de mayor capacidad se compró por **800 USD** (`COMPRADOR_009`); otros entrevistados mencionan la pérdida de autonomía y el gasto de batería como el principal costo de la eléctrica (`COMPRADOR_020`, `COMPRADOR_025`).
- **Señal en el dataset:** **284 anuncios** mencionan “batería” y **139** mencionan “litio”, lo que confirma que es un atributo central de la oferta.
- **Límite:** no hay un precio sistemático de reemplazo de batería por modelo.

---

## Bloque 3 — Importación, papeles y regulación

### 14. ¿Cuál es el impuesto o costo real para importar una moto al país? 🔴

- **Única evidencia:** la importadora (`IMPORTADORA_001`) menciona una **rebaja de aranceles** para vehículos automotores y una carga del **5 %**, pero el propio registro lo deja en `preguntas_pendientes` porque el audio es ruidoso.
- **Conclusión:** el proyecto **no confirma** el impuesto real; es un dato por verificar con fuente oficial.

### 15. ¿Qué países y canales de importación son hoy los más usados? 🟡

- **Entrevistas:** un comprador declara haber comprado por **Panamá** (`COMPRADOR_023`); la importadora es la otra fuente directa.
- **Dataset:** los anuncios **no declaran país de origen** (0 menciones a “Panamá”; solo 13 a “importada/importado”). No se puede construir un ranking de países.
- **Conclusión:** respuesta parcial, solo cualitativa.

### 16. ¿Qué requisitos pesan más: licencia, chapa, seguro o registro? 🟡

- **Entrevistas:** `COMPRADOR_025` declara **no tener chapa ni licencia** y haber tenido problemas en la estación; otros mencionan papeles como factor.
- **Dataset:** **47 anuncios** mencionan “papeles” y **60** mencionan “chapa”; ninguno menciona “licencia”.
- **Límite:** no hay una medición de cuánto pesa cada requisito en la decisión.

### 17. ¿Cómo han cambiado las regulaciones recientes la compra, venta y circulación? 🔴

- Solo hay una mención cualitativa (importadora) sobre incentivo arancelario. El proyecto **no tiene** una línea de base regulatoria ni datos antes/después.
- **Conclusión:** pendiente; requiere revisar normativas y comparar periodos.

### 18. ¿Qué riesgo percibe el comprador al adquirir una moto sin papeles o importada informalmente? 🟡

- **Entrevistas:** aparecen casos de **pieza robada o dañada** (`COMPRADOR_023`) y de motos **sin chapa ni licencia** (`COMPRADOR_025`). El análisis cualitativo lo trata como riesgo percibido, no como estadística.
- **Límite:** no hay cuantificación del riesgo ni de su efecto en el precio.

---

## Bloque 4 — Repuestos y servicio técnico

### 19. ¿Cuáles son las piezas y accesorios que más frecuentemente se rompen? 🟡

- **Entrevistas:** problemas de **piezas, aceite y neumático** en combustión (`COMPRADOR_018`); **puño de acelerar** por el clima y desgaste de **plásticos/estética** en eléctrica (`COMPRADOR_025`); averías y repuestos en talleres (`TALLER_001`–`TALLER_004`).
- **Dataset:** los anuncios no describen fallas (0 menciones a “repuesto”), así que no se puede construir un ranking de piezas.

### 20. ¿Qué repuestos son los más difíciles de conseguir y cuánto demoran? 🔴

- Las entrevistas confirman que **conseguir repuestos es un problema** (`COMPRADOR_018`, talleres), pero no identifican de forma consistente cuáles ni los tiempos.
- **Conclusión:** el proyecto lo deja en `preguntas_pendientes`; falta un módulo específico de repuestos.

### 21. ¿Cómo son los precios de los repuestos respecto al año pasado? 🔴

- No hay serie temporal de precios de repuestos (el dataset cubre 17 días y no es de repuestos). Las entrevistas no dan una comparación clara con el año anterior.

### 22. ¿La disponibilidad de talleres y mecánicos alcanza para la demanda actual? 🔴

- Se entrevistaron **4 talleres**, pero su identidad como talleres **no está confirmada** (la asignación viene de la carpeta de origen). No hay censo de talleres ni de capacidad.
- **Conclusión:** pendiente.

### 23. ¿Qué tan fácil es encontrar un mecánico que trabaje con motos eléctricas? 🔴

- Los 4 talleres entrevistados hablan de eléctricas, pero no se puede generalizar. No hay datos de cobertura ni de especialización.

---

## Bloque 5 — Uso, carga y apagones

### 24. ¿Cuánto influyen los apagones en la decisión de comprar una eléctrica? 🟡

- **Entrevistas:** es un tema recurrente. `COMPRADOR_023` dice que los apagones “afectan mucho”; `COMPRADOR_025` afirma que en ocasiones **no puede usar la moto** por el apagón; `TALLER_004` también lo menciona.
- **Dataset:** solo **1 anuncio** menciona “apagón”, porque los anuncios no suelen hablar de eso.
- **Lectura:** hay una señal cualitativa fuerte, pero no una medición de cuánto frena la compra.

### 25. ¿Dónde y cómo carga la gente que vive en edificios o zonas con poco espacio? 🟡

- **Entrevistas:** la pauta es **cargar de noche** (`COMPRADOR_023`, `COMPRADOR_025`) y, en algunos casos, **hasta dos veces al día** (`COMPRADOR_025`). No hay datos sistemáticos sobre edificios, garajes o carga compartida.
- **Dataset:** 74 anuncios mencionan “carga” y 33 “cargador”, pero como atributo del producto, no como práctica del usuario.

### 26. ¿La autonomía real coincide con la que promete el vendedor? 🟡

- **Entrevistas (respuestas divergentes):** `COMPRADOR_020` dice que la autonomía **disminuyó**; `COMPRADOR_023` dice que **ha ido aumentando**; `COMPRADOR_025` dice que la anunciada era real pero **ha perdido con el tiempo**; `TALLER_004` señala que **varía según peso, velocidad y lomas**.
- **Dataset:** 242 anuncios mencionan “autonomía”, pero es información declarada por el vendedor, no medida.
- **Lectura:** no hay una cifra única; la autonomía real es **variable y dependiente del uso**.

### 27. ¿Qué uso le da el cliente a la moto? 🟢

- **Entrevistas:** domina el **trabajo** (8 de 25), seguido de mixto trabajo/recados (3) y mensajería/reparto (2); el uso personal puro es minoritario (2). Los talleres también reportan uso laboral.
- **Dataset:** no clasifica uso, pero la evidencia cualitativa es consistente.

---

## Bloque 6 — Canales, confianza y futuro

### 28. ¿Qué canal domina la compraventa: Revolico, Facebook, Telegram, importadoras o conocidos? 🟡

- **Dataset:** toda la muestra cuantitativa proviene de **Revolico**, así que no permite comparar canales.
- **Entrevistas:** aparecen **Revolico** (`COMPRADOR_018`, `019`), **Facebook** (`COMPRADOR_020`), **conocido** (`COMPRADOR_025`) e **importación/Panamá** (`COMPRADOR_023`); la importadora es un canal formal.
- **Conclusión:** Revolico domina la evidencia cuantitativa por diseño del scraping; los otros canales solo están documentados cualitativamente.

### 29. ¿Qué tan importante es la garantía y la confianza en el vendedor al comprar una moto usada? 🟡

- **Dataset:** **69 anuncios** mencionan “garantía”.
- **Entrevistas:** la importadora recomienda revisar la ficha técnica para no pagar de más; un taller menciona garantía, pero el dato quedó por confirmar. La confianza en el vendedor aparece como tema, sin medición.
- **Límite:** no hay una escala de confianza ni de disposición a pagar por garantía.

### 30. ¿Cómo imagina el mercado de motos en La Habana en los próximos 2 o 3 años? 🟡

- **Señales cualitativas:** la importadora ve **avance de lo eléctrico**; `COMPRADOR_025` afirma que hoy elegiría **combustión** por practicidad y seguridad; varios entrevistados condicionan la eléctrica a los **apagones** y a la **batería**.
- **Lo que no hay:** el proyecto no tiene modelo de pronóstico ni serie temporal suficiente. La respuesta debe presentarse como **escenario cualitativo**, no como proyección.

---

## Resumen de cobertura

| Nivel | Preguntas | Total |
|---|---|---:|
| 🟢 Responde con datos | 4, 8, 9, 27 | 4 |
| 🟡 Responde parcialmente o solo con entrevistas | 1, 2, 3, 6, 10, 12, 13, 15, 16, 18, 19, 24, 25, 26, 28, 29, 30 | 17 |
| 🔴 No responde todavía | 5, 7, 11, 14, 17, 20, 21, 22, 23 | 9 |

## Qué haría falta para cerrar las brechas

1. **Geolocalizar o extraer el municipio** de los anuncios (pregunta 5).
2. **Scrapear más de un periodo** para medir crecimiento y variación de precios (preguntas 1, 7, 21).
3. **Añadir campos** de condición (nueva/usada), país de importación y uso declarado (preguntas 7, 15).
4. **Ampliar la muestra cualitativa** en remesas y talleres, y confirmar la identidad de los 4 talleres (preguntas 11, 22, 23).
5. **Verificar aranceles y regulaciones** con fuente oficial (preguntas 14, 17).
6. **Módulo específico de repuestos** con piezas, tiempos y precios (preguntas 19–21).

---

*Documento generado a partir de `data/processed/anuncios_limpios.csv`, `reports/metricas/resumen_mercado.json`, `docs/entrevistas/*.json` y `docs/entrevistas/analisis_lote_2026-11-05.md`.*
