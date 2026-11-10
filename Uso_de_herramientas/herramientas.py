import sys, json

lineas = sys.stdin.read().splitlines()

CLIMA = {"Bogota": 14, "Medellin": 24, "Cali": 26}

def calculadora(entrada):
    op = entrada.get("operacion")
    a = entrada.get("a")
    b = entrada.get("b")
    if op == "sumar":
        return str(a + b)
    if op == "restar":
        return str(a - b)
    if op == "multiplicar":
        return str(a * b)
    if op == "dividir":
        if b == 0:
            return "error: división por cero"
        return str(a // b)
    return f"error: operación desconocida: {op}"

def clima(entrada):
    ciudad = entrada.get("ciudad")
    if ciudad in CLIMA:
        return f"{CLIMA[ciudad]} °C"
    return f"error: ciudad desconocida: {ciudad}"

HERRAMIENTAS = {"calculadora": calculadora, "clima": clima}

llamadas = 0
errores = 0

for linea in lineas:
    linea = linea.strip()
    if linea:
        respuesta = json.loads(linea)
        motivo = respuesta.get("stop_reason")
        contenido = respuesta.get("content", [])

        if motivo == "tool_use":
            for bloque in contenido:
                if bloque.get("type") == "tool_use":
                    nombre = bloque["name"]

                    if nombre in HERRAMIENTAS:
                        resultado = HERRAMIENTAS[nombre](
                            bloque.get("input", {})
                        )
                    else:
                        resultado = f"error: herramienta desconocida: {nombre}"

                    llamadas += 1

                    if resultado.startswith("error:"):
                        errores += 1

                    print(f"tool_result {bloque['id']} {resultado}")

        elif motivo == "end_turn":
            texto = "".join(
                b["text"] for b in contenido if b.get("type") == "text"
            )
            print(f"final: {texto}")

print(f"resumen: {llamadas} llamadas, {errores} errores")