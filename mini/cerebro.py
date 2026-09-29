"""
cerebro.py - Modulo de razonamiento para ASIRU (Fase 2 + Fase 3)

Usa Ollama/Llama2 como LLM local.

Fase 2: Conecta con Ollama para razonar y conversar.
Fase 3: Primero chequea si el usuario quiere una habilidad local (hora, cálculo,
        recordatorios), y si no, manda la pregunta a Llama2.

NOTA: Para cambiar a otro LLM (Claude, OpenAI, etc.), ver MODELOS.md
"""

from ollama import Client as OllamaClient
from intents import detectar_intent

# Configuración de Ollama/Llama2
OLLAMA_HOST = "http://localhost:11434"  # Puerto por defecto de Ollama
MODELO = "phi3"  # Modelo que descargaste con `ollama run llama2`

PERSONALIDAD = """Eres ASIRU, un asistente de inteligencia artificial inspirado en JARVIS.
Hablas claro y directo, con un toque de humor seco pero nunca exagerado.
Eres muy competente: no rellenas tus respuestas con paja innecesaria.
Tus respuestas se convierten en voz, asi que se breve -- una o dos frases,
salvo que te pidan explicitamente mas detalle.
Te diriges a tu usuario con cercania y respeto, nunca de forma robotica o generica."""

_cliente = None
_historial = []


def _cargar_cliente():
    """Crea el cliente de Ollama una sola vez y lo reutiliza."""
    global _cliente
    if _cliente is None:
        try:
            _cliente = OllamaClient(host=OLLAMA_HOST)
            # Prueba que Ollama esté accesible
            _cliente.list()
        except Exception as e:
            raise ConnectionError(
                f"No puedo conectar a Ollama en {OLLAMA_HOST}.\n"
                f"¿Está Ollama corriendo? Abre otra terminal y ejecuta:\n"
                f"  ollama run {MODELO}\n"
                f"Error: {e}"
            )
    return _cliente


def pensar(texto_usuario):
    """Fase 3: Primero intenta detectar si el usuario quiere una habilidad local.
    Si no hay intent detectado, manda a Llama2 para que piense la respuesta.
    Actualiza el historial en el camino."""
    
    # Fase 3: Detección de intents (habilidades locales)
    intent = detectar_intent(texto_usuario)
    if intent:
        resultado_habilidad = intent.ejecutar()
        # Agrega al historial que el usuario pidió algo y ASIRU lo hizo
        _historial.append({"role": "user", "content": texto_usuario})
        _historial.append({"role": "assistant", "content": resultado_habilidad})
        return resultado_habilidad

    # Fase 2: No hay intent, manda a Llama2
    cliente = _cargar_cliente()
    _historial.append({"role": "user", "content": texto_usuario})

    # Construye el prompt con historial y personalidad
    prompt_con_historial = PERSONALIDAD + "\n\n"
    for msg in _historial:
        rol = "Usuario" if msg["role"] == "user" else "ASIRU"
        prompt_con_historial += f"{rol}: {msg['content']}\n"
    
    prompt_con_historial += "ASIRU: "

    try:
        respuesta = cliente.generate(
            model=MODELO,
            prompt=prompt_con_historial,
            stream=False,
        )
        texto_respuesta = respuesta["response"].strip()
    except Exception as e:
        raise RuntimeError(
            f"Error al llamar a Llama2: {e}\n"
            f"¿Está Ollama corriendo? Ejecuta en otra terminal: ollama run {MODELO}"
        )

    _historial.append({"role": "assistant", "content": texto_respuesta})
    return texto_respuesta


def reiniciar_historial():
    """Borra la memoria de la conversacion actual (para empezar de cero)."""
    global _historial
    _historial = []


if __name__ == "__main__":
    # Prueba rapida en modo texto, sin pasar por voz
    print("ASIRU (modo texto, Llama2 — Ctrl+C para salir)\n")
    try:
        while True:
            entrada = input("Tu: ")
            respuesta = pensar(entrada)
            print(f"ASIRU: {respuesta}\n")
    except KeyboardInterrupt:
        print("\nHasta luego.")
    except ConnectionError as e:
        print(f"\n[ERROR] {e}")
    except RuntimeError as e:
        print(f"\n[ERROR] {e}")
