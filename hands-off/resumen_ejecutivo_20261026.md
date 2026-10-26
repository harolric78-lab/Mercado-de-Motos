# Resumen Ejecutivo — Mercado de Motos en Cuba

> **Corte de datos:** 26 de octubre de 2026 · **Autor:** Harold Ricardo Ponce · **Asignatura:** Introducción a la Ciencia de Datos

---

## 1. Qué se analizó

| Fuente | Ventana | Volumen | Estado |
|---|---|---:|---|
| Revolico (histórico) | 10–22 oct 2026 | 6 249 anuncios únicos (5 686 con precio USD) | Consolidado |
| Revolico (reciente) | 26 oct 2026 | 30 anuncios más recientes | Actualizado |
| VEDCA (catálogo de fábrica) | 26 oct 2026 | 7 vehículos, sin precios | Nuevo |
| Islagrande (tienda online de VEDCA) | 26 oct 2026 | 14 precios válidos (USD) | Nuevo |
| Entrevistas | — | 1 entrevista | En curso |
| Telegram / talleres | — | — | Pendiente (credenciales) |

---

## 2. Cifras clave

- **Composición de la oferta (6 249 anuncios):** eléctricas **82,0 %** (motos eléctricas 37,1 % + bicimotos 27,9 % + bicicletas 13,4 % + patinetes 3,6 %) vs. combustión **18,0 %**.
- **Precios medianos:** combustión **2 220 USD** · motos eléctricas **2 000 USD** · bicimotos **1 550 USD** · patinetes **750 USD** · bicicletas eléctricas **590 USD**.
- **Top por segmento:** ITALY RX Combat (50 anuncios, comb.), TOPMAQ General (181, eléct.), JMD General (174, bicimoto) y JMD General (34, patinete).
- **Corte reciente (30 anuncios):** 8 de combustión y 21 eléctricos; mediana 2 600 USD vs. 1 450 USD; rango 340–2 800 USD.
- **Precios de tienda (Islagrande):** eléctricas VEDCA entre **601 y 2 096 USD**; Hongli HL-125 (125 cc) a **1 474 USD**.
- **Precios atípicos:** sin precios extremadamente altos en el corte reciente; único atípico: un lote de combustión a **1 670 USD** (por debajo del rango).

---

## 3. Hallazgos

1. **El mercado ya es mayoritariamente eléctrico en oferta publicada** (4 de cada 5 anuncios), y la proporción se sostiene en los anuncios más recientes.
2. **Las eléctricas son más baratas pero más dispersas:** mediana 2 000 USD con CV 0,51 vs. CV 0,29 en combustión (2 220 USD).
3. **El arbitraje local es estrecho:** con costo operativo del 10 %, el escenario base (compra P25 → venta mediana) da margen cero o negativo en la mayoría de los modelos.
4. **La rentabilidad aparece comprando barato o importando:** TOPMAQ alcanza **28,1 %** de ROI y Suzuki GN125 **23,4 %** solo en el escenario de compra en P10 → venta en P75.
5. **La fábrica no fija precios públicos:** VEDCA publica catálogo sin precios; el precio de referencia lo dan las tiendas (Islagrande, Supermarket23, Katapulk) y los anuncios de Revolico.
6. **Hipótesis descartadas:** Yadea y Yati no tienen presencia en la muestra (0 y 1 anuncio); la Suzuki GN125 no es la más ofertada (la supera RX Combat), aunque conserva mejor margen.

---

## 4. Recomendación de inversión (síntesis)

| Prioridad | Segmento | Modelo | ROI oportunista | Rol |
|---|---|---|---:|---|
| 1 | Eléctricas | TOPMAQ (TANK/F3) | 28,1 % | Núcleo de cartera |
| 2 | Combustión | Suzuki GN125 | 23,4 % | Nicho de margen |
| 3 | Bicimotos | JMD General | 2,4 % | Flujo de caja |
| — | Combustión | ITALY RX Combat | -2,5 % | Evitar arbitraje puro |
| — | Patinetes | JMD General | -0,7 % | Solo volumen + accesorios |

**Asignación sugerida:** 5 000 USD → 2 TOPMAQ o 2 GN125 · 10 000 USD → 4–5 unidades mixtas · 20 000 USD → lote de importación de 8–10 eléctricas + 3–4 GN125.

---

## 5. Limitaciones

- Precios de **anuncio**, no de transacción (hay margen de negociación no observado).
- Una sola fuente con datos (Revolico); Telegram pendiente de credenciales.
- 51,9 % de los anuncios no especifica marca en el corte histórico.
- Muestra transversal de 13 días: describe la **oferta activa**, no el volumen histórico de ventas.

---

## 6. Próximos pasos

1. Conectar Telegram (API oficial) para activar el componente de fuentes del índice de demanda.
2. Sumar entrevistas y datos de talleres para triangular precios de reparación/reventa.
3. Scraping periódico (Revolico + tiendas) para construir una serie temporal de precios.
4. Actualizar `reports/README.md` con el corte del 26/10 y las nuevas fuentes (VEDCA, Islagrande).

---

**Documentos de referencia**

- Informe ejecutivo completo: [`../reports/README.md`](../reports/README.md)
- Informes por corte: [`../docs/informes/`](../docs/informes/)
- Bitácora: [`../journal/README.md`](../journal/README.md)
