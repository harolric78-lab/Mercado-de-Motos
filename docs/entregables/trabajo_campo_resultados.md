# Trabajo de Campo — Resultados (solo datos disponibles)

**Fecha:** 06/11/2026  
**Alcance:** Análisis exhaustivo de los 6.159 anuncios del dataset y las 30 entrevistas existentes.  
**Restricción:** No se puede realizar trabajo de campo presencial (llamadas, visitas, encuestas nuevas) desde este entorno. Todo el análisis se basa en datos existentes.

---

## Q5. Oferta y precios por municipio de La Habana

### Qué se hizo
Se escaneó el texto de título y descripción de **todos los 6.159 anuncios** buscando menciones explícitas de municipios de La Habana, excluyendo falsos positivos (ej. "papeles en regla" no cuenta como municipio Regla). Se combinó con las 90 referencias Apollo ya resueltas.

### Resultado

| Fuente | Anuncios con municipio | % del total |
|---|---|---|
| Referencias Apollo (Res. 340/2026) | 90 | 1.46% |
| Extracción de texto (título/descripción) | 15 nuevos | 0.24% |
| **Total** | **105** | **1.70%** |
| **Sin municipio** | **6.054** | **98.30%** |

### Municipios identificados (105 anuncios)

| Municipio | Anuncios | Fuente |
|---|---|---|
| Plaza de la Revolucion | 34 + 1 = 35 | Apollo + texto |
| Centro Habana | 18 + 1 = 19 | Apollo + texto |
| Playa | 16 + 0 = 16 | Apollo |
| Diez de Octubre | 6 + 3 = 9 | Apollo + texto |
| Marianao | 6 + 1 = 7 | Apollo + texto |
| La Lisa | 4 + 6 = 10 | Apollo + texto |
| Arroyo Naranjo | 2 + 0 = 2 | Apollo |
| Cerro | 1 + 0 = 1 | Apollo |
| Habana del Este | 1 + 0 = 1 | Apollo |
| Boyeros | 1 + 1 = 2 | Apollo + texto |
| Cotorro | 1 + 0 = 1 | Apollo |
| Regla | 0 + 1 = 1 | Texto (1 genuino, 28 fueron "papeles en regla") |
| Guanabacoa | 0 + 0 = 0 | — |
| San Miguel del Padron | 0 + 1 = 1 | Texto |

### Precio mediano USD por municipio (solo anuncios con precio válido)

| Municipio | n | Precio mediano USD |
|---|---|---|
| Plaza | ~35 | ~1.555 |
| Centro Habana | ~19 | ~1.670 |
| Playa | 16 | ~1.800 |
| Diez de Octubre | ~9 | ~720 - 1.107 |
| Marianao | ~7 | ~1.025 - 1.147 |
| La Lisa | ~10 | ~1.350 - 1.500 |
| Cerro | 1 | 2.600 |
| Habana del Este | 1 | 2.100 |
| Arroyo Naranjo | 2 | 260 |
| Boyeros | 2 | 1.500 |
| Cotorro | 1 | 960 |
| Regla | 1 | (sin precio válido) |
| San Miguel del Padron | 1 | (sin precio válido) |
| Guanabacoa | 0 | — |

### Conclusión Q5
**No se puede responder.** Solo 1.70% de los anuncios tiene municipio identificable. La cobertura es demasiado insuficiente para afirmar cómo varía la oferta y los precios por zona de La Habana. Se necesitaría extraer municipio de todos los anuncios (requiere cambio en el scraping) o geolocalizar direcciones.

---

## Q11. Influencia de remesas

### Qué se hizo
Se revisaron las 25 entrevistas de compradores, 4 de talleres y 1 de importadora buscando menciones a remesas, familiares en el exterior o financiamiento desde fuera de Cuba.

### Resultado

| Entrevistado | ¿Menciona remesas? | Detalle |
|---|---|---|
| COMPRADOR_012 | ✅ Sí | "Recibe remesas casi todos los meses"; ingreso ~4.200 CUP; compró moto nueva por importadora de Panamá |
| Otros 24 entrevistados | ❌ No | Ninguna otra mención a remesas o familiares en el exterior como fuente de financiamiento |

### Datos oficiales
- **BCC:** No publica vínculo remesas→compra de vehículos.
- **ONEI:** Anuario Estadístico 2025, cap. 13 no cruza remesas con motos.
- **Gaceta Oficial:** No hay norma que relacione remesas con importación o compra de motos.

### Conclusión Q11
**No se puede responder.** Solo 1 de 25 entrevistados (4%) menciona remesas, y no hay dato oficial que vincule remesas con la compra de motos. Requeriría añadir pregunta directa al cuestionario y ampliar la muestra, o solicitar datos al BCC.

---

## Q20. Repuestos más difíciles y demoras

### Qué se hizo
Se revisaron las 30 entrevistas buscando menciones consistentes a piezas específicas difíciles de conseguir y tiempos de espera.

### Resultado

| Pieza mencionada | Quién lo menciona | Contexto |
|---|---|---|
| Batería | COMPRADOR_006, 009, 017, 020, 025 | Costo principal, dura 2-5 años, reemplazo caro (800-900 USD) |
| Frenos | COMPRADOR_006, 014 | Cambio de freno reportado |
| Plásticos | COMPRADOR_025 | "Más en plásticos y estética que en problemas técnicos" |
| Neumáticos | COMPRADOR_018 | Problemas con neumático en dos años |
| Aceite | COMPRADOR_018 | Problemas con aceite |
| Piezas generales | COMPRADOR_018 | "Problemas con piezas" |
| Pieza no especificada | TALLER_001, TALLER_004 | Se menciona una pieza/avería pero no se identifica cuál |

### Tiempos de demora
**No hay ningún dato de tiempo de demora** en ninguna entrevista. Ningún entrevistado dice "tardé X días en conseguir la pieza X".

### Conclusión Q20
**No se puede responder.** No hay datos consistentes sobre qué repuestos son más difíciles de conseguir ni cuánto demoran. Las entrevistas confirman que conseguir repuestos es un problema general, pero no identifican piezas específicas ni tiempos.

---

## Q22. Talleres y mecánicos vs. demanda

### Qué se hizo
Se revisaron las 4 entrevistas de talleres y se buscó cualquier dato de censo, capacidad o volumen de trabajo.

### Resultado

| Entrevistado | ¿Es taller confirmado? | Datos de capacidad/demanda |
|---|---|---|
| TALLER_001 | ❌ No confirmado | "La moto se usa principalmente para transporte de trabajo." Menciona una pieza pero no cuál ni cuánto cuesta. |
| TALLER_002 | ❌ No confirmado | "La moto se usa para el trabajo en La Habana." No da datos de capacidad. |
| TALLER_003 | ❌ No confirmado | "La usa para el trabajo." Canal de compra no inteligible. |
| TALLER_004 | ❌ No confirmado | "La usa para transporte de trabajo." Menciona carga, avería y apagones sin datos claros. |

### Datos oficiales
- **Res. 52/2026:** Obliga a comercializadores autorizados a tener servicio posventa, piezas, personal calificado, equipamiento especializado, asistencia 24h y estaciones de carga. **Pero solo para el canal autorizado**, no para el resto de talleres.
- No hay censo de talleres ni de mecánicos en la Gaceta Oficial.

### Conclusión Q22
**No se puede responder.** Solo 4 "talleres" entrevistados, ninguno con identidad confirmada como taller. No hay censo, no hay capacidad medida, no hay comparación con la demanda.

---

## Resumen del trabajo de campo

| Pregunta | ¿Se respondió? | Cobertura lograda | Qué falta definitivamente |
|---|---|---|---|
| Q5 | ❌ No | 1.70% (105/6.159) | Municipio en el 98.3% restante de anuncios |
| Q11 | ❌ No | 1/25 entrevistados | Pregunta directa de remesas + muestra más grande |
| Q20 | ❌ No | 0% (ningún dato consistente) | Módulo de repuestos en entrevistas a talleres |
| Q22 | ❌ No | 0% (ningún censo) | Censo o muestreo de talleres por municipio |

**Limitación fundamental:** Este entorno no puede realizar trabajo de campo presencial (llamadas telefónicas, visitas a talleres, encuestas presenciales, geolocalización de direcciones físicas). Todo el análisis posible con datos existentes ya se ha realizado.

### Qué se necesitaría para cerrar estas 4 preguntas

1. **Q5:** Modificar el scraping para capturar municipio de cada anuncio (Revolico no lo expone de forma confiable en el HTML actual) o geolocalizar direcciones.
2. **Q11:** Añadir pregunta directa ("¿recibe remesas? ¿cuánto? ¿se usó para comprar la moto?") al cuestionario de entrevistas y ampliar la muestra a 100+ compradores.
3. **Q20:** Crear un módulo específico de repuestos en las entrevistas (pieza, tiempo de espera, precio pagado) y aplicarlo a compradores y talleres.
4. **Q22:** Realizar censo o muestreo de talleres de motos en La Habana, geolocalizados, con conteo de mecánicos y capacidad estimada.

---

**Estado final:** 26 de 30 preguntas tienen respuesta (parcial o completa). Las 4 restantes requieren trabajo de campo que no puede realizarse desde este entorno.