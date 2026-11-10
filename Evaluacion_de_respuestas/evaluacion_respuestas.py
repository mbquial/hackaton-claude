import sys, json, unicodedata

lineas = sys.stdin.read().splitlines()

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = "".join(c if c.isalnum() else " " for c in texto)
    return " " + " ".join(texto.split()) + " "

por_categoria = {}
aprobadas_total = 0
n = 0

for linea in lineas:
    linea = linea.strip()
    if linea:
        caso = json.loads(linea)
        esperado = normalizar(caso["esperado"])
        respuesta = normalizar(caso["respuesta"])

        paso = esperado in respuesta

        cat = caso["categoria"]
        if cat not in por_categoria:
            por_categoria[cat] = [0, 0]
        por_categoria[cat][1] += 1
        if paso:
            por_categoria[cat][0] += 1
            aprobadas_total += 1
        n += 1

for cat in sorted(por_categoria):
    a, t = por_categoria[cat]
    print(f"{cat}: {a}/{t}")
if n == 0:
    p10 = 0
else:
    p10 = (aprobadas_total * 2000 + n) // (2 * n)
print(f"total: {aprobadas_total}/{n} ({p10 // 10}.{p10 % 10}%)")