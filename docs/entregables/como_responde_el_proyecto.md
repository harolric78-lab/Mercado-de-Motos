# Cómo responde el proyecto a las 30 preguntas del mercado de motos en La Habana

Documento de trabajo que acompaña a `preguntas.txt`. Explica, para cada pregunta, **con qué evidencia del proyecto se responde**, **qué se encontró** y **qué queda como límite o pendiente**.

## Fuentes del proyecto

| Fuente | Qué aporta | Cobertura |
|---|---|---|
| Dataset de anuncios (`data/processed/anuncios_limpios.csv`) | Precios, categorías, marcas, vistas y menciones en los textos | **6.101 anuncios** de Revolico (La Habana), del **2026-10-10 al 2026-10-26** |
| Entrevistas cualitativas (`docs/entrevistas/`) | Preferencias, gastos, repuestos, apagones, canales y percepciones | **30 entrevistas**: 25 compradores, 4 talleres y 1 importadora |
| Informes (`reports/`) | Tablas y gráficos agregados | `informe_mercado.md`, `resumen_mercado.json`, `graficos/` |
| Análisis cualitativo (`docs/entrevistas/analisis_lote_2026-11-05.md`) | Lectura transversal de las entrevistas | 25 compradores + talleres |
| Fuentes oficiales (`docs/entregables/respuestas_fuentes_oficiales.md`) | Normas, impuestos, valores de referencia, tipo de cambio y requisitos legales | Gaceta Oficial (2020-2026), BCC y ONEI |

**Leyenda:** 🟢 el proyecto lo responde con datos; 🟡 lo responde parcialmente o solo con entrevistas; 🔴 no lo responde todavía (queda como pendiente).

> Actualización 06/11/2026: la revisión de fuentes oficiales cambió el veredicto de cinco preguntas (7, 14, 17, 21 y 23) y reforzó la 10 y la 16. El detalle está en `respuestas_fuentes_oficiales.md`. El conteo pasa de 4/17/9 a **5/21/4**.

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
- **Diferencia de papeles (fuente oficial):** ambas requieren licencia (categoría A para motos, A1 para ciclomotores), registro, chapa trasera y revisión técnica; la ley no crea un permiso distinto para eléctricas. La diferencia está en la importación: la eléctrica está exenta del Impuesto Aduanero en el canal de comercializadores autorizados y paga 5 % de impuesto especial, frente al 20 % de la combustión (Res. 172/2026).

### 5. ¿Cómo varía la oferta y los precios según la zona de La Habana? 🔴

- **Lo que hay:** el dataset solo registra `ubicacion = "La Habana"` para los 6.101 anuncios; **no trae municipio**. Las entrevistas mencionan zonas (Diez de Octubre, Plaza de la Revolución/Vedado), pero no de forma sistemática.
- **Conclusión:** el proyecto **todavía no puede responder** esta pregunta por zona. Para hacerlo habría que extraer el municipio de los anuncios o geolocalizarlos.

### 6. ¿Qué segmento está creciendo más: uso personal, mensajería, trabajo o alquiler? 🟡

- **Lo que muestran las entrevistas:** el **uso laboral** es el patrón más repetido. De 25 compradores, 8 declaran uso exclusivo de trabajo, 3 mixto (trabajo/recados) y 2 mensajería/reparto; solo 2 declaran uso personal. Los talleres también describen uso de trabajo.
- **Límite:** el dataset no clasifica el uso; la respuesta es cualitativa y de una muestra pequeña.

### 7. ¿El mercado se mueve más por la compra de motos nuevas o por la reventa? 🟡

- **Lo que hay en el dataset:** solo **323 anuncios (5,3 %)** usan la palabra “nueva” y **ninguno** dice explícitamente “usada”. Eso no permite separar compra nueva de reventa.
- **Lo que aporta la fuente oficial:** la **Res. 171/2026** fija valores mínimos para la compraventa y donación de motos usadas por edad (265.000 / 132.500 / 66.250 CUP para motocicletas y triciclos), y la **Res. 172/2026** fija mínimos de impuesto especial para usados (100 USD por motocicleta). Es decir, la reventa es un mercado reconocido y tasado por la ley.
- **Límite:** la norma confirma que existe reventa, pero **no dice qué proporción del mercado es nueva y qué proporción es usada**. Para eso sigue faltando un campo de condición en el scraping.
- **Conclusión:** se responde parcialmente: hay reventa formal y tasada, pero no se puede cuantificar el peso relativo.

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
- **Lo que aporta la fuente oficial:** el BCC fija la tasa oficial en **793,00 CUP/USD** (06/11/2026), con compra en ventanilla a 777,14 y venta a 808,86. A esa tasa, la mediana de combustión (2.250 USD) equivale a **1.784.250 CUP** y la de eléctrica (2.050 USD) a **1.625.650 CUP**.
- **Lectura:** la tasa no cambia el precio en USD; cambia su equivalente en CUP y la capacidad de pago de quien gana en CUP. El mercado de anuncios está dolarizado.
- **Límite:** no se mide el *pass-through* (cuánto sube el precio en USD por cada variación del tipo de cambio) ni se usa la tasa informal. La relación causal sigue sin cuantificar.

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

### 14. ¿Cuál es el impuesto o costo real para importar una moto al país? 🟡

- **Lo que decía la importadora:** `IMPORTADORA_001` menciona una **rebaja de aranceles** y una carga del **5 %**, pero el audio es ruidoso y el dato quedó en `preguntas_pendientes`.
- **Lo que confirma la fuente oficial:** el **5 %** (eléctricas) y el **20 %** (motos y triciclos de combustión) **no son el arancel**, sino el **Impuesto Especial a Productos y Servicios** sobre el precio de venta (Res. 172/2026). Además, la Res. 172/2026 **exonera del Impuesto Aduanero** a los comercializadores autorizados que importan vehículos eléctricos para venderlos en USD; la combustión no tiene esa exención.
- **Costos que sí están publicados:** valor de referencia en aduana (eléctrica 200 USD; combustión 850 USD sin sidecar y 950 con sidecar), servicio de aduana (8 USD para moto/ciclomotor de combustión hasta 250 cc; 2 USD sidecar) y la tarifa comercial progresiva del viajero (15 % hasta 2.000 USD, 20 % hasta 4.000, 25 % hasta 6.000 y 30 % por encima), que **no** es la tarifa del régimen no comercial ordinario.
- **Límite:** la **tarifa ad-valorem exacta** del Impuesto Aduanero para la importación no comercial de motos de combustión no aparece en la Gaceta consultada; la fija el Ministerio de Finanzas y Precios. Por eso no se puede dar un “costo total” exacto.
- **Conclusión:** se conoce la estructura y varios componentes, pero no el tipo exacto del arancel no comercial. La pregunta pasa de 🔴 a 🟡. El detalle está en `respuestas_fuentes_oficiales.md`.

### 15. ¿Qué países y canales de importación son hoy los más usados? 🟡

- **Entrevistas:** un comprador declara haber comprado por **Panamá** (`COMPRADOR_023`); la importadora es la otra fuente directa.
- **Dataset:** los anuncios **no declaran país de origen** (0 menciones a “Panamá”; solo 13 a “importada/importado”). No se puede construir un ranking de países.
- **Conclusión:** respuesta parcial, solo cualitativa.

### 16. ¿Qué requisitos pesan más: licencia, chapa, seguro o registro? 🟡

- **Entrevistas:** `COMPRADOR_025` declara **no tener chapa ni licencia** y haber tenido problemas en la estación; otros mencionan papeles como factor.
- **Dataset:** **47 anuncios** mencionan “papeles” y **60** mencionan “chapa”; ninguno menciona “licencia”.
- **Lo que exige la ley (Ley 109/2010, edición 2026):** licencia de conducción obligatoria (Art. 261), categoría **A** para motocicletas y **A1** para ciclomotores (Art. 264); inscripción en el Registro de Vehículos del MININT (Arts. 215-216); licencia de circulación y chapas que entrega el Registro (Art. 221); una sola chapa trasera para motos (Art. 197) y prohibición de chapas distintas (Art. 198); revisión técnica actualizada (Arts. 211-213); comunicación de cambios en 30 días (Art. 217).
- **Sobre el seguro:** el Código de Seguridad Vial consultado **no lo establece como requisito obligatorio**. Si existe una obligación, proviene de otra norma no revisada.
- **Límite:** la ley dice qué es obligatorio, pero **no mide cuál requisito “pesa más”** para el comprador. Esa parte sigue siendo cualitativa.

### 17. ¿Cómo han cambiado las regulaciones recientes la compra, venta y circulación? 🟢

- **Lo que dice la fuente oficial:** el paquete de 2026 reemplazó el de diciembre de 2024. La Gaceta 65 explica que la actualización responde al “contexto económico actual” y a la necesidad de “contribuir con la transformación de la matriz energética”.
- **Cadena de reemplazo:** Decreto 119/2024 → **Decreto 163/2026** (transmisión, comercialización e importación); Res. 398/2024 → **Res. 172/2026** (precios, impuesto especial y arancel); Res. 397/2024 → **Res. 171/2026** (valores mínimos de compraventa); Res. 180/2024 → **Res. 52/2026** (regulaciones complementarias); Res. 364/2024 → **Res. 340/2026** (importaciones no comerciales); Decreto-Ley 101/2024 → **Decreto-Ley 132/2026** (modifica el DL 22/2020).
- **Cambios concretos:** se exige a los comercializadores autorizados servicio posventa, piezas, personal calificado, equipamiento especializado, asistencia en carretera 24 horas y estaciones de carga para eléctricos (Res. 52/2026, Art. 3); se exonera del Impuesto Aduanero la importación de eléctricos por comercializadores autorizados (Res. 172/2026); se actualizan los valores de referencia y las reglas de importación no comercial (Res. 340/2026).
- **Límite:** se comparan normas y objetivos, no efectos medidos. No hay evaluación oficial del impacto en precios, ventas o circulación.
- **Conclusión:** la pregunta se responde con la normativa oficial; pasa de 🔴 a 🟢.

### 18. ¿Qué riesgo percibe el comprador al adquirir una moto sin papeles o importada informalmente? 🟡

- **Entrevistas:** aparecen casos de **pieza robada o dañada** (`COMPRADOR_023`) y de motos **sin chapa ni licencia** (`COMPRADOR_025`). El análisis cualitativo lo trata como riesgo percibido, no como estadística.
- **Lo que dice la ley:** la chapa debe ser la otorgada por el Registro y se prohíbe cualquier otra (Arts. 197-198); el Registro puede retirar licencia y chapas por modificaciones no autorizadas (Art. 216); el MININT puede ocupar chapas y licencia de circulación e inmovilizar el vehículo en los supuestos del Art. 96 (Art. 98). Eso configura un riesgo legal objetivo.
- **Límite:** no hay cuantificación del riesgo percibido ni de su efecto en el precio; la ley dice qué puede pasar, no cuánto lo teme el comprador.

---

## Bloque 4 — Repuestos y servicio técnico

### 19. ¿Cuáles son las piezas y accesorios que más frecuentemente se rompen? 🟡

- **Entrevistas:** problemas de **piezas, aceite y neumático** en combustión (`COMPRADOR_018`); **puño de acelerar** por el clima y desgaste de **plásticos/estética** en eléctrica (`COMPRADOR_025`); averías y repuestos en talleres (`TALLER_001`–`TALLER_004`).
- **Dataset:** los anuncios no describen fallas (0 menciones a “repuesto”), así que no se puede construir un ranking de piezas.

### 20. ¿Qué repuestos son los más difíciles de conseguir y cuánto demoran? 🔴

- Las entrevistas confirman que **conseguir repuestos es un problema** (`COMPRADOR_018`, talleres), pero no identifican de forma consistente cuáles ni los tiempos.
- **Lo que aporta la fuente oficial:** la Res. 340/2026 lista valores de referencia para muchas piezas (baterías, neumáticos, carburador, amortiguadores, etc.), pero **no dice nada sobre disponibilidad ni tiempos de demora**. Tener un valor de aduana no es tener el repuesto en el taller.
- **Conclusión:** el proyecto lo deja en `preguntas_pendientes`; falta un módulo específico de repuestos que mida disponibilidad y demora.

### 21. ¿Cómo son los precios de los repuestos respecto al año pasado? 🟡

- **Lo que hay en el proyecto:** no hay serie temporal de precios de repuestos (el dataset cubre 17 días y no es de repuestos). Las entrevistas no dan una comparación clara con el año anterior.
- **Lo que aporta la fuente oficial:** la **Res. 340/2026** publica valores de referencia actuales para baterías de litio (60 USD), otras baterías (35 USD), kit de gel (100 USD), neumáticos (35 USD), cámaras (5 USD), llantas (35 USD), carburador (40 USD), amortiguadores (15 USD), caja de velocidad (120 USD), asiento (50 USD), tubo de escape (50 USD), rodamientos (20 USD), etc.
- **Límite:** son **valores de aduana**, no precios de venta al público, y no hay en la Gaceta consultada una serie de 2025 para comparar. La pregunta pide la variación anual; eso sigue sin responderse.
- **Conclusión:** se gana una línea base oficial, pero no la comparación con el año pasado. Pasa de 🔴 a 🟡.

### 22. ¿La disponibilidad de talleres y mecánicos alcanza para la demanda actual? 🔴

- Se entrevistaron **4 talleres**, pero su identidad como talleres **no está confirmada** (la asignación viene de la carpeta de origen). No hay censo de talleres ni de capacidad.
- **Lo que aporta la fuente oficial:** la Res. 52/2026 exige servicio posventa a los **comercializadores autorizados**, pero no crea un censo ni mide la capacidad del resto de los talleres. La mayor parte del mercado informal queda fuera de esa obligación.
- **Conclusión:** pendiente; la norma no sustituye un censo.

### 23. ¿Qué tan fácil es encontrar un mecánico que trabaje con motos eléctricas? 🟡

- **Lo que hay en el proyecto:** los 4 talleres entrevistados hablan de eléctricas, pero no se puede generalizar. No hay datos de cobertura ni de especialización.
- **Lo que aporta la fuente oficial:** la **Res. 52/2026** obliga a los comercializadores autorizados a ofrecer servicio posventa en todo el país, con personal calificado, equipamiento especializado, literatura de servicio y asistencia en carretera 24 horas; también exige estaciones de carga para los vehículos eléctricos que importen.
- **Límite:** la norma crea una obligación para el **canal formal**, pero no mide la facilidad real de encontrar un mecánico, sobre todo en el mercado informal, que es donde se mueve la mayor parte de los anuncios.
- **Conclusión:** hay una base institucional parcial; pasa de 🔴 a 🟡, no a 🟢.

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
| 🟢 Responde con datos | 4, 8, 9, 17, 27 | 5 |
| 🟡 Responde parcialmente o solo con entrevistas | 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30 | 21 |
| 🔴 No responde todavía | 5, 11, 20, 22 | 4 |

> Cambio respecto al corte del 05/11/2026: 4/17/9 → **5/21/4**. La revisión de fuentes oficiales cerró la 17 y abrió parcialmente la 7, 14, 21 y 23. El detalle está en `respuestas_fuentes_oficiales.md`.

## Qué haría falta para cerrar las brechas

1. **Geolocalizar o extraer el municipio** de los anuncios (pregunta 5).
2. **Scrapear más de un periodo** para medir crecimiento y variación de precios (preguntas 1, 7, 21).
3. **Añadir campos** de condición (nueva/usada), país de importación y uso declarado (preguntas 7, 15).
4. **Ampliar la muestra cualitativa** en remesas y talleres, y confirmar la identidad de los 4 talleres (preguntas 11, 22, 23).
5. **Solicitar a la Aduana o al MFP la tarifa ad-valorem exacta** de la importación no comercial de motos de combustión (pregunta 14). La Gaceta consultada no la publica.
6. **Módulo específico de repuestos** con piezas, tiempos y precios (preguntas 19–21).
7. **Censo o muestreo de talleres** para medir capacidad y cobertura de mecánicos de eléctricas (preguntas 22–23).

---

*Documento generado a partir de `data/processed/anuncios_limpios.csv`, `reports/metricas/resumen_mercado.json`, `docs/entrevistas/*.json`, `docs/entrevistas/analisis_lote_2026-11-05.md` y `docs/entregables/respuestas_fuentes_oficiales.md`.*
