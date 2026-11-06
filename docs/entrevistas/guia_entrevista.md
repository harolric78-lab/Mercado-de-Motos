# Guía de entrevista semiestructurada

Instrumento de recolección de la evidencia cualitativa del proyecto **Investigación del Mercado de Motos en Cuba**.

Las entrevistas son una **fuente primaria** del estudio, con el mismo rango que los anuncios de Revolico: aportan información sobre preferencias, gastos, repuestos, precios percibidos y prácticas del mercado que la oferta publicada no permite observar.

## Antes de empezar

- **Duración:** 10–15 minutos.
- **Registro:** audio (si la persona lo autoriza) y notas de campo.
- **Regla de oro:** se anota lo que la persona dice. Si no sabe o no responde, se deja `null`. No se completa por inferencia ni se corrige el habla.
- **Anonimato:** no se publican nombres, teléfonos ni direcciones. El registro usa identificadores (`COMPRADOR_001`, `TALLER_001`, `IMPORTADORA_001`).
- **Herramienta:** el cuestionario legible por máquina está en [`cuestionario.json`](cuestionario.json) y la captura asistida en `src/cualitativo/nueva_entrevista.py`.

## Consentimiento (leer textual)

> Estoy haciendo un estudio sobre el mercado de motos en La Habana para la asignatura Introducción a la Ciencia de los Datos. Sus respuestas se usan solo para el análisis, sin publicar su nombre ni sus datos de contacto. ¿Está de acuerdo en participar y en que grabe la conversación?

Registrar `consentimiento: true` solo si la respuesta es afirmativa. Si no autoriza el audio, se puede continuar con notas y `audio: null`.

## Bloque 1 — Perfil

1. ¿Cuántos años tienes?
2. ¿Sexo?
3. ¿En qué provincia y municipio vives?
4. ¿A qué te dedicas?
5. ¿Recibes remesas? ¿Con qué frecuencia?
6. ¿Tienes familiares en el exterior?
7. ¿En qué rango está tu ingreso mensual?

## Bloque 2 — Compra

8. ¿Qué tipo de vehículo tienes o buscabas: combustión, eléctrica, bicicleta eléctrica o patinete?
9. ¿Qué marca y modelo buscabas?
10. ¿Cuál era tu presupuesto inicial y en qué moneda?
11. ¿Dónde la buscaste o la compraste: Revolico, importadora, agencia, conocido, redes sociales?
12. ¿Qué fue lo más importante al elegir? Ordena del 1 al 5: precio, marca, autonomía, repuestos, estética, papeles.
13. ¿Cuánto pagaste finalmente? ¿En qué año?
14. ¿La compraste nueva o usada? ¿Te la entregaron en el domicilio?
15. Si la compraste por importadora, ¿de qué país vino?

## Bloque 3 — Uso y gastos

16. ¿Para qué usas la moto: personal, trabajo o ambas?
17. ¿Cuántos kilómetros haces al día?
18. ¿Es tu único medio de transporte?
19. ¿Cuánto gastas al mes en combustible o electricidad?
20. ¿Cuánto gastas en mantenimiento y repuestos, y con qué frecuencia?
21. ¿Cuánto gastas en seguridad: candados, alarmas?
22. ¿Cuántos kilómetros tiene actualmente el vehículo?

## Bloque 4 — Repuestos y servicio

23. ¿Has tenido problemas para conseguir repuestos?
24. ¿Cuánto tardas en conseguir uno?
25. ¿Qué repuestos son los más difíciles de encontrar?
26. ¿Cómo son los precios de los repuestos respecto al año pasado?

## Bloque 5 — Precios y mercado

27. ¿Los precios de las motos han subido o bajado en el último año? ¿Cuánto, aproximadamente?
28. ¿Qué crees que influye más en el precio: el dólar, la escasez, las regulaciones o la demanda?
29. ¿Crees que el mercado es mayormente legal o informal?
30. ¿Has visto cambios después de alguna regulación reciente?
31. ¿Consideraste comprar una eléctrica? ¿La prefieres? ¿Por qué?
32. ¿Qué autonomía real tienen las eléctricas que conoces?
33. **Solo talleres/importadoras:** ¿qué modelo es el que más se vende y en qué rango de precio?
34. **Solo talleres/importadoras:** ¿qué motos eléctricas tienen más demanda?

## Bloque 6 — Satisfacción

35. ¿Qué es lo que más te gusta de tu vehículo?
36. ¿Qué es lo que menos te gusta?
37. ¿Lo recomendarías?

## Cierre

38. ¿Algo que quieras añadir sobre el mercado, los precios o los repuestos?

## Registro posterior

1. Normalizar en `docs/entrevistas/<tipo>.json` con el esquema [`esquema.json`](esquema.json).
2. Guardar la transcripción en `data/raw/entrevistas/<ID>.md` y el audio en `data/raw/audios/`.
3. Anotar en `preguntas_pendientes` todo lo que quedó sin responder.
4. Añadir la fecha y las fuentes al `journal.md` (raíz del proyecto, fuera del repositorio).
