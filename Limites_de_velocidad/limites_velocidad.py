import sys

lineas = sys.stdin.read().splitlines()

solicitudes = [3, 1]
tokens = [100, 20]

sol = solicitudes[0]
tok = tokens[0]
ultimo = 0

for linea in lineas:
    partes = linea.split()
    if len(partes) == 4 or partes[0] == "REQUEST":
        t = int(partes[1])
        nuevos = int(partes[2])
        dt = t - ultimo
        sol = min(solicitudes[0], sol + dt * solicitudes[1])
        tok = min(tokens[0], tok + dt * tokens[1])
        ultimo = t

        falta_sol = max(0, 1 - sol)
        falta_tok = max(0, nuevos - tok)

        if falta_sol == 0 and falta_tok == 0:
            sol -= 1
            tok -= nuevos
            print("ok")
        else:
            espera_sol = -(-falta_sol // solicitudes[1])
            espera_tok = -(-falta_tok // tokens[1])
            print(f"429 retry-after={max(espera_sol, espera_tok)}")