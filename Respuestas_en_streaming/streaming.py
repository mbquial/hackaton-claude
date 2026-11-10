import sys, json

lineas = sys.stdin.read().splitlines()

bloques = {}
stop_reason = None
input_tokens = 0
output_tokens = 0

for linea in lineas:
    linea = linea.strip()
    if linea.startswith("data:"):
        evento = json.loads(linea[len("data:"):].strip())
        tipo = evento.get("type")

        if tipo == "message_start":
            bloques = {}
            stop_reason = None
            input_tokens = evento["message"]["usage"]["input_tokens"]
            output_tokens = 0

        elif tipo == "content_block_delta":
            delta = evento["delta"]
            if delta.get("type") == "text_delta":
                idx = evento["index"]
                bloques[idx] = bloques.get(idx, "") + delta["text"]

        elif tipo == "message_delta":
            stop_reason = evento["delta"].get("stop_reason")
            output_tokens = evento["usage"]["output_tokens"]

        elif tipo == "message_stop":
            texto = "".join(bloques[i] for i in sorted(bloques))
            print(f"texto: {texto}")
            print(f"stop_reason: {stop_reason}")
            print(f"input_tokens: {input_tokens}")
            print(f"output_tokens: {output_tokens}")
