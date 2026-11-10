import sys, json

lineas = sys.stdin.read().splitlines()

P_ENTRADA = 300
P_ESCRITURA = 375
P_LECTURA = 30
P_SALIDA = 1500

def fmt(unidades):
    micro = (unidades + 50) // 100
    return f"${micro // 1000000}.{micro % 1000000:06d}"

total = 0
sin_cache = 0
aciertos = 0
n = 0

for linea in lineas:
    linea = linea.strip()
    if linea:
        uso = json.loads(linea)
        entrada = uso.get("input_tokens", 0)
        escritura = uso.get("cache_creation_input_tokens", 0)
        lectura = uso.get("cache_read_input_tokens", 0)
        salida = uso.get("output_tokens", 0)

        costo = (entrada * P_ENTRADA
                + escritura * P_ESCRITURA
                + lectura * P_LECTURA
                + salida * P_SALIDA)
        costo_sin = (entrada + escritura + lectura) * P_ENTRADA + salida * P_SALIDA

        n += 1
        total += costo
        sin_cache += costo_sin
        if lectura > 0:
            aciertos += 1

        print(f"solicitud {n}: {fmt(costo)}")

print(f"total: {fmt(total)}")
print(f"sin_cache: {fmt(sin_cache)}")
print(f"ahorro: {fmt(sin_cache - total)}")
print(f"aciertos_de_cache: {aciertos}/{n}")