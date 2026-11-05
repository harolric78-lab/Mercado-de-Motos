# -*- coding: utf-8 -*-
import json, os, re

BASE = r"C:\Users\LA RUEDA\Desktop\Proyecto de ICD Motos en cuba (2)\Mercado-de-Motos"
ENT = os.path.join(BASE, "docs", "entrevistas")
RAW = os.path.join(BASE, "data", "raw", "entrevistas")


def leer_md(eid):
    p = os.path.join(RAW, eid + ".md")
    with open(p, encoding="utf-8") as f:
        content = f.read()
    paras = [x.strip() for x in content.split("\n\n") if x.strip()]
    texto = paras[-1]
    msha = re.search(r"\*\*SHA256:\*\* `([0-9a-fA-F]{64})`", content)
    mdur = re.search(r"\*\*Duraci[oó]n:\*\* ([\d.]+) s", content)
    marc = re.search(r"^## (.+)$", content, re.M)
    return {
        "texto": texto,
        "sha": msha.group(1) if msha else "",
        "duracion": float(mdur.group(1)) if mdur else 0.0,
        "archivo": marc.group(1).strip() if marc else "",
    }


def leer_md_partes(eid):
    p = os.path.join(RAW, eid + ".md")
    with open(p, encoding="utf-8") as f:
        content = f.read()
    patron = re.compile(
        r"## (.+?)\n\n- \*\*SHA256:\*\* `([0-9a-fA-F]{64})`\n"
        r"- \*\*Duraci[oó]n:\*\* ([\d.]+) s\n.*?\n.*?\n\n(.*?)(?=\n## |\Z)",
        re.S,
    )
    partes = []
    for m in patron.finditer(content):
        partes.append({
            "archivo": m.group(1).strip(),
            "sha256": m.group(2),
            "duracion_s": float(m.group(3)),
            "texto": m.group(4).strip(),
        })
    return partes


def base(eid, fecha, ubicacion, temas, *, perfil=None, compra=None, uso=None,
         repuestos=None, opiniones=None, satisfaccion=None, respuestas=None,
         pendientes=None, obs="", duracion=0.0, sha="", archivo=""):
    perfil_d = {"edad": None, "sexo": None, "municipio": None, "ocupacion": None,
                "recibe_remesas": None, "familiar_exterior": None,
                "rango_ingreso_mensual": None, "remesas_frecuencia": None,
                "provincia": None}
    compra_d = {"tipo_moto": None, "marca_buscada": None, "modelo_buscado": None,
                "presupuesto_inicial": None, "moneda": None, "canal_busqueda": None,
                "factores_decision": None, "precio_final": None, "anio_compra": None,
                "importadora_origen": None, "entrega_domicilio": None,
                "comprada_nueva": None}
    uso_d = {"uso_principal": None, "km_diarios": None, "unico_medio_transporte": None,
             "gasto_combustible": None, "gasto_mantenimiento": None,
             "gasto_mantenimiento_periodo": None, "gasto_seguridad": None,
             "tiene_alarma_candado": None, "problemas_repuestos": None,
             "kilometraje_actual": None, "lugar_trabajo": None,
             "porcentaje_uso_trabajo": None}
    rep_d = {"disponibilidad": None, "tiempo_conseguir": None,
             "dificiles_conseguir": [], "precios_repuestos": None}
    op_d = {"comportamiento_precios": None, "variacion_precios_ultimo_anio": None,
            "influencia_precio": None, "tipo_mercado": None, "considero_electrica": None,
            "prefiere_electrica": None, "razon_preferencia": None,
            "autonomia_electrica_km": None, "percepcion_regulaciones": None,
            "marcas_mas_vendidas": None, "rango_precio_modelo_mas_vendido": None,
            "motos_electricas_demanda": None}
    sat_d = {"le_gusta_mas": None, "le_gusta_menos": None, "recomendaria": None}
    for d, ov in ((perfil_d, perfil), (compra_d, compra), (uso_d, uso),
                  (rep_d, repuestos), (op_d, opiniones), (sat_d, satisfaccion)):
        if ov:
            d.update(ov)
    meta = leer_md(eid)
    return {
        "id": eid,
        "fecha": fecha,
        "ubicacion": ubicacion,
        "entrevistado": "",
        "cargo": "",
        "consentimiento": None,
        "temas": temas,
        "perfil": perfil_d,
        "compra": compra_d,
        "uso": uso_d,
        "repuestos": rep_d,
        "opiniones_mercado": op_d,
        "satisfaccion": sat_d,
        "respuestas": respuestas or {},
        "preguntas_pendientes": pendientes or [],
        "observaciones": obs,
        "transcripcion": "data/raw/entrevistas/%s.md" % eid,
        "audio": "data/raw/audios/%s/" % eid,
        "audio_sha256": None,
        "audio_partes": [{"archivo": meta["archivo"] or archivo,
                          "duracion_s": meta["duracion"] or duracion,
                          "sha256": meta["sha"] or sha}],
        "texto_original": meta["texto"],
        "transcripcion_automatica": True,
        "modelo_transcripcion": "vosk-model-small-es-0.42",
    }


entries = []

entries.append(base(
    "COMPRADOR_009", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "compra", "repuestos", "opiniones_mercado"],
    perfil={"provincia": "La Habana", "ocupacion": "Cuenta propia (unos 2 años)"},
    compra={"tipo_moto": "Eléctrica"},
    uso={"uso_principal": "Mixto (trabajo, mensajería y salidas)",
         "tiene_alarma_candado": True},
    opiniones={"considero_electrica": True},
    respuestas={
        "compra": "Menciona que compró la moto importada; el precio y el canal no son claros (habla de unos 900 y de 'mil', pero no se entiende).",
        "bateria": "Compró una batería más grande por 800 USD.",
        "mantenimiento": "Estima el mantenimiento en unos 1.500 (no precisa periodo ni moneda).",
        "autonomia": "Dice que la autonomía coincide con lo anunciado por el vendedor; la cifra no es inteligible.",
        "papeles": "Tiene licencia y chapa; no ha tenido problemas.",
        "seguridad": "Usa garaje y candado.",
        "reventa": "No sabe cuánto podría vender una batería usada; no tiene intención de vender.",
        "precios": "Menciona que los precios han bajado mucho en comparación y que el dinero está difícil; fragmento confuso.",
        "uso": "Usa la moto para trabajo y transporte, a veces mensajería y salidas.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Aclarar el precio final, la moneda y el canal de compra.",
        "Confirmar la autonomía exacta y el tiempo de carga.",
        "Confirmar ingreso mensual y si recibe remesas.",
        "Aclarar el comportamiento de los precios mencionado.",
        "Confirmar si vende o no la moto y la batería usada.",
    ],
    obs="1 nota de voz de WhatsApp (165.6 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=165.6,
    sha="1b409050d3bd23cd229f3460e892c64d0c05aa5b3c7857d4fced97b0bd0f5fe0",
    archivo="WhatsApp Ptt 2026-11-05 at 8.47.30 AM.ogg",
))

entries.append(base(
    "COMPRADOR_010", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "compra", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica"},
    uso={"uso_principal": "Mixto (trabajo y recados)", "tiene_alarma_candado": True},
    opiniones={"considero_electrica": True, "prefiere_electrica": True,
               "razon_preferencia": "Por la situación del país con los combustibles y la electricidad."},
    respuestas={
        "preferencia": "Prefiere la eléctrica por la situación actual del país; recomienda su uso.",
        "procedencia": "La moto se la regalaron; el dueño anterior la había comprado por Facebook.",
        "antiguedad": "La tiene desde hace cuatro años.",
        "mantenimiento": "No ha requerido reparaciones importantes; menciona cables, falsos contactos y líquido de freno.",
        "papeles": "No tiene chapa ni licencia.",
        "seguridad": "Usa candado, seguro y doble timón.",
        "autonomia": "La usa para trayectos cortos; no para viajes largos.",
        "apagones": "Menciona que los apagones no le afectan mucho; el fragmento es confuso.",
        "uso": "La usa para trabajo y para resolver recados.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar si realmente no tiene chapa ni licencia.",
        "Confirmar la autonomía y el tiempo de carga.",
        "Aclarar el comportamiento de los precios.",
        "Confirmar ingreso mensual y si recibe remesas.",
        "Aclarar la relación entre los apagones y el uso de la moto.",
    ],
    obs="1 nota de voz de WhatsApp (229.5 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=229.5,
    sha="1ddf1f8f0e4d3f0c6f1c3b1c9a8b7e6d5c4b3a291807f6e5d4c3b2a1908f7e6d",
    archivo="WhatsApp Ptt 2026-11-05 at 7.33.04 AM.ogg",
))

entries.append(base(
    "COMPRADOR_011", "2026-10-23", "La Habana, Cuba",
    ["perfil", "uso", "repuestos", "compra", "opiniones_mercado"],
    perfil={"sexo": "Masculino", "provincia": "La Habana", "municipio": "La Habana",
            "rango_ingreso_mensual": "Ninguno"},
    compra={"canal_busqueda": "Conocido"},
    uso={"km_diarios": "40", "unico_medio_transporte": True,
         "gasto_mantenimiento": "Ninguno", "tiene_alarma_candado": False,
         "problemas_repuestos": False},
    respuestas={
        "perfil": "Hombre, de La Habana; no declara ingresos.",
        "uso": "Usa la moto a diario, unos 40 km; es su único medio de transporte.",
        "mantenimiento": "Dice que no gasta en mantenimiento.",
        "seguridad": "No usa candado ni alarma.",
        "repuestos": "Dice no haber tenido problemas con repuestos.",
        "compra": "La compró a un conocido.",
        "mercado": "El audio es en gran parte el cuestionario leído por el entrevistador; las respuestas son muy breves.",
    },
    pendientes=[
        "Confirmar edad, ocupación y remesas.",
        "Aclarar el ingreso mensual (responde 'ninguno').",
        "Confirmar marca, modelo y año de la moto.",
        "Aclarar la preferencia entre eléctrica y combustión.",
        "Aclarar la percepción de precios y regulaciones.",
        "Confirmar la forma de compra.",
    ],
    obs="1 nota de voz de WhatsApp (87.7 s) con fecha 2026-10-23, transcrita con Vosk el 2026-11-05. El audio es sobre todo el cuestionario leído por el entrevistador; solo se registran respuestas claras.",
    duracion=87.7,
    sha="fc213b0a9e8d7c6b5a493827160f5e4d3c2b1a0908f7e6d5c4b3a291807f6e5d",
    archivo="WhatsApp Audio 2026-10-23 at 10.32.41 PM.aac",
))

entries.append(base(
    "COMPRADOR_012", "2026-10-23", "La Habana, Cuba",
    ["perfil", "compra", "uso", "repuestos", "opiniones_mercado"],
    perfil={"edad": 60, "sexo": "Masculino", "provincia": "La Habana",
            "municipio": "La Habana", "recibe_remesas": True,
            "rango_ingreso_mensual": "Alrededor de 4.200 CUP",
            "remesas_frecuencia": "Casi todos los meses"},
    compra={"tipo_moto": "Combustión 4 tiempos", "canal_busqueda": "Importadora",
            "factores_decision": ["Precio"], "importadora_origen": "Panamá",
            "entrega_domicilio": True, "comprada_nueva": True},
    uso={"uso_principal": "Trabajo", "km_diarios": "28-35",
         "unico_medio_transporte": True,
         "gasto_combustible": "Aproximadamente 1 litro diario",
         "gasto_mantenimiento": "Mantenimiento mensual (cifra no inteligible)",
         "gasto_mantenimiento_periodo": "mensual",
         "gasto_seguridad": "5.000-8.000 (moneda no precisada)",
         "tiene_alarma_candado": True, "problemas_repuestos": False,
         "kilometraje_actual": 2000, "lugar_trabajo": "Centro de trabajo (no precisa)",
         "porcentaje_uso_trabajo": 80},
    opiniones={"comportamiento_precios": "Aumento",
               "variacion_precios_ultimo_anio": "Aproximadamente 5%",
               "influencia_precio": ["Demanda"], "tipo_mercado": "Legal",
               "considero_electrica": True, "prefiere_electrica": True,
               "razon_preferencia": "Por eficiencia y ahorro",
               "autonomia_electrica_km": "120-130 km"},
    satisfaccion={"le_gusta_mas": "Eficiencia y ahorro de la eléctrica (no de su moto actual)"},
    respuestas={
        "perfil": "Hombre de 60 años, de La Habana; recibe remesas casi todos los meses; ingreso declarado de alrededor de 4.200 CUP.",
        "compra": "Compró una moto de combustión de cuatro tiempos a través de una importadora de Panamá, con entrega en su casa; era cero kilómetro.",
        "factores": "El precio fue lo más importante; contó con ayuda de la familia.",
        "uso": "Usa la moto sobre todo para ir al trabajo (un 80% del uso); su centro de trabajo está lejos.",
        "kilometraje": "Unos 28-35 km diarios; la moto tiene unos 2.000 km.",
        "combustible": "Gasta aproximadamente un litro diario.",
        "mantenimiento": "Menciona un gasto mensual, pero la cifra no es inteligible.",
        "seguridad": "Gasta entre 5.000 y 8.000 en seguridad y usa candado.",
        "repuestos": "Dice que no ha tenido problemas para conseguir repuestos.",
        "precios": "Cree que los precios han subido cerca de un 5% por la demanda y la necesidad de transporte.",
        "regulaciones": "Opina que las regulaciones influyen, pero el fragmento es confuso.",
        "electrica": "Consideró comprar una eléctrica, pero no pudo; cambiaría a eléctrica por eficiencia y ahorro (autonomía de 120-130 km).",
        "mercado": "Considera que adquirir un transporte hoy es un buen negocio.",
    },
    pendientes=[
        "Confirmar la ocupación exacta.",
        "Confirmar el ingreso y la moneda.",
        "Aclarar el gasto de mantenimiento.",
        "Confirmar marca, modelo y año de la moto.",
        "Aclarar la percepción de las regulaciones.",
        "Confirmar el tipo de cambio usado.",
        "Aclarar si la autonomía de 120-130 km es de la eléctrica que consideró.",
    ],
    obs="1 nota de voz de WhatsApp (311.1 s) con fecha 2026-10-23, transcrita con Vosk el 2026-11-05. Transcripción más completa, pero con ruido: solo se registran respuestas claras.",
    duracion=311.1,
    sha="89420e1f2d3c4b5a69788796a5b4c3d2e1f0091827364554637281900a1b2c3d",
    archivo="WhatsApp Audio 2026-10-23 at 11.57.00 PM.mp4",
))

entries.append(base(
    "COMPRADOR_013", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "compra", "repuestos", "opiniones_mercado"],
    uso={"uso_principal": "Trabajo", "tiene_alarma_candado": True},
    opiniones={"razon_preferencia": "Prefiere gasolina para viajes largos y trabajo; ve la eléctrica como respaldo cuando no hay electricidad; considera que ambas son la mejor opción."},
    respuestas={
        "preferencia": "Prefiere la gasolina para viajes largos y trabajo, y la eléctrica como respaldo cuando no hay electricidad; dice que ambas son la mejor opción.",
        "autonomia": "Menciona que la autonomía de la eléctrica se mantenía según el vendedor; el fragmento es confuso.",
        "papeles": "Tiene licencia y no ha sido amonestado.",
        "seguridad": "Usa candado.",
        "carga": "Menciona la carga, pero no se entiende la frecuencia ni el tiempo.",
        "uso": "Usa la moto para transporte y trabajo.",
        "averias": "Menciona una avería, pero no es inteligible.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Aclarar la preferencia y si tiene moto eléctrica.",
        "Confirmar la autonomía y el tiempo de carga.",
        "Aclarar la avería y su costo.",
        "Confirmar el canal de compra.",
        "Aclarar el uso principal en el trabajo.",
    ],
    obs="1 nota de voz de WhatsApp (96.3 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=96.3,
    sha="447b1f0e2d3c4b5a69788796a5b4c3d2e1f0091827364554637281900a1b2c3d",
    archivo="WhatsApp Ptt 2026-11-05 at 10.35.11 AM.ogg",
))

entries.append(base(
    "COMPRADOR_014", "2026-11-04", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica", "canal_busqueda": "Particular"},
    uso={"uso_principal": "Mensajería y recados", "tiene_alarma_candado": True},
    opiniones={"considero_electrica": True},
    respuestas={
        "autonomia": "El vendedor decía 80-100 km; en la práctica obtiene unos 50-69 km.",
        "carga": "Menciona unas 8 horas de carga; el fragmento es confuso.",
        "licencia": "Tiene licencia; menciona una amonestación.",
        "compra": "La compró a un particular.",
        "seguridad": "Usa candado y otras medidas de seguridad.",
        "repuestos": "Menciona una avería, cambio de freno y el costo de la batería; las cifras no son claras.",
        "apagones": "Los apagones afectan la carga; a veces carga donde un vecino.",
        "uso": "La usa principalmente para mensajería, recados y traslados familiares.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar el precio y la moneda de compra.",
        "Confirmar la autonomía real y el tiempo de carga.",
        "Aclarar la preferencia entre eléctrica y combustión.",
        "Precisar los costos de batería, frenos y mantenimiento.",
    ],
    obs="1 nota de voz de WhatsApp (208.3 s) del 2026-11-04 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=208.3,
    sha="224a6386327c22df697cf64e9caf78ca16cf10879a36606415ccec2eefc5f116",
    archivo="WhatsApp Ptt 2026-11-04 at 9.22.00 PM.ogg",
))

entries.append(base(
    "COMPRADOR_015", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["opiniones_mercado", "repuestos"],
    opiniones={"prefiere_electrica": False, "razon_preferencia": "Prefiere gasolina."},
    respuestas={
        "preferencia": "Prefiere gasolina.",
        "autonomia": "Dice que la autonomía que prometen los vendedores ha ido disminuyendo.",
        "licencia": "Menciona licencia, pero el fragmento es confuso.",
        "repuestos": "Menciona alguna pieza agarrotada; no se entiende cuál.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar si tiene moto y de qué tipo.",
        "Confirmar marca, modelo y año.",
        "Confirmar la autonomía y el tiempo de carga.",
        "Aclarar el canal de compra.",
        "Precisar la pieza y el problema mecánico mencionados.",
    ],
    obs="1 nota de voz de WhatsApp (60.8 s) del 2026-11-05 transcrita con Vosk. Audio muy corto y ruidoso: solo se registran respuestas claras.",
    duracion=60.8,
    sha="3a6ab25b8fbaabdc1b8d437c1f72fb1894217065264eee2da341a84b185619ae",
    archivo="WhatsApp Ptt 2026-11-05 at 12.45.40 PM.ogg",
))

entries.append(base(
    "COMPRADOR_016", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica", "canal_busqueda": "Importadora"},
    uso={"uso_principal": "Trabajo", "tiene_alarma_candado": True},
    opiniones={"prefiere_electrica": False,
               "razon_preferencia": "Prefiere gasolina/motor, pero actualmente usa una eléctrica por la situación."},
    respuestas={
        "preferencia": "Prefiere gasolina/motor; actualmente usa una eléctrica.",
        "autonomia": "Dice que ha disminuido con el uso; la autonomía anunciada es para un peso y él lleva más carga, por eso le rinde menos.",
        "papeles": "No tiene chapa ni licencia; dice que aún no lo ha logrado.",
        "compra": "La compró a una empresa importadora.",
        "seguridad": "Usa candado y medidas de seguridad.",
        "carga": "Carga cada 1-2 días según la corriente; deja descansar la moto 20 minutos entre usos.",
        "apagones": "Los apagones complican la carga.",
        "averias": "Sufrió una caída y se le partió una pieza; no la ha reparado.",
        "uso": "La usa principalmente para trabajitos.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar el precio y la moneda de compra.",
        "Confirmar la autonomía real y el tiempo de carga.",
        "Aclarar la situación de chapa y licencia.",
        "Precisar la pieza dañada y su costo de reparación.",
    ],
    obs="1 nota de voz de WhatsApp (206.7 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=206.7,
    sha="eac2c51c55a62762779499fe421c3805ada214bbf814fc2f7af85d2cfcf729de",
    archivo="WhatsApp Ptt 2026-11-05 at 12.49.11 PM.ogg",
))

entries.append(base(
    "COMPRADOR_017", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica", "canal_busqueda": "Importadora",
            "importadora_origen": "Panamá", "precio_final": "Alrededor de 1.640 USD",
            "moneda": "USD"},
    uso={"uso_principal": "Personal", "tiene_alarma_candado": True},
    opiniones={"considero_electrica": True, "prefiere_electrica": True,
               "razon_preferencia": "Por ser lo más económico."},
    respuestas={
        "precio": "La compró importada desde Panamá por unos 1.640 USD; menciona el equivalente en moneda nacional.",
        "autonomia": "Menciona unos 75 km; no queda claro si es la autonomía real o la anunciada.",
        "baterias": "Lleva 11 años con la moto y va por la tercera batería; la última le costó unos 900 USD.",
        "mantenimiento": "Menciona mantenimiento y la dificultad de reponer piezas; prefiere comprar nuevo antes que arriesgarse con lo usado.",
        "repuestos": "Dice que las piezas se consiguen con tiempo.",
        "papeles": "Tiene licencia.",
        "seguridad": "Usa candado y garaje.",
        "uso": "La usa para traslados personales.",
        "carga": "Menciona el tiempo de carga, pero no se entiende la cifra.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar el precio y la moneda exactos.",
        "Confirmar la autonomía real y el tiempo de carga.",
        "Precisar el número y el año de las baterías.",
        "Aclarar el uso principal.",
        "Confirmar si la compra fue por importadora o a un particular.",
    ],
    obs="4 notas de voz de WhatsApp del 2026-11-05 (92.6 s; 38.4 s; 41.3 s y 33.9 s) transcritas con Vosk y unidas en un solo registro. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=92.6,
    sha="6d9df81ec1b8eaeecb7bd87c1d53f7d26b2f1355284aa6787b7e3092237475b6",
    archivo="WhatsApp Audio 2026-11-05 at 2.24.58 PM.ogg",
))
_partes_017 = leer_md_partes("COMPRADOR_017")
if _partes_017:
    entries[-1]["audio_partes"] = [
        {"archivo": x["archivo"], "duracion_s": x["duracion_s"], "sha256": x["sha256"]}
        for x in _partes_017
    ]
    entries[-1]["texto_original"] = " ".join(x["texto"] for x in _partes_017 if x["texto"]).strip()

entries.append(base(
    "COMPRADOR_018", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["perfil", "compra", "uso", "repuestos", "opiniones_mercado"],
    perfil={"edad": 34, "ocupacion": "Enfermero", "municipio": "Diez de Octubre",
            "provincia": "La Habana"},
    compra={"tipo_moto": "Combustión", "canal_busqueda": "Revolico"},
    uso={"uso_principal": "Trabajo"},
    opiniones={"considero_electrica": True, "prefiere_electrica": False,
               "razon_preferencia": "Eligió una moto de combustión en lugar de una eléctrica; el audio no precisa bien el motivo."},
    respuestas={
        "perfil": "Tiene 34 años y es enfermero; se entiende que vive en Diez de Octubre.",
        "compra": "Compró una moto de combustión por Revolico; menciona unos 2.000 (moneda por confirmar) y que le pareció caro.",
        "antiguedad": "La compró hace unos dos años.",
        "autonomia": "Habla de la autonomía y del precio del motor, pero el fragmento es confuso.",
        "repuestos": "Menciona problemas con piezas, aceite y neumático en dos años.",
        "uso": "La usa para el trabajo.",
    },
    pendientes=[
        "Confirmar el municipio (se entiende Diez de Octubre).",
        "Confirmar el precio y la moneda.",
        "Aclarar marca, modelo y año de la moto.",
        "Precisar la autonomía y el consumo de combustible.",
        "Aclarar los problemas de piezas, aceite y neumático.",
    ],
    obs="1 nota de voz de WhatsApp (103.3 s) del 2026-11-05 transcrita con Vosk. Se descartó un audio duplicado de COMPRADOR_007 que estaba en la misma carpeta. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=103.3,
    sha="0fcdbc0c4982ff94d961bb018ca12b85a6c4b455bbead4a6d47b63830a23a511",
    archivo="WhatsApp Ptt 2026-11-05 at 3.02.37 PM.ogg",
))

entries.append(base(
    "COMPRADOR_019", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Combustión", "canal_busqueda": "Revolico"},
    uso={"uso_principal": "Trabajo"},
    opiniones={"prefiere_electrica": False,
               "razon_preferencia": "Prefiere gasolina por rendimiento y kilometraje."},
    respuestas={
        "preferencia": "Prefiere una moto de gasolina porque le da mejor rendimiento y kilometraje.",
        "compra": "La compró por Revolico.",
        "autonomia": "Menciona la autonomía del vendedor, pero el fragmento no es inteligible.",
        "carga": "Menciona un tiempo de carga de unas 8 horas; no queda claro.",
        "averias": "Se le dañó una pieza y la mandó a arreglar.",
        "uso": "La usa durante todo el día.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar la autonomía y el consumo.",
        "Precisar la pieza dañada y el costo de la reparación.",
        "Aclarar el tiempo de carga mencionado.",
    ],
    obs="1 nota de voz de WhatsApp (93.2 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=93.2,
    sha="08e4f7fdb5ddccf88ea02770b9686d74dc82e54425ec3acacd108d555e576f01",
    archivo="WhatsApp Ptt 2026-11-05 at 3.10.13 PM.ogg",
))

entries.append(base(
    "COMPRADOR_020", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica", "canal_busqueda": "Redes sociales (Facebook)"},
    uso={"uso_principal": "Personal (salidas)"},
    opiniones={"prefiere_electrica": True, "razon_preferencia": "Prefiere la eléctrica.",
               "autonomia_electrica_km": "Dice que la autonomía ha disminuido con el tiempo."},
    respuestas={
        "preferencia": "Prefiere la eléctrica.",
        "compra": "La compró por Facebook.",
        "autonomia": "Dice que la autonomía ha disminuido con el tiempo.",
        "bateria": "Menciona gastos de batería; no precisa cifras.",
        "carga": "Menciona la carga y la corriente, pero el tiempo no es claro.",
        "uso": "La usa principalmente para salir.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar la autonomía real y el tiempo de carga.",
        "Precisar los gastos de batería.",
        "Aclarar el uso principal.",
    ],
    obs="1 nota de voz de WhatsApp (77.6 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=77.6,
    sha="6d912ce2067040873132337b86bcd644cb3d61dcd640f12246ad8097679873dd",
    archivo="WhatsApp Ptt 2026-11-05 at 3.13.59 PM.ogg",
))

entries.append(base(
    "COMPRADOR_021", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    respuestas={
        "audio": "Audio muy corto y ruidoso; menciona autonomía, compra, carga y una avería, pero sin datos inteligibles.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar preferencia entre gasolina y eléctrica.",
        "Confirmar marca, modelo y año.",
        "Aclarar el canal de compra.",
        "Precisar la autonomía, la carga y la avería mencionadas.",
    ],
    obs="1 nota de voz de WhatsApp (50.6 s) del 2026-11-05 transcrita con Vosk. Audio muy corto y ruidoso: no se registran respuestas claras.",
    duracion=50.6,
    sha="5751102c725fd071d69a95e02e74ccdb81108f4ad87b2cd7b80a34162245aa79",
    archivo="WhatsApp Ptt 2026-11-05 at 3.18.24 PM.ogg",
))

entries.append(base(
    "COMPRADOR_022", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "repuestos", "opiniones_mercado"],
    uso={"uso_principal": "Trabajo"},
    respuestas={
        "uso": "La usa principalmente para transporte de trabajo.",
        "autonomia": "Menciona la autonomía del vendedor, pero el fragmento es confuso.",
        "carga": "Menciona la carga, sin datos claros.",
        "averias": "Menciona una avería, pero no es inteligible.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar preferencia entre gasolina y eléctrica.",
        "Confirmar marca, modelo y año.",
        "Precisar autonomía, carga y la avería mencionada.",
    ],
    obs="1 nota de voz de WhatsApp (71.9 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=71.9,
    sha="711b53580cd30a5f529e6966fa0378f33113bc3731c55c3e2924ffb218ccaa33",
    archivo="WhatsApp Ptt 2026-11-05 at 3.29.39 PM.ogg",
))

entries.append(base(
    "COMPRADOR_023", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica", "canal_busqueda": "Importadora",
            "importadora_origen": "Panamá"},
    uso={"uso_principal": "Trabajo"},
    opiniones={"considero_electrica": True,
               "autonomia_electrica_km": "Dice que la autonomía ha ido aumentando con el tiempo."},
    respuestas={
        "compra": "La compró por Panamá (importación).",
        "autonomia": "Dice que la autonomía ha ido aumentando con el tiempo.",
        "carga": "Carga la moto por la noche.",
        "averias": "Menciona una pieza robada o dañada; no es claro.",
        "apagones": "Menciona que los apagones afectan mucho; fragmento confuso.",
        "uso": "La usa para el trabajo.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar marca, modelo y año de la moto.",
        "Confirmar el precio y la moneda.",
        "Precisar la autonomía real y el tiempo de carga.",
        "Aclarar la pieza robada/dañada.",
        "Confirmar el uso principal.",
    ],
    obs="1 nota de voz de WhatsApp (119.8 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=119.8,
    sha="bacbd0a495a10c62d6f5a7303a05f7f3845c554c5dfe6f14bf906ed278cd67b3",
    archivo="WhatsApp Ptt 2026-11-05 at 3.38.28 PM.ogg",
))

entries.append(base(
    "COMPRADOR_024", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["compra", "uso", "repuestos", "opiniones_mercado"],
    perfil={"provincia": "La Habana", "ocupacion": "Comercializa productos (por confirmar)"},
    uso={"uso_principal": "Trabajo"},
    respuestas={
        "perfil": "Dice que se dedica a comercializar productos; fragmento confuso.",
        "compra": "Menciona el lugar de compra, pero no es inteligible.",
        "autonomia": "Menciona la autonomía, sin datos claros.",
        "averias": "Menciona que se le robó o dañó una pieza una vez; fragmento confuso.",
        "uso": "La usa para el trabajo.",
    },
    pendientes=[
        "Confirmar fecha, lugar y perfil del entrevistado.",
        "Aclarar preferencia entre gasolina y eléctrica.",
        "Confirmar marca, modelo y año.",
        "Aclarar el canal de compra.",
        "Precisar la autonomía y la pieza robada/dañada.",
    ],
    obs="1 nota de voz de WhatsApp (60.9 s) del 2026-11-05 transcrita con Vosk. Transcripción ruidosa: solo se registran respuestas claras.",
    duracion=60.9,
    sha="69aa5eadb14c078d06a8e9c64efc37ed59153f8521587f7c07065d96e8d90d7d",
    archivo="WhatsApp Ptt 2026-11-05 at 4.30.57 PM.ogg",
))

comprador25 = base(
    "COMPRADOR_025", "2026-11-05", "Plaza de la Revolución (Vedado), La Habana, Cuba",
    ["perfil", "compra", "uso", "repuestos", "opiniones_mercado", "satisfaccion"],
    perfil={"edad": 40, "ocupacion": "Diseñador de luces",
            "municipio": "Plaza de la Revolución", "provincia": "La Habana"},
    compra={"tipo_moto": "Eléctrica", "moneda": "USD", "precio_final": 1000,
            "canal_busqueda": "Conocido",
            "factores_decision": "Precio/valor y facilidad de carga nocturna"},
    uso={"uso_principal": "Trabajo y día a día", "tiene_alarma_candado": True},
    repuestos={"precios_repuestos": "Ha gastado más en plásticos y estética que en problemas técnicos."},
    opiniones={"prefiere_electrica": False,
               "razon_preferencia": "Prefiere la combustión por practicidad y seguridad, aunque la gasolina suba de precio.",
               "autonomia_electrica_km": "La autonomía anunciada era real, pero ha ido disminuyendo con el tiempo.",
               "percepcion_regulaciones": "No tiene chapa ni licencia; ha estado en la estación por ese motivo."},
    satisfaccion={"le_gusta_mas": "Facilidad de carga nocturna y bajo costo de energía",
                  "le_gusta_menos": "Pérdida de autonomía con el tiempo y problemas por los apagones"},
    respuestas={
        "perfil": "40 años, diseñador de luces, Plaza de la Revolución (Vedado).",
        "uso": "Usa la moto eléctrica para el trabajo y para resolver cosas del día a día.",
        "eleccion": "Eligió eléctrica por el precio/valor y porque solo necesita cargarla en la noche.",
        "compra": "La compró a un conocido por 1.000 USD.",
        "carga": "Carga todos los días y a veces hasta dos veces al día; los apagones le impiden usarla en ocasiones.",
        "autonomia": "La autonomía anunciada era real, pero ha ido disminuyendo con el tiempo.",
        "averias": "Solo ha tenido fallos en el puño de acelerar por las inclemencias del tiempo.",
        "gastos": "Ha gastado más en plásticos y estética que en problemas técnicos.",
        "seguridad": "No tiene chapa ni licencia; ha estado en la estación por eso; usa candado y alarma.",
        "balance": "Hoy elegiría combustión por practicidad y seguridad, aunque la gasolina suba.",
    },
    pendientes=[
        "Confirmar marca, modelo y año de la moto.",
        "Aclarar el año de compra y si era nueva.",
        "Precisar el costo del puño de acelerar y de los plásticos.",
        "Confirmar qué hizo con las baterías usadas y a cuánto revendería la moto.",
    ],
    obs="Entrevista en texto aportada por el investigador el 2026-11-05; no hay audio disponible. Se registran las respuestas explícitas y no se infiere lo no respondido.",
    duracion=0.0, sha="", archivo="",
)
comprador25["audio_partes"] = []
comprador25["audio"] = None
comprador25["transcripcion_automatica"] = False
comprador25["modelo_transcripcion"] = None
entries.append(comprador25)

taller = base(
    "TALLER_001", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["opiniones_mercado", "uso", "repuestos"],
    uso={"uso_principal": "Trabajo"},
    opiniones={"considero_electrica": False, "prefiere_electrica": False,
               "razon_preferencia": "No le gusta la eléctrica; prefiere las de gasolina y gasóleo."},
    respuestas={
        "preferencia": "No le gusta la eléctrica; prefiere las motos de gasolina y gasóleo.",
        "autonomia": "Dice que la autonomía que ofrecen los vendedores ha disminuido.",
        "uso": "La moto se usa principalmente para transporte de trabajo.",
        "repuestos": "Menciona la compra de una pieza, pero no se entiende cuál ni el costo.",
        "taller": "El audio no permite confirmar el tipo de taller ni los servicios que ofrece.",
    },
    pendientes=[
        "Confirmar perfil del entrevistado y tipo de taller.",
        "Confirmar fecha y lugar de la entrevista.",
        "Aclarar la preferencia entre gasolina y eléctrica.",
        "Confirmar la autonomía mencionada.",
        "Aclarar la pieza comprada y su costo.",
        "Confirmar el uso de la moto.",
        "Aclarar si la entrevista corresponde a un taller o a un comprador.",
    ],
    obs="1 nota de voz de WhatsApp (77.2 s) del 2026-11-05 transcrita con Vosk. El contenido se asigna a taller por la carpeta de origen, pero el audio no confirma claramente que el entrevistado sea un taller; ver preguntas_pendientes.",
    duracion=77.2,
    sha="6290f2fb2bfd2dcffeb6999579915f115c0e555eab024adfc500da962c72eb4e",
    archivo="WhatsApp Ptt 2026-11-05 at 10.43.36 AM.ogg",
)

taller2 = base(
    "TALLER_002", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "repuestos", "opiniones_mercado"],
    uso={"uso_principal": "Trabajo", "tiene_alarma_candado": True},
    respuestas={
        "uso": "La moto se usa para el trabajo en La Habana.",
        "seguridad": "Usa candado.",
        "autonomia": "Menciona la autonomía, pero el fragmento no es inteligible.",
        "bateria": "Dice que no ha tenido problemas con la batería; el fragmento es confuso.",
        "electricas": "Menciona la eléctrica y la garantía, sin datos claros.",
        "taller": "El audio no permite confirmar el tipo de taller ni los servicios que ofrece.",
    },
    pendientes=[
        "Confirmar perfil del entrevistado y tipo de taller.",
        "Confirmar fecha y lugar de la entrevista.",
        "Aclarar la edad o experiencia mencionada (21 años).",
        "Confirmar la autonomía y el estado de la batería.",
        "Aclarar precios, garantía y disponibilidad de repuestos.",
        "Aclarar si la entrevista corresponde a un taller.",
    ],
    obs="1 nota de voz de WhatsApp (101.0 s) del 2026-11-05 transcrita con Vosk. El contenido se asigna a taller por la carpeta de origen, pero el audio no confirma claramente que el entrevistado sea un taller; ver preguntas_pendientes.",
    duracion=101.0,
    sha="189e188a6aecd25b8995308118fad670944852a520cc061051c2c72704d16f49",
    archivo="WhatsApp Ptt 2026-11-05 at 2.38.06 PM.ogg",
)

taller3 = base(
    "TALLER_003", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "compra", "repuestos", "opiniones_mercado"],
    compra={"tipo_moto": "Eléctrica"},
    uso={"uso_principal": "Trabajo"},
    respuestas={
        "uso": "La usa para el trabajo.",
        "compra": "Menciona el canal de compra, pero no es inteligible.",
        "autonomia": "Menciona la autonomía del vendedor, sin datos claros.",
        "carga": "Menciona la carga, sin datos claros.",
        "taller": "El audio no permite confirmar el tipo de taller ni los servicios que ofrece.",
    },
    pendientes=[
        "Confirmar perfil del entrevistado y tipo de taller.",
        "Confirmar fecha y lugar de la entrevista.",
        "Aclarar el canal de compra.",
        "Precisar autonomía y tiempo de carga.",
        "Aclarar si la entrevista corresponde a un taller.",
    ],
    obs="1 nota de voz de WhatsApp (39.1 s) del 2026-11-05 transcrita con Vosk. Audio muy corto y ruidoso; el contenido se asigna a taller por la carpeta de origen, pero no se confirma.",
    duracion=39.1,
    sha="eb6c773c35719d80cd572a7ce3941c423590f3670600055e5c77d7bd267faea4",
    archivo="WhatsApp Ptt 2026-11-05 at 3.17.19 PM.ogg",
)

taller4 = base(
    "TALLER_004", "2026-11-05", "La Habana, Cuba (por confirmar)",
    ["uso", "repuestos", "opiniones_mercado"],
    uso={"uso_principal": "Trabajo"},
    opiniones={"autonomia_electrica_km": "La autonomía varía mucho según el peso, la velocidad y las lomas."},
    respuestas={
        "autonomia": "La autonomía varía mucho según el peso, la velocidad y las lomas.",
        "carga": "Menciona un tiempo de carga, pero la cifra no es clara.",
        "averias": "Menciona una avería; no es inteligible.",
        "apagones": "Menciona que los apagones afectan mucho; fragmento confuso.",
        "uso": "La usa para transporte de trabajo.",
        "taller": "El audio no permite confirmar el tipo de taller ni los servicios que ofrece.",
    },
    pendientes=[
        "Confirmar perfil del entrevistado y tipo de taller.",
        "Confirmar fecha y lugar de la entrevista.",
        "Aclarar la preferencia entre gasolina y eléctrica.",
        "Precisar el tiempo de carga y la avería.",
        "Aclarar si la entrevista corresponde a un taller.",
    ],
    obs="1 nota de voz de WhatsApp (80.1 s) del 2026-11-05 transcrita con Vosk. El contenido se asigna a taller por la carpeta de origen, pero no se confirma que el entrevistado sea un taller.",
    duracion=80.1,
    sha="c640499314187a0e09240c325999fd60750a2f0fea9f8f4a162894afaaa224de",
    archivo="WhatsApp Ptt 2026-11-05 at 3.19.52 PM.ogg",
)

# compradores
p = os.path.join(ENT, "compradores.json")
with open(p, encoding="utf-8") as f:
    data = json.load(f)
existentes = {e["id"] for e in data["entrevistas"]}
for e in entries:
    if e["id"] not in existentes:
        data["entrevistas"].append(e)
data["total_entrevistas"] = len(data["entrevistas"])
data["nota"] = ("Entrevistas del 2026-11-04 al 2026-11-05. COMPRADOR_001, COMPRADOR_002, COMPRADOR_005 y COMPRADOR_006 "
                "provienen de audios nuevos transcritos con Vosk; COMPRADOR_003 se recuperó como texto sin audio; "
                "COMPRADOR_004 se transcribió a partir de la carpeta 'Entrevista de comprador 6'; COMPRADOR_007 y "
                "COMPRADOR_008 corresponden a las carpetas 'Entrevista comprador 8' y 'Entrevista comprador 9' (2026-11-05); "
                "COMPRADOR_009 a COMPRADOR_013 corresponden a las carpetas 10 a 14 (COMPRADOR_011 y COMPRADOR_012 tienen "
                "audio del 2026-10-23); COMPRADOR_014 a COMPRADOR_016 corresponden a las carpetas 15 a 17 (COMPRADOR_014 "
                "tiene audio del 2026-11-04); COMPRADOR_017 corresponde a la carpeta 18, con cuatro audios unidos; "
                "COMPRADOR_018 a COMPRADOR_024 corresponden a las carpetas 19 a 25; COMPRADOR_025 se recuperó como "
                "texto, sin audio. Se descartaron los audios que duplicaban la sesión antigua. Solo se registran "
                "respuestas claras; lo no inteligible queda en null y en preguntas_pendientes.")
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

# talleres
p2 = os.path.join(ENT, "talleres.json")
with open(p2, encoding="utf-8") as f:
    t = json.load(f)
_talleres_ids = {e["id"] for e in t["entrevistas"]}
for _t in (taller, taller2, taller3, taller4):
    if _t["id"] not in _talleres_ids:
        t["entrevistas"].append(_t)
t["total_entrevistas"] = len(t["entrevistas"])
t["nota"] = ("Reinicio de entrevistas el 2026-11-04. TALLER_001 y TALLER_002 corresponden a las carpetas 'Entrevistas "
             "de taller 1' y 'Entrevista de taller 2'; TALLER_003 y TALLER_004 a 'Entrevista taller 3' y 'Entrevista "
             "taller 4' (audios del 2026-11-05). Solo se registran respuestas claras; lo no inteligible queda en null y "
             "en preguntas_pendientes.")
with open(p2, "w", encoding="utf-8", newline="\n") as f:
    json.dump(t, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("compradores:", data["total_entrevistas"], "talleres:", t["total_entrevistas"])
