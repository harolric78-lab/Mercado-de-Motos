# Respuestas desde fuentes oficiales

Documento de trabajo complementario a `como_responde_el_proyecto.md` y a `preguntas_reformuladas.md`.
Revisa qué aportan la **Gaceta Oficial**, el **Banco Central de Cuba (BCC)** y la **ONEI** a las 30 preguntas del mercado de motos en La Habana, y actualiza el veredicto de cobertura.

**Fecha de corte:** 06/11/2026.
**Regla:** solo se afirma lo que está escrito en la fuente oficial. Cuando el dato no aparece, se declara como límite; no se completa con estimaciones.

---

## 1. Qué se revisó

| Fuente | Fecha | Identificador | Qué aporta |
|---|---|---|---|
| Gaceta Oficial, Edición Especial 10 | 10/08/2026 | GOC-2026-ES10 | Ley 109/2010, Código de Seguridad Vial, edición anotada 2026: licencia, registro, chapa, revisión técnica, casco y circulación |
| Gaceta Oficial Ordinaria 65 | 04/08/2026 | GOC-2026-O65 | Decreto 163/2026; Res. 171, 172, 173, 174 y 175/2026; Res. 52/2026 |
| Gaceta Oficial Ordinaria 83 | 05/10/2026 | GOC-2026-O83 | Decreto-Ley 132/2026; Res. 197/2026; Res. 340/2026 |
| Gaceta Oficial Ordinaria 128 | 30/12/2024 | GOC-2024-O128 | Decreto 119/2024 y normas de 2024 que el paquete de 2026 reemplaza |
| Decreto-Ley 22/2020 | 10/12/2020 | GOC-2020-EX68 | Marco del arancel de aduanas para importaciones sin carácter comercial |
| BCC, tasas de cambio | 06/11/2026 | `bc.gob.cu/tasas-de-cambio` | Tasa oficial USD/CUP y tasas de compra y venta en ventanilla |
| ONEI, Anuario Estadístico 2025, cap. 13 | 2026 | `aec2025` | Transporte y seguridad vial; no trae parque de motos ni precios |

---

## 2. Hallazgo principal: el 5 % y el 20 % no son el arancel

La importadora (`IMPORTADORA_001`) menciona un **5 %** para eléctricas y un **20 %** para combustión. Esos porcentajes **no son el arancel de importación**: son el **Impuesto Especial a Productos y Servicios** que se aplica sobre el **precio de venta** de los vehículos que comercializan las entidades autorizadas (Res. 172/2026, Anexo Único).

| Base imponible | Tipo |
|---|---:|
| Precio de venta de vehículos de combustión, clase moto y triciclo | **20 %** |
| Precio de venta de vehículos eléctricos, todas las clases | **5 %** |
| Precio de venta de vehículos híbridos, todas las clases | **15 %** |
| Precio de venta de motos y triciclos de combustión ensamblados en Cuba | **10 %** |
| Precio de venta de vehículos eléctricos ensamblados por personas jurídicas autorizadas | **3 %** |

Fuente: Res. 172/2026 (GOC-2026-430-O65), Anexo Único.

Además, la Res. 172/2026 **exonera del Impuesto Aduanero** a las entidades comercializadoras autorizadas que importan vehículos eléctricos para venderlos en USD (apartado Noveno). Es decir, en el canal formal la eléctrica no paga arancel de importación, pero sí el 5 % de impuesto especial sobre la venta. La combustión no tiene esa exención: paga el arancel que corresponda y el 20 % de impuesto especial.

**Consecuencia para el informe:** no se debe decir que “la moto eléctrica paga 5 % de arancel”. Lo correcto es: “la moto eléctrica paga 5 % de impuesto especial sobre la venta; el arancel de importación de la eléctrica está exonerado para los comercializadores autorizados”. El arancel exacto de la combustión no aparece publicado en los textos consultados.

---

## 3. Costo de importación: dos canales distintos

### 3.1 Vía no comercial (persona natural)

| Concepto | Moto eléctrica | Moto de combustión | Fuente |
|---|---:|---:|---|
| Valor de referencia en aduana | 200 USD | 850 USD sin sidecar; 950 USD con sidecar | Res. 340/2026, Anexo II, cap. 8 |
| Servicio de aduana | No se detalla una tarifa específica para motos eléctricas | 8 USD (hasta 250 cc) | Res. 175/2026, Anexo I |
| Impuesto Aduanero | Se paga en CUP si es importación directa de residente permanente | Se paga en USD | Res. 174/2026, apartados Primero y Noveno |
| Frecuencia | Sin límite quinquenal explícito para eléctricas | Una vez cada 5 años | Res. 174/2026, apartado Segundo |
| Impuesto especial 5 %/20 % | No aplica a la importación para uso propio; es un impuesto de venta | No aplica a la importación para uso propio | Res. 172/2026, apartado Primero |

**Límite:** la tarifa ad-valorem exacta del Impuesto Aduanero para la importación no comercial de motos **no está publicada** en la Gaceta consultada. El Decreto-Ley 22/2020 solo establece que el adeudo es ad-valorem y que la base puede ser el valor de referencia; la escala concreta la fija el Ministerio de Finanzas y Precios. Por eso no se puede dar un “costo total” exacto sin ese dato.

### 3.2 Vía comercial (importadora autorizada)

| Concepto | Moto eléctrica | Moto de combustión | Fuente |
|---|---|---|---|
| Arancel de importación | Exento para comercializadores autorizados que venden en USD | El que corresponda (no publicado en los textos consultados) | Res. 172/2026, apartado Noveno |
| Impuesto especial sobre la venta | 5 % | 20 % | Res. 172/2026, Anexo Único |
| Margen comercial | Hasta 3 % en servicios de importación para clientes autorizados | Hasta 3 % en servicios de importación para clientes autorizados | Res. 172/2026, apartado Tercero |
| Formación del precio | Costos totales + arancel + margen + impuesto especial | Costos totales + arancel + margen + impuesto especial | Res. 172/2026, apartado Segundo |

**Ejemplo ilustrativo, no costo oficial:** si una eléctrica se vende a 2.050 USD, el impuesto especial es 102,50 USD; si una de combustión se vende a 2.250 USD, el impuesto especial es 450 USD. Son cálculos sobre el precio de venta, no sobre el valor de aduana.

### 3.3 Vía comercial opcional del viajero

La Res. 197/2026 (GOC-2026-600-O83) establece una tarifa progresiva para la persona natural que, siendo viajera, opte por formalizar una **importación con carácter comercial** de mercancías que no clasifican para la vía no comercial:

| Valor de importación | Tarifa |
|---|---:|
| Hasta 2.000 USD | 15 % |
| Exceso de 2.000 a 4.000 USD | 20 % |
| Exceso de 4.000 a 6.000 USD | 25 % |
| Exceso de 6.000 USD | 30 % |

Esta tarifa **no es** la del régimen no comercial ordinario y **no es** el 20 % de la importadora. Es una opción para regularizar importaciones que exceden los límites. No debe usarse para explicar el precio de una moto comprada en el canal formal.

---

## 4. Valores oficiales de referencia

### 4.1 Vehículos (Res. 340/2026, Anexo II, cap. 8)

| Artículo | Valor de referencia |
|---|---:|
| Ciclomotor o motocicleta eléctrica de hasta dos plazas, con o sin sidecar | 200 USD |
| Ciclomotor o motocicleta de combustión o híbrida, sin sidecar | 850 USD |
| Ciclomotor o motocicleta de combustión o híbrida, con sidecar | 950 USD |
| Triciclo eléctrico o híbrido, más de dos plazas | 550 USD |
| Triciclo de combustión de hasta 250 cc, más de dos plazas | 950 USD |
| Sidecar para motocicleta | 100 USD |
| Remolque ligero de hasta 750 kg | 300 USD |
| Motor eléctrico con accesorios para remotorizar | 950 USD |

Estos valores son **bases de aduana**, no precios de mercado. No sirven para responder cuánto cuesta una moto en La Habana; sirven para calcular el adeudo y para comparar con los precios publicados.

### 4.2 Vehículos usados: valores mínimos para impuestos (Res. 171/2026)

| Clase | Hasta 5 años | Más de 5 hasta 15 | Más de 15 |
|---|---:|---:|---:|
| Ciclomotores | 132.500 CUP | 66.250 CUP | 33.125 CUP |
| Motocicletas y triciclos | 265.000 CUP | 132.500 CUP | 66.250 CUP |

Fuente: Res. 171/2026 (GOC-2026-429-O65). Son valores mínimos para la compraventa y donación, a efectos de los impuestos sobre Ingresos Personales y Transmisión de Bienes y Herencias.

**Lectura:** el sistema tributario reconoce y tasa la **reventa** de motos por edad. Eso confirma que el mercado de usados existe y no es marginal, pero **no dice qué proporción del mercado es nueva y qué proporción es usada**.

### 4.3 Repuestos: valores de referencia (Res. 340/2026, Anexo II, cap. 8)

| Repuesto | Valor de referencia |
|---|---:|
| Baterías o acumuladores de litio | 60 USD |
| Otras baterías y acumuladores | 35 USD |
| Kit o set de baterías de gel | 100 USD |
| Neumáticos para motos o ciclomotores | 35 USD |
| Cámaras para neumáticos de motos o ciclomotores | 5 USD |
| Llantas para motos o ciclomotores | 35 USD |
| Carburador | 40 USD |
| Delco (distribuidor) | 30 USD |
| Guardafangos | 40 USD |
| Parabrisas | 150 USD |
| Amortiguadores | 15 USD |
| Bobina de encendido | 5 USD |
| Cajas de velocidad | 120 USD |
| Asiento para moto o ciclomotor | 50 USD |
| Tubo de escape de autos y motos | 50 USD |
| Rodamientos | 20 USD |
| Válvulas de motor | 5 USD |

Son **valores de aduana**, no precios de venta al público. No hay en la Gaceta consultada una serie del año anterior que permita decir si los repuestos subieron o bajaron; solo existe la foto oficial de octubre de 2026.

---

## 5. Tipo de cambio y equivalencias

Tasa oficial del BCC al 06/11/2026: **1 USD = 793,00 CUP**.
En ventanilla: compra **777,14 CUP** y venta **808,86 CUP** por USD.

| Categoría | Mediana del dataset | Equivalente en CUP a 793 |
|---|---:|---:|
| Motos de combustión | 2.250 USD | 1.784.250 CUP |
| Motos eléctricas | 2.050 USD | 1.625.650 CUP |
| Bicicletas eléctricas | 1.150 USD | 911.950 CUP |
| Patinetes | 750 USD | 594.750 CUP |

**Lectura:** el mercado se cotiza en USD (99,4 % de los anuncios). La tasa oficial no cambia el precio en dólares; cambia su equivalente en CUP y, por tanto, la capacidad de pago de quien tiene ingresos en CUP. No se midió el pass-through del tipo de cambio al precio.

---

## 6. Cambio regulatorio 2024 → 2026

El paquete de 2026 reemplazó el paquete de diciembre de 2024. La propia Gaceta 65 explica el objetivo: actualizar las normas al contexto económico y contribuir a la transformación de la matriz energética.

| Norma de 2024 | Norma de 2026 | Qué regula |
|---|---|---|
| Decreto 119/2024 | **Decreto 163/2026** | Transmisión de la propiedad, comercialización e importación de vehículos |
| Res. 226/2024 (MINCEX) | **Res. 104/2026** | Autorizaciones de importación de personas jurídicas |
| Res. 60/2024 (MINCIN) | **Res. 17/2026** | Comercialización por entidades autorizadas |
| Res. 397/2024 (MFP) | **Res. 171/2026** | Valores mínimos para impuestos de compraventa y donación |
| Res. 398/2024 (MFP) | **Res. 172/2026** | Formación de precios, impuesto especial y trato arancelario |
| Res. 399/2024 (MFP) | **Res. 173/2026** | Precios en CUP de vehículos usados y partes recuperadas |
| Res. 400/2024 (MFP) | **Res. 174/2026** | Importación excepcional por encima del valor |
| Res. 401/2024 (MFP) | **Res. 175/2026** | Tarifas de servicios de aduana |
| Res. 180/2024 (MITRANS) | **Res. 52/2026** | Regulaciones complementarias de comercialización, importación, ensamblaje y desarme |
| Res. 364/2024 (Aduana) | **Res. 340/2026** | Reglas y valores de referencia de importaciones no comerciales |
| Decreto-Ley 101/2024 | **Decreto-Ley 132/2026** | Modifica el Decreto-Ley 22/2020 |

**Qué cambia en la práctica, según el texto oficial:**
- se actualiza el régimen de transmisión, comercialización e importación (Decreto 163/2026);
- se refuerza la participación de los actores económicos no estatales (Res. 52/2026);
- se exige a los comercializadores autorizados servicio posventa, piezas, personal calificado, equipamiento especializado, asistencia en carretera 24 horas y estaciones de carga para vehículos eléctricos (Res. 52/2026, Art. 3);
- se exonera del Impuesto Aduanero la importación de vehículos eléctricos por comercializadores autorizados (Res. 172/2026);
- se actualizan los valores de referencia y las reglas de importación no comercial (Res. 340/2026).

**Límite:** se comparan las normas y sus objetivos, no los efectos medidos. No hay una evaluación oficial del impacto de estos cambios en precios, ventas o circulación.

---

## 7. Requisitos legales para comprar y circular

La Ley 109/2010, en su edición anotada 2026, establece:

- **Licencia de conducción obligatoria** para conducir vehículos de motor (Art. 261). Categoría **A** para motocicletas y **A1** para ciclomotores (Art. 264).
- **Registro de Vehículos** a cargo del Ministerio del Interior: inscripción, control, inspección técnica y documental, licencia o permiso de circulación y chapas (Arts. 215-216).
- La inscripción autoriza la **licencia de circulación** y la entrega de **chapas** (Art. 221).
- Las motocicletas llevan **una sola chapa en la parte posterior**, expedida por el Registro (Art. 197). Se prohíbe cualquier chapa distinta a la otorgada por el Registro (Art. 198).
- **Revisión técnica** obligatoria y certificado actualizado para circular (Arts. 211-213).
- Obligación de comunicar al Registro, en **30 días**, transmisiones, cambios de motor o combustible, cambios de carrocería o cuadro, pérdida de chapas, conversiones, altas, bajas y cambios de domicilio (Art. 217).
- **Casco protector** para conductor y pasajeros, correctamente abrochado; transporte de pasajeros en dispositivos adecuados; carga que no sobresalga más de 50 cm (Art. 72).

**Sobre el seguro:** el Código de Seguridad Vial consultado **no establece el seguro como requisito obligatorio** para circular. Si existe una obligación de seguro, proviene de otra norma no revisada aquí. Esto es importante porque la pregunta 16 lo incluye como uno de los cuatro requisitos.

---

## 8. Qué preguntas cambian

| # | Antes | Ahora | Qué aporta la fuente oficial | Límite |
|---|---|---|---|---|
| 7 | 🔴 | 🟡 | Res. 171/2026 y Res. 172/2026 tasan la compraventa de motos usadas por edad; la reventa es un mercado reconocido | No dice qué proporción del mercado es nueva vs. usada |
| 10 | 🟡 | 🟡 | Tasa oficial BCC 793 CUP/USD; compra 777,14 y venta 808,86 | No mide el efecto causal del dólar en el precio |
| 14 | 🔴 | 🟡 | Res. 340/2026 (valores), Res. 175/2026 (servicios), Res. 172/2026 (5 %/20 % y exención de arancel a eléctricos), Res. 197/2026 (tarifa comercial progresiva) | No se publica la tarifa ad-valorem exacta de la importación no comercial de combustión |
| 16 | 🟡 | 🟡 | Ley 109/2010: licencia A/A1, registro, chapa trasera única, revisión técnica; el seguro no aparece como obligatorio | No mide cuál requisito “pesa más” para el comprador |
| 17 | 🔴 | 🟢 | Cadena completa de reemplazo 2024 → 2026 y objetivos declarados | Compara normas y objetivos, no efectos medidos |
| 21 | 🔴 | 🟡 | Res. 340/2026 trae valores de referencia actuales para baterías, neumáticos, carburador, amortiguadores, etc. | Son valores de aduana, no precios de venta; no hay serie del año anterior |
| 23 | 🔴 | 🟡 | Res. 52/2026 obliga a los comercializadores autorizados a tener personal calificado y equipamiento especializado, incluida la atención a eléctricos | No mide la facilidad real de encontrar mecánico, sobre todo en el canal informal |

**Las que se refuerzan sin cambiar de veredicto:** 10 y 16.
**Las que cambian de veredicto:** 7, 14, 17, 21 y 23 (cinco).

---

## 9. Veredicto final de las 30 preguntas

**Leyenda:** 🟢 responde con datos; 🟡 responde parcialmente o solo con entrevistas; 🔴 no responde todavía.

| # | Pregunta (resumen) | Antes | Ahora | Fuente o límite principal |
|---|---|---|---|---|
| 1 | Crecimiento eléctrica vs. combustión | 🟡 | 🟡 | Dataset: composición, no serie temporal |
| 2 | Tipo de moto más fácil de vender | 🟡 | 🟡 | Anuncios y vistas; no ventas efectivas |
| 3 | Marcas con más demanda y que ganaron terreno | 🟡 | 🟡 | 47,7 % sin marca; no hay año anterior |
| 4 | Diferencia real gasolina vs. eléctrica | 🟢 | 🟢 | Dataset, entrevistas y requisitos legales |
| 5 | Oferta y precios por zona | 🔴 | 🔴 | El dataset no trae municipio; ONEI no da oferta por zona |
| 6 | Segmento que crece más | 🟡 | 🟡 | Entrevistas; no mide crecimiento |
| 7 | Mercado nuevo vs. reventa | 🔴 | 🟡 | Res. 171/2026 tasa usados; no hay proporción nueva/usada |
| 8 | Disposición a pagar | 🟢 | 🟢 | Medianas del dataset |
| 9 | Rangos de precio por marca | 🟢 | 🟢 | Medianas por marca |
| 10 | Efecto del dólar y el tipo de cambio | 🟡 | 🟡 | BCC 793; no hay medición de pass-through |
| 11 | Influencia de remesas | 🔴 | 🔴 | Sin vínculo oficial remesas→motos; 1/25 entrevistas |
| 12 | Qué pesa más al elegir | 🟡 | 🟡 | Entrevistas; sin ranking uniforme |
| 13 | Costo de cambiar la batería | 🟡 | 🟡 | Entrevista 800 USD; Res. 340/2026: batería litio 60 USD (valor de aduana) |
| 14 | Impuesto o costo real de importar | 🔴 | 🟡 | Valores y servicios oficiales; falta la tarifa ad-valorem exacta |
| 15 | Países y canales de importación | 🟡 | 🟡 | Entrevistas (Panamá); los anuncios no declaran país |
| 16 | Requisitos: licencia, chapa, seguro, registro | 🟡 | 🟡 | Ley 109/2010; el seguro no aparece como obligatorio |
| 17 | Cambios regulatorios recientes | 🔴 | 🟢 | Paquete 2024 → 2026 documentado |
| 18 | Riesgo de comprar sin papeles | 🟡 | 🟡 | Riesgo legal en Arts. 197-198 y 215-217; percepción solo en entrevistas |
| 19 | Piezas que más se rompen | 🟡 | 🟡 | Entrevistas; no hay estadística de fallas |
| 20 | Repuestos más difíciles y demoras | 🔴 | 🔴 | Sin datos oficiales de disponibilidad o demora |
| 21 | Precios de repuestos vs. año pasado | 🔴 | 🟡 | Valores actuales de Res. 340/2026; no hay serie 2025 |
| 22 | Talleres y mecánicos vs. demanda | 🔴 | 🔴 | Sin censo; Res. 52/2026 solo obliga al canal autorizado |
| 23 | Facilidad de encontrar mecánico de eléctricas | 🔴 | 🟡 | Res. 52/2026 exige personal calificado y equipamiento; no mide facilidad real |
| 24 | Influencia de los apagones | 🟡 | 🟡 | Entrevistas; 1 anuncio menciona apagón |
| 25 | Dónde y cómo carga la gente | 🟡 | 🟡 | Entrevistas; sin datos sistemáticos |
| 26 | Autonomía real vs. prometida | 🟡 | 🟡 | Entrevistas divergentes; anuncios declaran, no miden |
| 27 | Uso que le da el cliente | 🟢 | 🟢 | Entrevistas |
| 28 | Canal que domina la compraventa | 🟡 | 🟡 | Dataset solo Revolico; otros canales en entrevistas |
| 29 | Garantía y confianza | 🟡 | 🟡 | 69 anuncios con “garantía”; sin escala |
| 30 | Mercado en 2 o 3 años | 🟡 | 🟡 | Escenarios cualitativos; sin modelo de pronóstico |

### Resumen

| Nivel | Preguntas | Total |
|---|---|---:|
| 🟢 Responde con datos | 4, 8, 9, 17, 27 | **5** |
| 🟡 Responde parcialmente o solo con entrevistas | 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 28, 29, 30 | **21** |
| 🔴 No responde todavía | 5, 11, 20, 22 | **4** |

**Conclusión:** el proyecto **no responde las 30 preguntas solo con fuentes oficiales**. Las fuentes oficiales permiten responder **5** con datos, **21** de forma parcial y dejan **4** fuera de alcance. La mejora respecto al corte anterior (4/17/9) es real: se cierran la 17 y se abren parcialmente la 7, 14, 21 y 23. Pero las cuatro rojas siguen necesitando trabajo de campo o datos que no están publicados.

---

## 10. Las 4 que siguen sin respuesta oficial

| # | Qué falta | Cómo cerrarla |
|---|---|---|
| 5 | Oferta y precios por municipio | Extraer municipio o geolocalizar los anuncios; cruzar con entrevistas por zona |
| 11 | Peso de las remesas en la compra | Añadir pregunta directa y ampliar la muestra; no hay vínculo oficial remesas→motos |
| 20 | Repuestos más difíciles y tiempos de demora | Módulo de repuestos en entrevistas y seguimiento de precios/tiempos en talleres |
| 22 | Censo de talleres y capacidad vs. demanda | Censo o muestreo de talleres; la norma solo cubre a los concesionarios autorizados |

**Brecha transversal:** la tarifa ad-valorem exacta del Impuesto Aduanero para la importación no comercial de motos de combustión. No está en la Gaceta consultada. Para cerrarla hay que solicitar la Resolución del MFP que fija la escala o consultar directamente a la Aduana General.

---

## 11. Fuentes y enlaces

- Ley 109/2010, Código de Seguridad Vial, edición anotada 2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-es10.pdf` (GOC-2026-ES10, 10/08/2026).
- Gaceta Oficial Ordinaria 65/2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-o65_0.pdf` (GOC-2026-O65, 04/08/2026).
- Gaceta Oficial Ordinaria 83/2026: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2026-o83.pdf` (GOC-2026-O83, 05/10/2026).
- Gaceta Oficial Ordinaria 128/2024: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2024-o128.pdf` (GOC-2024-O128, 30/12/2024).
- Decreto-Ley 22/2020: `https://www.gacetaoficial.gob.cu/sites/default/files/goc-2020-ex68.pdf` (GOC-2020-EX68, 10/12/2020).
- BCC, tasas de cambio: `https://www.bc.gob.cu/tasas-de-cambio` (consultado 06/11/2026).
- ONEI, Anuario Estadístico 2025, cap. 13: `http://www.onei.gob.cu/sites/default/files/publicaciones/2026-10/13-transporte-y-seguridad-vial_aec2025.pdf`.

**Nota de vigencia:** la Res. 340/2026 derogó la Res. 175/2022, la Res. 170/2024 y la Res. 312/2026. Los valores de referencia citados son los vigentes al 05/10/2026. La Res. 172/2026 derogó la Res. 398/2024; la Res. 171/2026 derogó la Res. 397/2024; la Res. 52/2026 derogó la Res. 180/2024. Verificar cambios posteriores antes de publicar.

---

*Documento elaborado a partir de la Gaceta Oficial, el BCC y la ONEI. No sustituye a `como_responde_el_proyecto.md`; lo actualiza en los puntos donde la fuente oficial cambia la lectura.*
