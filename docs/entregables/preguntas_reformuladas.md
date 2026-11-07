# Las 30 preguntas del mercado de motos: verificacion y reformulacion

Documento de trabajo que acompana a `preguntas.txt` y a `como_responde_el_proyecto.md`.
Responde a dos cosas concretas:

1. **Si el proyecto actual responde o no a las 30 preguntas originales.**
2. **Como reformular las que no responde**, para que todas tengan una respuesta honesta con la evidencia que ya existe, sin inventar datos.

---

## 1. Veredicto: no, el proyecto no responde las 30 preguntas tal como estan escritas

| Nivel | Preguntas | Total |
|---|---|---:|
| Responde con datos | 4, 8, 9, 17, 27 | 5 |
| Responde parcialmente o solo con entrevistas | 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30 | 21 |
| No responde todavia | 5, 11, 20, 22 | 4 |

> Actualizado el 06/11/2026 tras revisar la Gaceta Oficial, el BCC y la ONEI. La 17 pasa a responderse con datos; la 7, 14, 21 y 23 pasan a parciales. El detalle esta en `respuestas_fuentes_oficiales.md`.

**Conclusión:** el trabajo tiene una base solida (6.101 anuncios, 30 entrevistas, informes y graficos), pero **4 preguntas quedaron fuera de alcance** y **21 solo se responden como tendencia, percepcion o dato oficial parcial**. La causa no es falta de trabajo, sino que varias preguntas piden cosas que el diseno actual no recogio:

- series de tiempo para medir crecimiento o variacion anual;
- municipio o geolocalizacion de los anuncios;
- condicion nueva/usada y pais de importacion en el scraping;
- un censo de talleres o de mecanicos;
- la tarifa ad-valorem exacta de la importacion no comercial (la Gaceta no la publica);
- una muestra mas grande de remesas y un modulo de disponibilidad/tiempos de repuestos.

Reformular no es maquillar la respuesta. Es **ajustar la pregunta a lo que la evidencia puede sostener** y decirlo con claridad. Las preguntas reformuladas siguen siendo utiles para el informe y para el cliente; lo que cambia es que ya no prometen una medicion que no existe.

---

## 2. Regla de reformulacion

| Si la pregunta original pide... | La pregunta reformulada pregunta... |
|---|---|
| Crecimiento, evolucion, "ultimo ano" | Composicion actual y evidencia disponible |
| "Cuanto" con precision | Rango, mediana o casos documentados |
| Una causa unica | Que factores aparecen y con que evidencia |
| Una comparacion por zona | Que se sabe de zona y que falta para comparar |
| Un censo (talleres, mecanicos) | Que evidencia cualitativa hay y que no se puede generalizar |
| Un impuesto o norma exactos | Que costo o cambio menciona la fuente y cual falta verificar |

Las preguntas 4, 8, 9, 17 y 27 se mantienen casi igual porque el proyecto ya las responde con datos o con la normativa oficial. Las preguntas 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 28, 29 y 30 se mantienen en su tema, pero se redactan como **evidencia disponible** para no exigir una medicion que no existe.

---

## 3. Las 30 preguntas reformuladas

> Leyenda de fuente: **D** = dataset de anuncios; **E** = entrevistas; **I** = informes/graficos; **O** = fuentes oficiales (Gaceta Oficial, BCC, ONEI); **L** = limite declarado.
> Tipo: **Cuantitativa** = cifra o tabla; **Cualitativa** = casos y percepciones; **Mixta** = dato + entrevista.

### Bloque 1 - Mercado y demanda

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 1 | Como crece la electrica frente a la combustion | **Que composicion tiene hoy la oferta de motos electricas frente a la de combustion en La Habana?** | D, I | Cuantitativa |
| 2 | Que tipo de moto es mas facil de vender | **Que categoria concentra mas anuncios y cuales reciben mas vistas promedio en la oferta publicada?** | D, I | Cuantitativa |
| 3 | Que marcas tienen mas demanda y cuales ganaron terreno | **Que marcas dominan la oferta publicada y como se distribuyen por categoria?** | D, I | Cuantitativa |
| 4 | Que diferencia real hay entre gasolina y electrica | **Que diferencias de precio, autonomia, mantenimiento y papeles aparecen en los datos y en las entrevistas?** | D, E, I | Mixta |
| 5 | Como varia la oferta y el precio por zona | **Que evidencia hay sobre diferencias por zona o municipio, y que falta para compararlas?** | E, L | Cualitativa |
| 6 | Que segmento crece mas (personal, mensajeria, trabajo, alquiler) | **Que usos declaran los compradores entrevistados: trabajo, mensajeria, personal o mixto?** | E | Cualitativa |
| 7 | El mercado se mueve mas por motos nuevas o por reventa | **Que senales de compra nueva y de reventa aparecen, y que evidencia oficial existe sobre la tasacion de usados?** | D, E, O, L | Mixta |

### Bloque 2 - Precios y capacidad de pago

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 8 | Cuanto esta dispuesto a pagar el consumidor | **Que precios se publican y que pagos declaran los entrevistados por tipo de moto?** | D, E, I | Cuantitativa |
| 9 | Que rangos de precio manejan las marcas mas vendidas | **Que rangos de precio se manejan hoy para las marcas con mas anuncios?** | D, I | Cuantitativa |
| 10 | Como afecta el dolar y el tipo de cambio | **En que moneda se cotiza el mercado y que se sabe del efecto del dolar en el precio?** | D, E, L | Mixta |
| 11 | Cuanto influyen las remesas y familiares en el exterior | **Que casos documentados muestran el peso de las remesas o de la ayuda familiar en la compra?** | E, L | Cualitativa |
| 12 | Que pesa mas: precio, autonomia, marca o repuestos | **Que factores de decision aparecen en las entrevistas y con que peso relativo?** | E, L | Cualitativa |
| 13 | Que pasa con el costo cuando hay que cambiar la bateria | **Que se sabe del costo de reemplazo de la bateria en las electricas?** | E, D, L | Mixta |

### Bloque 3 - Importacion, papeles y regulacion

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 14 | Cual es el impuesto o costo real para importar | **Que componentes del costo de importacion estan publicados y cual sigue sin publicarse?** | E, O, L | Mixta |
| 15 | Que paises y canales de importacion se usan | **Que paises y canales de importacion aparecen documentados en las entrevistas y en los anuncios?** | E, D, L | Mixta |
| 16 | Que requisitos pesan mas: licencia, chapa, seguro o registro | **Que requisitos de papeles mencionan los entrevistados y como afectan el uso?** | E, D | Mixta |
| 17 | Como han cambiado las regulaciones recientes | **Que cambios regulatorios recientes afectan la compra, venta y circulacion, y que objetivos declaran?** | O | Cualitativa |
| 18 | Que riesgo percibe el comprador sin papeles o importada informal | **Que riesgos perciben los compradores al adquirir una moto sin papeles o importada informalmente?** | E, L | Cualitativa |

### Bloque 4 - Repuestos y servicio tecnico

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 19 | Que piezas y accesorios se rompen mas | **Que piezas y accesorios generan gasto o falla segun los entrevistados?** | E, L | Cualitativa |
| 20 | Que repuestos son mas dificiles y cuanto demoran | **Que problemas de repuestos mencionan los entrevistados y como los resuelven?** | E, L | Cualitativa |
| 21 | Como son los precios de repuestos respecto al ano pasado | **Que valores de referencia oficiales existen hoy y que falta para comparar con el ano pasado?** | O, L | Cualitativa |
| 22 | La disponibilidad de talleres alcanza para la demanda | **Que evidencia hay sobre la disponibilidad y capacidad de talleres?** | E, L | Cualitativa |
| 23 | Que tan facil es encontrar un mecanico de electricas | **Que obligaciones oficiales de servicio posventa existen y que no se puede medir?** | O, E, L | Cualitativa |

### Bloque 5 - Uso, carga y apagones

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 24 | Cuanto influyen los apagones en comprar una electrica | **Como afectan los apagones al uso y a la carga de las electricas segun los entrevistados?** | E, D, L | Cualitativa |
| 25 | Donde y como carga la gente en edificios o zonas con poco espacio | **Donde y como cargan los entrevistados, y que limites aparecen?** | E, D, L | Cualitativa |
| 26 | La autonomia real coincide con la prometida | **La autonomia real coincide con la prometida segun los entrevistados?** | E, D, L | Cualitativa |
| 27 | Que uso le da el cliente a la moto | **Que uso le dan los compradores a la moto: trabajo, mensajeria, transporte familiar u ocio?** | E | Cualitativa |

### Bloque 6 - Canales, confianza y futuro

| # | Pregunta original (resumen) | Pregunta reformulada | Fuente | Tipo |
|---|---|---|---|---|
| 28 | Que canal domina la compraventa | **Que canales de compraventa aparecen en las fuentes del proyecto y cual domina la evidencia?** | D, E, L | Mixta |
| 29 | Que tan importante es la garantia y la confianza | **Que senales de garantia y confianza aparecen en los anuncios y en las entrevistas?** | D, E, L | Mixta |
| 30 | Como imagina el mercado en 2 o 3 anos | **Que escenarios de futuro plantean las fuentes del proyecto y con que limites?** | E, L | Cualitativa |

---

## 4. Que cambia en las preguntas que antes no se respondian

| # | Antes | Ahora | Por que se puede responder |
|---|---|---|---|
| 5 | "Como varia la oferta y el precio por zona" | "Que evidencia hay por zona y que falta" | El dataset no trae municipio; las entrevistas si mencionan Vedado y Diez de Octubre. Se responde con esos casos y se declara el limite. |
| 7 | "Se mueve mas por nuevas o por reventa" | "Que senales de nueva y reventa aparecen y que evidencia oficial hay" | Hay 323 anuncios con "nueva", 0 con "usada"; la Res. 171/2026 tasa los usados por edad, pero no se puede cuantificar el peso relativo. |
| 11 | "Cuanto influyen las remesas" | "Que casos documentados muestran su peso" | `COMPRADOR_012` declara remesas casi mensuales y ayuda familiar; no hay base para un porcentaje. |
| 14 | "Cual es el impuesto real" | "Que componentes oficiales se conocen y cual falta" | El 5 %/20 % es impuesto especial (Res. 172/2026); hay valores de referencia, servicio de aduana y tarifa del viajero. Falta el arancel ad-valorem exacto. |
| 17 | "Como han cambiado las regulaciones" | "Que cambios regulatorios recientes afectan la compra, venta y circulacion" | La Gaceta 65/2026 documenta la cadena de reemplazo 2024-2026, sus objetivos y las nuevas obligaciones de posventa. |
| 20 | "Que repuestos son mas dificiles y cuanto demoran" | "Que problemas de repuestos mencionan y como los resuelven" | Las entrevistas confirman el problema, pero no identifican piezas ni tiempos de forma consistente. |
| 21 | "Como son los precios de repuestos respecto al ano pasado" | "Que valores oficiales hay y que falta para comparar" | La Res. 340/2026 publica valores de referencia de repuestos, pero no hay serie de 2025 para medir la variacion. |
| 22 | "La disponibilidad de talleres alcanza" | "Que evidencia hay sobre disponibilidad y capacidad" | Hay 4 talleres entrevistados, pero sin censo ni identidad confirmada. |
| 23 | "Que tan facil es encontrar mecanico de electricas" | "Que obligaciones de posventa existen y que no se mide" | La Res. 52/2026 obliga a los comercializadores autorizados a dar posventa, pero no mide el mercado informal. |

---

## 5. Que se gana y que se pierde

**Se gana:**

- las 30 preguntas tienen una respuesta posible con la evidencia actual;
- cada respuesta declara su fuente y su limite;
- el informe deja de prometer mediciones que el diseno no puede dar;
- las preguntas 4, 8, 9, 17 y 27 siguen respondiendose con cifras o con la normativa oficial;
- la 7, 14, 21 y 23 ganan una base oficial parcial sin dejar de ser cualitativas.

**Se pierde:**

- las preguntas 1, 3, 6, 10, 11, 22 y 30 ya no se pueden presentar como "crecimiento", "demanda" o "censo"; se presentan como **composicion, casos o percepciones**;
- la 7, 14, 21 y 23 no alcanzan para afirmar peso relativo, costo total ni variacion anual;
- la muestra de entrevistas sigue siendo pequena y no probabilistica;
- la foto de 17 dias no sustituye una serie temporal.

**Lo que no cambia:** el proyecto sigue sin poder afirmar tasas de crecimiento, participacion de mercado por marca, la tarifa ad-valorem exacta, censo de talleres ni pronosticos cuantitativos. Reformular las preguntas no elimina esos limites; los hace explicitos.

---

## 6. Como usarlo en el informe

- Usar la columna "Pregunta reformulada" como titulo de cada seccion.
- Citar la fuente con la leyenda **D / E / I / O / L**.
- Cuando la respuesta sea cualitativa, escribir "segun los entrevistados" o "en la evidencia disponible", no "el mercado".
- Mantener el anexo `como_responde_el_proyecto.md` como respaldo: ahi estan los numeros y los casos que sostienen cada respuesta.

---

*Documento generado a partir de `preguntas.txt`, `como_responde_el_proyecto.md`, `respuestas_fuentes_oficiales.md`, `reports/metricas/resumen_mercado.json`, `reports/informe_mercado.md` y `docs/entrevistas/*.json`.*
