"""
hablar.py - Modulo de sintesis de voz para ASIRU (Fase 1)

Convierte texto en audio hablado usando el motor TTS del sistema
(espeak-ng en Linux). 100% offline, sin API key.
"""

import pyttsx3

_motor = None


def _cargar_motor():
    global _motor
    if _motor is None:
        _motor = pyttsx3.init()
        _motor.setProperty("rate", 175)   # velocidad de habla (palabras/min aprox)
        _motor.setProperty("volume", 1.0)
    return _motor


def hablar(texto):
    """Convierte texto en voz y lo reproduce por el altavoz."""
    motor = _cargar_motor()
    print(f"ASIRU: {texto}")
    motor.say(texto)
    motor.runAndWait()


def guardar_audio(texto, ruta_salida="salida.wav"):
    """Convierte texto en voz y lo guarda en un archivo, sin reproducirlo.
    Util para probar el motor de voz sin necesitar altavoces (ej. en un servidor)."""
    motor = _cargar_motor()
    motor.save_to_file(texto, ruta_salida)
    motor.runAndWait()
    return ruta_salida


if __name__ == "__main__":
    hablar("Hola, soy ASIRU. Sistema de voz activado correctamente.")
