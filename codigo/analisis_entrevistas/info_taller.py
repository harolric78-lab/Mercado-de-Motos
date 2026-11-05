import av, hashlib, os
root=r"C:\Users\LA RUEDA\Desktop\Proyecto de ICD Motos en cuba (2)\Entrevistas"
for carpeta in ["Entrevistas de taller 1","Nueva carpeta"]:
    p=os.path.join(root,carpeta)
    for f in os.listdir(p):
        full=os.path.join(p,f)
        if not os.path.isfile(full): continue
        try:
            with av.open(full) as c:
                d=c.duration/1_000_000 if c.duration else -1
        except Exception as e:
            d=-1
        h=hashlib.sha256(open(full,"rb").read()).hexdigest()
        print(f"{carpeta} | {f} | {d:.1f}s | {h}")
