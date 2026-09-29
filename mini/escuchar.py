"""
escuchar.py - Modulo de reconocimiento de voz para ASIRU (Fase 1)

Graba audio del microfono y lo transcribe a texto usando Whisper,
corriendo 100% local (no manda tu voz a ningun servidor).
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# "tiny" = mas rapido, menos preciso. "base" = buen balance. "small" = mas preciso, mas lento.
MODELO = "base"
IDIOMA = "es"
SAMPLE_RATE = 16000  # Whisper espera audio a 16kHz

_modelo_whisper = None


def _cargar_modelo():
    """Carga el modelo de Whisper una sola vez y lo reutiliza (cargarlo es lento)."""
    global _modelo_whisper
    if _modelo_whisper is None:
        print("[ASIRU] Cargando modelo de voz... (la primera vez descarga el modelo, tarda mas)")
        _modelo_whisper = WhisperModel(MODELO, device="cpu", compute_type="int8")
        print("[ASIRU] Modelo listo.")
    return _modelo_whisper


def grabar_audio(duracion=5):
    """Graba audio del microfono durante 'duracion' segundos y lo devuelve como array."""
    print(f"Escuchando... (habla ahora, {duracion}s)")
    audio = sd.rec(int(duracion * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()  # bloquea hasta que termine de grabar
    return audio.flatten()


def transcribir(audio):
    """Convierte un array de audio (numpy) en texto."""
    modelo = _cargar_modelo()
    segmentos, _ = modelo.transcribe(audio, language=IDIOMA)
    texto = " ".join(segmento.text for segmento in segmentos).strip()
    return texto


def transcribir_archivo(ruta_wav):
    """Convierte un archivo .wav en texto. Util para probar sin microfono."""
    modelo = _cargar_modelo()
    segmentos, _ = modelo.transcribe(ruta_wav, language=IDIOMA)
    texto = " ".join(segmento.text for segmento in segmentos).strip()
    return texto


def escuchar_y_transcribir(duracion=5):
    """Funcion principal de esta fase: graba del microfono y devuelve el texto."""
    audio = grabar_audio(duracion)
    return transcribir(audio)


if __name__ == "__main__":
    # Prueba rapida: graba 5 segundos y muestra que entendio ASIRU
    texto = escuchar_y_transcribir()
    print(f"Entendi: {texto}")
