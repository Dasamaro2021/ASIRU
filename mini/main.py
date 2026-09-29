"""
main.py - ASIRU Fase 2: escucha, piensa y responde

Escucha lo que dices, lo manda al cerebro (Claude) para que piense una
respuesta con criterio propio, y te la lee en voz alta.
"""

from escuchar import escuchar_y_transcribir
from hablar import hablar
from cerebro import pensar, reiniciar_historial

PALABRAS_SALIDA = {"salir", "adios", "adiós", "apagate", "apágate"}
PALABRAS_REINICIO = {"olvida todo", "empecemos de nuevo", "borra la memoria"}


def main():
    hablar("Hola, soy ASIRU. Ya puedo pensar, no solo repetir.")

    while True:
        texto = escuchar_y_transcribir(duracion=5)

        if not texto:
            hablar("No escuche nada, intenta de nuevo.")
            continue

        print(f"Tu dijiste: {texto}")
        texto_limpio = texto.lower().strip(".,!? ")

        if texto_limpio in PALABRAS_SALIDA:
            hablar("Hasta luego.")
            break

        if texto_limpio in PALABRAS_REINICIO:
            reiniciar_historial()
            hablar("Listo, empezamos de cero.")
            continue

        try:
            respuesta = pensar(texto)
        except ValueError as e:
            hablar("Me falta configurar mi cerebro. Revisa la consola.")
            print(f"[ERROR] {e}")
            continue

        hablar(respuesta)


if __name__ == "__main__":
    main()
