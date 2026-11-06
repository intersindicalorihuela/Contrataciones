#!/usr/bin/env python3
"""Genera index.html a partir del Excel de contrataciones.

Uso:  python convert.py [Contrataciones.xlsx]
Requiere:  pip install openpyxl
Lee todas las hojas que tengan las columnas Nombre/Turno/Categoría/Departamento/
Posición/Inicio/Fin/TNom/B/Jor (por cabecera, no por posición) y escribe index.html.
"""
import sys, json, datetime as dt, calendar, unicodedata
import openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else "Contrataciones.xlsx"
EPOCH = dt.date(1970, 1, 1)

def norm(s):
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return s.replace(".", "").replace(" ", "")

# nombre normalizado de cabecera -> campo
HDR = {"nombre": "nombre", "turno": "turno", "categoria": "cat", "departamento": "dpto",
       "posicion": "pos", "finicio": "ini", "inicio": "ini", "ffin": "fin", "fin": "fin",
       "tnom": "tnom", "b": "b", "jor": "jor"}
TURNO = {"O": "O", "ORDINARIO": "O", "P": "P", "PROMOCIONINTERNATEMPORAL": "P"}

def day(v):
    if isinstance(v, dt.datetime): v = v.date()
    return (v - EPOCH).days if isinstance(v, dt.date) else None

def code(v):  # "S." -> "S"
    return str(v or "").strip().rstrip(".").upper()

cats, perfiles, dptos, rows, avisos = [], [], [], [], []
def idx(lst, v):
    if v not in lst: lst.append(v)
    return lst.index(v)

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
for ws in wb.worksheets:
    it = ws.iter_rows(values_only=True)
    head = next(it, None)
    if not head: continue
    col = {}
    for i, h in enumerate(head):
        f = HDR.get(norm(h))
        if f and f not in col: col[f] = i
    if not {"nombre", "cat", "dpto", "ini"} <= set(col):
        avisos.append(f"Hoja ignorada: {ws.title}"); continue
    n = 0
    for r in it:
        g = lambda k: r[col[k]] if k in col and col[k] < len(r) else None
        nombre = g("nombre")
        if not nombre or day(g("ini")) is None: continue
        cat = str(g("cat") or "").strip()
        perfil = -1
        if "- Perfil:" in cat:
            cat, p = [x.strip() for x in cat.split("- Perfil:", 1)]
            perfil = idx(perfiles, p)
        pos = g("pos")
        rows.append([str(nombre).strip(), idx(cats, cat), perfil, idx(dptos, str(g("dpto") or "").strip()),
                     int(pos) if isinstance(pos, (int, float)) else None, day(g("ini")), day(g("fin")),
                     TURNO.get(norm(g("turno")).upper(), code(g("turno"))), code(g("tnom")), code(g("b")), code(g("jor"))])
        n += 1
    print(f"{ws.title}: {n} filas")

fechas = [x for r in rows for x in (r[5], r[6]) if x is not None]
maxf = max(fechas)
d = EPOCH + dt.timedelta(days=maxf)
corte = dt.date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])  # fin de mes de los datos
data = {"maxfecha": maxf, "corte": (corte - EPOCH).days, "cats": cats, "perfiles": perfiles, "dptos": dptos, "rows": rows}

tpl = open("template.html", encoding="utf8").read()
js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
open("index.html", "w", encoding="utf8").write(tpl.replace("{{DATA}}", js))
print(f"OK: {len(rows)} contratos · último dato {d} · corte {corte} · index.html generado")
for a in avisos: print("AVISO:", a)
