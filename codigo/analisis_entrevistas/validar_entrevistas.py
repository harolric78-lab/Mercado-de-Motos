# -*- coding: utf-8 -*-
import json, os, re, sys

BASE = r"C:\Users\LA RUEDA\Desktop\Proyecto de ICD Motos en cuba (2)\Mercado-de-Motos"
ENT = os.path.join(BASE, "docs", "entrevistas")
RAW = os.path.join(BASE, "data", "raw", "entrevistas")
pat = re.compile(r"^(COMPRADOR|TALLER|IMPORTADORA|ENTREVISTA)_[0-9]{3}$")

files = {"compradores.json": "COMPRADOR", "talleres.json": "TALLER", "importadoras.json": "IMPORTADORA"}
hashes = {}
errors = []
total = 0
ref_keys = None
for fname, pref in files.items():
    with open(os.path.join(ENT, fname), encoding="utf-8") as f:
        d = json.load(f)
    if d["total_entrevistas"] != len(d["entrevistas"]):
        errors.append(f"{fname}: total {d['total_entrevistas']} != {len(d['entrevistas'])}")
    ids = [e["id"] for e in d["entrevistas"]]
    if len(ids) != len(set(ids)):
        errors.append(f"{fname}: IDs duplicados")
    for e in d["entrevistas"]:
        total += 1
        if not pat.match(e["id"]):
            errors.append(f"ID inválido: {e['id']}")
        if not e["id"].startswith(pref + "_"):
            errors.append(f"{e['id']} en {fname}")
        keys = set(e.keys())
        if ref_keys is None:
            ref_keys = keys
        elif keys != ref_keys:
            errors.append(f"{e['id']}: claves distintas")
        for block in ("perfil", "compra", "uso", "repuestos", "opiniones_mercado", "satisfaccion"):
            if block not in e or not isinstance(e[block], dict):
                errors.append(f"{e['id']}: falta bloque {block}")
        tp = os.path.join(BASE, e["transcripcion"].replace("/", os.sep))
        if not os.path.exists(tp):
            errors.append(f"{e['id']}: no existe {e['transcripcion']}")
        else:
            content = open(tp, encoding="utf-8").read()
            paras = [x.strip() for x in content.split("\n\n") if x.strip()]
            if len(e["audio_partes"]) > 1:
                sec = re.findall(
                    r"## .+?\n\n- \*\*SHA256:\*\* `([0-9a-fA-F]{64})`\n"
                    r"- \*\*Duraci[oó]n:\*\* ([\d.]+) s\n.*?\n\n(.*?)(?=\n## |\Z)",
                    content, re.S,
                )
                texto_md = " ".join(x[2].strip() for x in sec).strip()
                shas_md = [x[0] for x in sec]
                shas_json = [p["sha256"] for p in e["audio_partes"]]
                if shas_md != shas_json:
                    errors.append(f"{e['id']}: los SHA del .md no coinciden con audio_partes")
                if texto_md != e["texto_original"]:
                    errors.append(f"{e['id']}: texto_original difiere del .md (multiparte)")
            else:
                if paras[-1] != e["texto_original"]:
                    errors.append(f"{e['id']}: texto_original difiere del .md")
                m = re.search(r"\*\*SHA256:\*\* `([0-9a-fA-F]{64})`", content)
                if m and e["audio_partes"] and m.group(1) != e["audio_partes"][0]["sha256"]:
                    errors.append(f"{e['id']}: sha del .md difiere del JSON")
        for p in e["audio_partes"]:
            h = p["sha256"]
            if h in hashes:
                errors.append(f"hash duplicado: {e['id']} y {hashes[h]}")
            hashes[h] = e["id"]

print("Total entrevistas:", total)
for fname, pref in files.items():
    d = json.load(open(os.path.join(ENT, fname), encoding="utf-8"))
    print(f"  {fname}: {d['total_entrevistas']} ({', '.join(e['id'] for e in d['entrevistas'])})")
print("Hashes únicos:", len(hashes))
if errors:
    print("ERRORES:")
    for x in errors:
        print(" -", x)
    sys.exit(1)
print("OK: validación estructural")
