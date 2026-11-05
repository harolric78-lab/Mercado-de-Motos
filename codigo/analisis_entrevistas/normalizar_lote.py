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
                "audio del 2026-10-23). Se descartaron los audios que duplicaban la sesión antigua. Solo se registran "
                "respuestas claras; lo no inteligible queda en null y en preguntas_pendientes.")
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

# talleres
p2 = os.path.join(ENT, "talleres.json")
with open(p2, encoding="utf-8") as f:
    t = json.load(f)
if taller["id"] not in {e["id"] for e in t["entrevistas"]}:
    t["entrevistas"].append(taller)
t["total_entrevistas"] = len(t["entrevistas"])
t["nota"] = ("Reinicio de entrevistas el 2026-11-04. TALLER_001 corresponde a la carpeta 'Entrevistas de taller 1' "
             "(audio del 2026-11-05). Solo se registran respuestas claras; lo no inteligible queda en null y en "
             "preguntas_pendientes.")
with open(p2, "w", encoding="utf-8", newline="\n") as f:
    json.dump(t, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("compradores:", data["total_entrevistas"], "talleres:", t["total_entrevistas"])
