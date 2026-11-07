# Respuestas a las 17 preguntas previamente sin responder

**Objetivo:** Reformular si es necesario cada una de las 17 preguntas que quedaban sin responder y identificar fuentes oficiales o datos que permitan responderlas.

**Fecha de corte:** 06/11/2026  
**Regla:** solo se afirma lo que está escrito en la fuente oficial o declarado explícitamente en las entrevistas. Cuando el dato no aparece, se declara como límite.

---

## Resumen de estado de las 17 preguntas

| # | Pregunta (resumen) | Estado anterior | Estado actual | ¿Responde con datos? | Fuente principal |
|---|---|---|---|---|---|
| 7 | Mercado nuevo vs. reventa | 🔴 | 🟡 | Parcial | Res. 171/2026, Res. 172/2026, entrevistas |
| 11 | Influencia de remesas | 🔴 | 🔴 | No | Sin vínculo oficial remesas→motos |
| 12 | Qué pesa más al elegir | 🔴 | 🟡 | Parcial | Entrevistas (precio, autonomía, marca) |
| 13 | Costo de cambiar batería | 🔴 | 🟡 | Parcial | Res. 340/2026, entrevistas |
| 14 | Impuesto/costo de importar | 🔴 | 🟡 | Parcial | Res. 340/2026, 172/2026, 175/2026, 197/2026 |
| 15 | Países y canales de importación | 🔴 | 🟡 | Parcial | Entrevistas (Panamá), importadora |
| 16 | Requisitos: licencia, chapa, seguro, registro | 🔴 | 🟡 | Parcial | Ley 109/2010 (Ed. 2026) |
| 18 | Riesgo de comprar sin papeles | 🔴 | 🟡 | Parcial | Ley 109/2010 (Arts. 197-198, 215-217) |
| 19 | Piezas que más se rompen | 🔴 | 🟡 | Parcial | Entrevistas (batería, plásticos, frenos) |
| 20 | Repuestos más difíciles y demoras | 🔴 | 🔴 | No | Sin datos oficiales de disponibilidad/demora |
| 21 | Precios de repuestos vs. año pasado | 🔴 | 🟡 | Parcial | Res. 340/2026 (valores actuales, no serie) |
| 22 | Talleres y mecánicos vs. demanda | 🔴 | 🔴 | No | Sin censo; Res. 52/2026 solo canal autorizado |
| 23 | Mecánico de eléctricas | 🔴 | 🟡 | Parcial | Res. 52/2026 (obligación a comercializadores) |
| 24 | Influencia de los apagones | 🔴 | 🟡 | Parcial | Entrevistas (apagones afectan carga) |
| 25 | Dónde y cómo carga la gente | 🔴 | 🟡 | Parcial | Entrevistas (carga en casa, apagones) |
| 26 | Autonomía real vs. prometida | 🔴 | 🟡 | Parcial | Entrevistas divergentes (brecha anunciada/real) |
| 30 | Mercado en 2 o 3 años | 🔴 | 🟡 | Parcial | Escenarios cualitativos; sin pronóstico |

**Resultado:** 4 siguen sin respuesta oficial (5, 11, 20, 22), 13 tienen base parcial.

---

## 7. Mercado nuevo vs. reventa

### Pregunta original
¿El mercado se mueve más por la compra de motos nuevas o por la reventa?

### Reformulación
¿Qué proporción del mercado de motos en La Habana corresponde a vehículos nuevos versus usados, y qué valores mínimos fija el sistema tributario para la compraventa de usados?

### Respuesta con datos oficiales

**Lo que sí se sabe:**
- La **Res. 171/2026** fija valores mínimos para impuestos de compraventa y donación de motos y triciclos por antigüedad:
  - Hasta 5 años: 265.000 CUP
  - Más de 5 hasta 15 años: 132.500 CUP
  - Más de 15 años: 66.250 CUP
- La **Res. 172/2026** fija mínimos de impuesto especial para usados: 100 USD por motocicleta de combustión.
- El sistema tributario reconoce y tasa la **reventa** de motos por edad.

**Lo que NO se sabe:**
- No hay dato oficial de qué proporción del mercado es nueva y qué proporción es usada.
- Los anuncios de Revolico no traen campo de condición (nueva/usada).

**Conclusión:** Parcial. Se confirma que el mercado de usados existe y está tasado, pero no se puede cuantificar su peso relativo. Se necesita añadir campo de condición al scraping o encuesta directa.

**Fuentes:** Res. 171/2026 (GOC-2026-429-O65), Res. 172/2026 (GOC-2026-430-O65).

---

## 11. Influencia de remesas

### Pregunta original
¿Cuánto influyen las remesas y los familiares en el exterior en la decisión de compra?

### Reformulación
¿Existe algún vínculo oficial o estadístico entre remesas familiares y la compra de motos en Cuba, y qué porcentaje de compradores declara usar remesas para financiar la moto?

### Respuesta con datos oficiales

**Lo que sí se sabe:**
- No hay vínculo oficial remesas→motos en ninguna norma consultada (Gaceta Oficial, BCC, ONEI).
- Solo **1 de 25 entrevistados** (COMPRADOR_012) declara recibir remesas casi todos los meses y usarlas para la moto.
- COMPRADOR_012 recibe remesas casi mensuales e ingreso declarado de ~4.200 CUP; compró una combustión nueva por importadora de Panamá.

**Lo que NO se sabe:**
- No hay estadística oficial de cuántos compradores de motos financian su compra con remesas.
- No hay dato del BCC o ONEI que cruce remesas con compra de vehículos.

**Conclusión:** No respondible con datos actuales. Requiere añadir pregunta directa de remesas al cuestionario de entrevistas y ampliar la muestra, o solicitar datos al BCC sobre uso de remesas para bienes duraderos.

**Fuentes:** Entrevistas (COMPRADOR_012), BCC (sin vínculo publicado), ONEI (sin dato).

---

## 12. Qué pesa más al elegir

### Pregunta original
¿Qué pesa más al elegir: el precio, la autonomía, la marca o la disponibilidad de repuestos?

### Reformulación
¿Qué factores declaran los entrevistados como decisivos al elegir una moto, y hay un ranking uniforme o prioridad clara entre precio, autonomía, marca y repuestos?

### Respuesta con datos (entrevistas)

**Lo que sí se sabe (declaraciones de entrevistados):**
- **COMPRADOR_003:** "El motor de combustión rinde mejor en largas distancias y el motor dura más que una batería eléctrica". Le gusta más: mejor rendimiento en largas distancias. Le gusta menos: precio elevado de la gasolina.
- **COMPRADOR_004:** Elige eléctrica por "dificultad para conseguir gasolina, precio irregular y riesgo de quedarse sin transporte".
- **COMPRADOR_005:** Prefiere combustión porque "con gasolina disponible se puede planificar cuándo repostar y seguir circulando; la eléctrica depende de encontrar un lugar con corriente".
- **COMPRADOR_006:** "El costo de operación es mucho menor; los factores con más peso fueron la autonomía y el precio."
- **COMPRADOR_007:** Prefiere eléctrica "pese a la situación de la electricidad, porque el precio de la gasolina le resulta imposible."
- **COMPRADOR_012:** "El precio fue el factor decisivo". Usa remesas de la familia.
- **COMPRADOR_013:** Prefiere gasolina para viajes largos y eléctrica como respaldo cuando no hay electricidad.
- **COMPRADOR_019:** Prefiere gasolina por "rendimiento y kilometraje".

**Lo que NO se sabe:**
- No hay ranking uniforme aplicado a toda la muestra. Cada entrevistado prioriza distinto factor según su contexto.
- No se puede afirmar cuál factor "pesa más" de forma estadística.

**Conclusión:** Parcial. Hay evidencia cualitativa de que precio, autonomía y disponibilidad de combustible son factores clave, pero no hay un ranking cuantificado.

**Fuentes:** Entrevistas (COMPRADOR_003, 004, 005, 006, 007, 012, 013, 019).

---

## 13. Costo de cambiar batería

### Pregunta original
¿Qué pasa con el costo de una eléctrica cuando hay que cambiar la batería?

### Reformulación
¿Qué costo tiene reemplazar la batería de una moto eléctrica, y qué valor de referencia oficial existe para baterías de litio?

### Respuesta con datos

**Lo que sí se sabe:**
- **Res. 340/2026** (Anexo II, cap. 8): valor de referencia en aduana de **baterías o acumuladores de litio: 60 USD**. Otras baterías y acumuladores: 35 USD. Kit de gel: 100 USD.
- **COMPRADOR_006:** Batería rinde hasta ~1.600 horas de funcionamiento.
- **COMPRADOR_017:** Va por la tercera batería a los 11 años; la última costó unos **900 USD**.
- **COMPRADOR_009:** Compró batería más grande por **800 USD**.

**Lo que NO se sabe:**
- Los 60 USD de Res. 340/2026 son **valor de aduana**, no precio de venta al público.
- No hay precio de mercado oficial para baterías de reemplazo en Cuba.
- No hay serie temporal de precios de baterías.

**Conclusión:** Parcial. Existe valor de referencia aduanero (60 USD litio) y declaraciones de compradores (800-900 USD), pero no hay precio de mercado oficial ni serie temporal.

**Fuentes:** Res. 340/2026, entrevistas (COMPRADOR_006, 009, 017).

---

## 14. Impuesto o costo real de importar

### Pregunta original
¿Cuál es el impuesto o costo real para importar una moto al país?

### Reformulación
¿Qué componentes del costo de importación de una moto están publicados en la Gaceta Oficial, y cuál componente sigue sin publicarse?

### Respuesta con datos oficiales

**Lo que sí se sabe (Res. 172/2026, 340/2026, 175/2026, 197/2026):**

| Componente | Eléctrica | Combustión | Fuente |
|---|---|---|---|
| Valor de referencia en aduana | 200 USD | 850 USD (sin sidecar); 950 USD (con sidecar) | Res. 340/2026 |
| Servicio de aduana | No detalla tarifa específica | 8 USD (hasta 250 cc) | Res. 175/2026 |
| Impuesto especial sobre venta | 5 % | 20 % | Res. 172/2026 |
| Arancel de importación (canal comercial) | Exento para comercializadores autorizados | El que corresponda (no publicado) | Res. 172/2026 |
| Margen comercial (servicios de importación) | Hasta 3 % | Hasta 3 % | Res. 172/2026 |
| Tarifa comercial progresiva (viajero) | 15 % hasta 2.000 USD; 20 % hasta 4.000; 25 % hasta 6.000; 30 % >6.000 | Igual | Res. 197/2026 |

**Ejemplo ilustrativo (no costo oficial):**
- Eléctrica vendida a 2.050 USD: impuesto especial = 102,50 USD.
- Combustión vendida a 2.250 USD: impuesto especial = 450 USD.

**Lo que NO se sabe:**
- La **tarifa ad-valorem exacta** del Impuesto Aduanero para importación no comercial de motos de combustión no está publicada. El Decreto-Ley 22/2020 solo establece que es ad-valorem; la escala concreta la fija el MFP.

**Conclusión:** Parcial. Se conocen la estructura, valores de referencia, servicios de aduana e impuesto especial, pero falta el arancel ad-valorem exacto de combustión.

**Fuentes:** Res. 340/2026, Res. 172/2026, Res. 175/2026, Res. 197/2026, Decreto-Ley 22/2020.

---

## 15. Países y canales de importación

### Pregunta original
¿Qué países y canales de importación son hoy los más usados (Panamá, Estados Unidos, otros)?

### Reformulación
¿Qué países de origen y canales de importación declaran los entrevistados y las normas oficiales para la importación de motos?

### Respuesta con datos

**Lo que sí se sabe (entrevistas):**
- **COMPRADOR_012:** Compró combustión nueva por **importadora de Panamá**, entrega en casa.
- **COMPRADOR_017:** Importó desde **Panamá** por ~1.640 USD.
- **COMPRADOR_023:** Compró por **Panamá** (importación).
- **COMPRADOR_020:** Compró por **Facebook** (usada).
- **COMPRADOR_010:** Moto regalada; dueño anterior la compró por Facebook.
- **COMPRADOR_006:** Compró a un **conocido que importa vehículos eléctricos**.
- **IMPORTADORA_001 (Solimport):** Origen principal **China**; canales: compra al proveedor en el exterior, transporte, nacionalización en aduana, aranceles, impuesto sobre ventas y margen comercial.

**Lo que NO se sabe:**
- Los anuncios de Revolico no declaran país de importación.
- No hay estadística oficial de cuántas motos entran por cada país o canal.

**Conclusión:** Parcial. Panamá y Facebook aparecen en entrevistas; China como origen según la importadora. No hay dato cuantitativo de cuál canal domina.

**Fuentes:** Entrevistas, IMPORTADORA_001.

---

## 16. Requisitos: licencia, chapa, seguro, registro

### Pregunta original
¿Qué requisitos pesan más para el comprador: licencia, chapa, seguro o registro?

### Reformulación
¿Qué requisitos legales establece la normativa para comprar y circular una moto en Cuba, y cuál de ellos aparece como obligatorio en el Código de Seguridad Vial?

### Respuesta con datos oficiales (Ley 109/2010, Edición 2026)

**Requisitos establecidos por la ley:**
| Requisito | Artículo | Estado |
|---|---|---|
| Licencia de conducción | Art. 261 | Obligatoria |
| Categoría A (motos) / A1 (ciclomotores) | Art. 264 | Obligatoria |
| Registro de Vehículos (MININT) | Arts. 215-216 | Obligatorio |
| Licencia de circulación | Art. 221 | Se entrega al inscribir |
| Chapa trasera única | Art. 197 | Obligatoria (una sola) |
| Prohibición de chapas no del Registro | Art. 198 | Obligatoria |
| Revisión técnica | Arts. 211-213 | Obligatoria y certificado actualizado |
| Comunicar cambios al Registro en 30 días | Art. 217 | Obligatorio |
| Casco protector | Art. 72 | Obligatorio |

**Sobre el seguro:**
- El Código de Seguridad Vial consultado **no establece el seguro como requisito obligatorio** para circular.
- Si existe una obligación de seguro, proviene de otra norma no revisada.

**Conclusión:** Parcial. Se saben los requisitos legales, pero no se puede medir cuál "pesa más" para el comprador (eso requiere encuesta directa). El seguro no aparece como obligatorio en el Código consultado.

**Fuentes:** Ley 109/2010, Código de Seguridad Vial, edición anotada 2026 (GOC-2026-ES10).

---

## 18. Riesgo de comprar sin papeles

### Pregunta original
¿Qué riesgo percibe el comprador al adquirir una moto sin papeles o importada informalmente?

### Respuesta con datos (ley + entrevistas)

**Riesgo legal objetivo (Ley 109/2010):**
- Art. 197: Las motocicletas llevan una sola chapa en la parte posterior, expedida por el Registro.
- Art. 198: Se prohíbe cualquier chapa distinta a la otorgada por el Registro.
- Art. 215-216: El Registro de Vehículos (MININT) puede retirar licencia y chapas por modificaciones no autorizadas.
- Art. 96/98: El MININT puede ocupar chapas y licencia de circulación e inmovilizar el vehículo en supuestos determinados.

**Riesgo percibido (entrevistas):**
- COMPRADOR_010: No tiene chapa ni licencia.
- COMPRADOR_016: No tiene chapa ni licencia; dice que aún no lo ha logrado.
- COMPRADOR_025: Sin chapa ni licencia; "ha estado en la estación por eso".
- COMPRADOR_023: Menciona una pieza robada o dañada.
- COMPRADOR_024: Se le robó o dañó una pieza una vez.

**Conclusión:** Parcial. Existe riesgo legal objetivo (inmovilización, ocupación de chapas) y riesgo percibido (entrevistas), pero no hay cuantificación estadística del riesgo ni de su efecto en el precio.

**Fuentes:** Ley 109/2010 (Arts. 197-198, 215-217, 96-98), entrevistas.

---

## 19. Piezas que más se rompen

### Pregunta original
¿Cuáles son las piezas y accesorios que más frecuentemente se rompen?

### Respuesta con datos (entrevistas)

**Lo que sí se sabe (declaraciones de entrevistados y talleres):**

| Pieza/accesorio | Quién lo menciona | Contexto |
|---|---|---|
| Batería | COMPRADOR_006, 009, 017, 020, 025 | Costo principal de eléctricas; dura 2-5 años |
| Frenos | COMPRADOR_006, 014 | Cambio de freno reportado |
| Plásticos | COMPRADOR_025 | "Más en plásticos y estética que en problemas técnicos" |
| Neumáticos | COMPRADOR_018 | Problemas con neumático en dos años |
| Aceite | COMPRADOR_018 | Problemas con aceite |
| Piezas generales | COMPRADOR_018 | "Problemas con piezas" |
| Carburador | (no mencionado en entrevistas) | — |
| Amortiguador | (no mencionado en entrevistas) | — |

**Talleres (identidad no confirmada):**
- TALLER_001: "Menciona la compra de una pieza, pero no se entiende cuál ni el costo."
- TALLER_004: Menciona una avería, no inteligible.

**Lo que NO se sabe:**
- No hay estadística oficial de fallas por pieza.
- No hay conteo de cuántas veces se rompe cada pieza.

**Conclusión:** Parcial. Las entrevistas mencionan batería, frenos, plásticos, neumáticos, aceite y piezas generales, pero no hay estadística de fallas.

**Fuentes:** Entrevistas (COMPRADOR_006, 009, 014, 017, 018, 020, 025), Res. 340/2026 (valores de referencia, no fallas).

---

## 20. Repuestos más difíciles y demoras

### Pregunta original
¿Qué repuestos son los más difíciles de conseguir y cuánto demoran?

### Respuesta con datos oficiales

**Lo que sí se sabe:**
- No hay datos oficiales de disponibilidad de repuestos ni tiempos de demora.
- Res. 340/2026 publica valores de referencia de repuestos, pero no dice nada sobre disponibilidad ni demora.
- Las entrevistas confirman que conseguir repuestos es un problema, pero no identifican piezas ni tiempos de forma consistente.

**Lo que NO se sabe:**
- Qué repuestos son más difíciles de conseguir.
- Cuánto demoran en conseguirse.

**Conclusión:** No respondible con datos actuales. Requiere módulo específico de repuestos en entrevistas a talleres y compradores, con seguimiento de precios y tiempos.

**Fuentes:** Res. 340/2026 (solo valores de aduana), entrevistas (sin dato consistente).

---

## 21. Precios de repuestos vs. año pasado

### Pregunta original
¿Cómo son los precios de los repuestos respecto al año pasado?

### Reformulación
¿Qué valores de referencia oficiales existen hoy para repuestos de motos, y existe alguna serie oficial del año anterior para comparar?

### Respuesta con datos oficiales

**Lo que sí se sabe (Res. 340/2026, Anexo II, cap. 8):**

| Repuesto | Valor de referencia (USD) |
|---|---:|
| Baterías o acumuladores de litio | 60 |
| Otras baterías y acumuladores | 35 |
| Kit o set de baterías de gel | 100 |
| Neumáticos para motos o ciclomotores | 35 |
| Cámaras para neumáticos | 5 |
| Llantas para motos o ciclomotores | 35 |
| Carburador | 40 |
| Delco (distribuidor) | 30 |
| Guardafangos | 40 |
| Parabrisas | 150 |
| Amortiguadores | 15 |
| Bobina de encendido | 5 |
| Cajas de velocidad | 120 |
| Asiento para moto o ciclomotor | 50 |
| Tubo de escape de autos y motos | 50 |
| Rodamientos | 20 |
| Válvulas de motor | 5 |

**Lo que NO se sabe:**
- No hay en la Gaceta consultada una serie del año anterior que permita decir si los repuestos subieron o bajaron.
- Son valores de aduana, no precios de venta al público.

**Conclusión:** Parcial. Existe línea base oficial de octubre 2026, pero no hay serie temporal para medir variación anual.

**Fuentes:** Res. 340/2026.

---

## 22. Talleres y mecánicos vs. demanda

### Pregunta original
¿La disponibilidad de talleres y mecánicos alcanza para la demanda actual?

### Respuesta con datos oficiales

**Lo que sí se sabe:**
- La **Res. 52/2026** exige a los comercializadores autorizados servicio posventa, piezas, personal calificado, equipamiento especializado, asistencia en carretera 24 horas y estaciones de carga para vehículos eléctricos.
- Esta obligación solo cubre a los **comercializadores autorizados**, no al resto de talleres.
- No hay censo de talleres ni de capacidad en la Gaceta consultada.

**Lo que NO se sabe:**
- Cuántos talleres existen en La Habana.
- Cuántos mecánicos hay.
- Si la capacidad alcanza para la demanda actual.
- Cómo funciona el mercado informal de reparación.

**Conclusión:** No respondible con datos actuales. Requiere censo o muestreo de talleres. La norma solo obliga al canal autorizado.

**Fuentes:** Res. 52/2026.

---

## 23. Mecánico de eléctricas

### Pregunta original
¿Qué tan fácil es encontrar un mecánico que trabaje con motos eléctricas?

### Respuesta con datos oficiales

**Lo que sí se sabe:**
- La **Res. 52/2026** obliga a los comercializadores autorizados a tener personal calificado, equipamiento especializado, literatura de servicio, asistencia en carretera 24 horas y estaciones de carga para vehículos eléctricos.
- Esto aplica solo al canal formal (comercializadores autorizados).

**Lo que NO se sabe:**
- Qué tan fácil es encontrar un mecánico de eléctricas en el mercado informal.
- Cuántos mecánicos están capacitados en eléctricas en La Habana.
- Cobertura geográfica del servicio de eléctricas.

**Conclusión:** Parcial. La norma crea una obligación para el canal formal, pero no mide la facilidad real de encontrar mecánico, sobre todo en el canal informal donde se mueve la mayor parte del mercado.

**Fuentes:** Res. 52/2026.

---

## 24. Influencia de los apagones

### Pregunta original
¿Cuánto influyen los apagones en la decisión de comprar una eléctrica?

### Respuesta con datos (entrevistas)

**Lo que sí se sabe (declaraciones):**
- COMPRADOR_005: La eléctrica "depende de encontrar un lugar con corriente".
- COMPRADOR_007: Está en un circuito que no le afecta tanto cuando el sistema es estable; cuando es crítica también le afecta.
- COMPRADOR_008: En su zona la electricidad es inestable.
- COMPRADOR_014: Los apagones afectan la carga; a veces carga donde un vecino.
- COMPRADOR_016: Los apagones complican la carga; carga cada 1-2 días según la corriente.
- COMPRADOR_020: Autonomía ha disminuido con el tiempo (posiblemente relacionado con carga/descarga).
- COMPRADOR_023: Los apagones afectan mucho.
- COMPRADOR_025: Carga todos los días, a veces dos veces; los apagones le impiden usarla en ocasiones.
- COMPRADOR_007: Carga cada 4-5 días, tarda unas 7 horas.

**Lo que NO se sabe:**
- No hay dato cuantitativo de cuántos compradores dejan de comprar eléctrica por los apagones.
- Solo 1 anuncio en el dataset menciona apagón.

**Conclusión:** Parcial. Los apagones son una restricción operativa concreta mencionada por varios entrevistados, pero no hay medición estadística de su influencia en la decisión de compra.

**Fuentes:** Entrevistas (COMPRADOR_005, 007, 008, 014, 016, 020, 023, 025, 007).

---

## 25. Dónde y cómo carga la gente

### Pregunta original
¿Dónde y cómo carga la gente que vive en edificios o zonas con poco espacio?

### Respuesta con datos (entrevistas)

**Lo que sí se sabe:**
- COMPRADOR_004: Carga en casa de su novia cuando no hay electricidad en la suya.
- COMPRADOR_006: Carga cada 2 o 3 días completos; demora entre 6 y 8 horas; la hace en casa durante la noche.
- COMPRADOR_007: Carga aproximadamente cada 4 o 5 días; tarda unas 7 horas.
- COMPRADOR_008: Carga normalmente cada dos días; no precisa el tiempo.
- COMPRADOR_014: Menciona unas 8 horas de carga (fragmento confuso).
- COMPRADOR_016: Carga cada 1-2 días según la corriente; deja descansar la moto 20 minutos entre usos.
- COMPRADOR_023: Carga la moto por la noche.
- COMPRADOR_025: Carga todos los días y a veces dos veces al día.

**Lo que NO se sabe:**
- No hay datos sistemáticos sobre dónde carga la gente que vive en edificios o zonas con poco espacio.
- No hay dato sobre infraestructura de carga pública.

**Conclusión:** Parcial. Las entrevistas describen carga en casa, carga nocturna, carga en casa de vecinos, y tiempos de 6-8 horas, pero no hay dato sistemático sobre vivienda en edificios o zonas con poco espacio.

**Fuentes:** Entrevistas (COMPRADOR_004, 006, 007, 008, 014, 016, 023, 025).

---

## 26. Autonomía real vs. prometida

### Pregunta original
¿La autonomía real de las eléctricas coincide con la que promete el vendedor?

### Respuesta con datos (entrevistas)

**Lo que sí se sabe (brecha anunciada vs. real):**

| Entrevistado | Prometido | Real declarado | Brecha |
|---|---|---|---|
| COMPRADOR_014 | 80-100 km | 50-69 km | ~20-31 km menos |
| COMPRADOR_006 | 80 km | ~70 km reales; -15 % tras años | ~10 km menos + degradación |
| COMPRADOR_016 | Anunciada para un peso | Rinde menos por llevar más carga | Menor por carga extra |
| COMPRADOR_020 | — | Disminuyó con el tiempo | — |
| COMPRADOR_025 | Era real al principio | Ha ido disminuyendo | Degradación temporal |
| COMPRADOR_017 | — | 75 km (no claro si real o anunciada) | — |
| COMPRADOR_008 | El vendedor decía que era real | Disminuye con el uso y el tiempo | — |
| TALLER_004 | — | Varía según peso, velocidad y lomas | — |

**Lo que NO se sabe:**
- No hay mediciones propias de autonomía real.
- No hay dato sistemático de la brecha promedio.

**Conclusión:** Parcial. Existe una brecha clara entre lo anunciado y lo real en varios casos (ej. 80-100 km prometido vs. 50-69 km real), pero no hay medición sistemática ni promedio calculable.

**Fuentes:** Entrevistas (COMPRADOR_006, 008, 014, 016, 017, 020, 025, TALLER_004).

---

## 30. Mercado en 2 o 3 años

### Pregunta original
¿Cómo imagina el mercado de motos en La Habana en los próximos 2 o 3 años?

### Respuesta con datos (escenarios cualitativos)

**Lo que sí se sabe (escenarios cualitativos de entrevistas):**
- COMPRADOR_002: "La combustión seguirá siendo relevante; el combustible es una fuente finita y no renovable."
- COMPRADOR_006: "Seguiría eligiendo eléctrica para el uso diario en la ciudad; solo elegiría gasolina si necesitara recorrer largas distancias con frecuencia."
- COMPRADOR_012: "Considera el mercado legal y que adquirir un transporte hoy es un buen negocio."
- COMPRADOR_013: Prefiere gasolina para viajes largos y eléctrica como respaldo cuando no hay electricidad (lógica híbrida).
- IMPORTADORA_001: "El avance se inclina hacia los equipos eléctricos; la compra de combustión se mantiene por la situación del combustible." Razones: situación económica, situación del combustible, incentivo arancelario.
- IMPORTADORA_001: "La reventa fija precios muy por encima del oficial."

**Lo que NO se sabe:**
- No hay modelo de pronóstico cuantitativo.
- No hay dato oficial de proyección de ventas o precios a 2-3 años.

**Conclusión:** Parcial. Existen escenarios cualitativos (tendencia hacia eléctricas, combustión mantiene nicho de largas distancias), pero no hay pronóstico cuantitativo.

**Fuentes:** Entrevistas (COMPRADOR_002, 006, 012, 013), IMPORTADORA_001.

---

## Plan de acción para cerrar las 4 preguntas aún sin respuesta (5, 11, 20, 22)

| # | Pregunta | Qué falta | Cómo cerrarla |
|---|---|---|---|
| 5 | Oferta y precios por municipio | Municipio por anuncio | Extraer municipio del texto del anuncio o geolocalizar; cruzar con entrevistas por zona |
| 11 | Peso de las remesas | Pregunta directa y muestra | Añadir pregunta de remesas al cuestionario; no hay vínculo oficial remesas→motos |
| 20 | Repuestos más difíciles y demoras | Módulo de repuestos | Entrevistas a talleres y compradores con pieza, tiempo y precio; seguimiento |
| 22 | Censo de talleres | Censo o muestreo de talleres | Censo geolocalizado de talleres y mecánicos; capacidad (clientes/día) y demanda |

**Brecha transversal:** La tarifa ad-valorem exacta del Impuesto Aduanero para la importación no comercial de motos de combustión no está publicada. Para cerrarla hay que solicitar la Resolución del MFP que fija la escala o consultar directamente a la Aduana General.

---

## Fuentes y enlaces oficiales

- Ley 109/2010, Código de Seguridad Vial, edición anotada 2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-es10.pdf`
- Gaceta Oficial Ordinaria 65/2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-o65_0.pdf`
- Gaceta Oficial Ordinaria 83/2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-o83.pdf`
- Gaceta Oficial Ordinaria 128/2024: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2024-o128.pdf`
- Decreto-Ley 22/2020: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2020-ex68.pdf`
- BCC, tasas de cambio: `https://www.bc.gob.cu/tasas-de-cambio`
- ONEI, Anuario Estadístico 2025, cap. 13: `http://www.onei.gob.cu/sites/default/files/publicaciones/2026-10/13-transporte-y-seguridad-vial_aec2025.pdf`

---