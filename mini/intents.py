"""
intents.py - Detector de intents para la Fase 3

Interpreta lo que el usuario quiere hacer sin necesidad de un LLM.
Basado en palabras clave simples — perfecto para modelos débiles como Llama2.
"""

import re
from habilidades import HABILIDADES


class Intent:
    """Representa un intent detectado: qué hacer y con qué parámetros."""

    def __init__(self, nombre, funcion, parametro=None):
        self.nombre = nombre
        self.funcion = funcion
        self.parametro = parametro

    def ejecutar(self):
        """Ejecuta la función del intent con su parámetro si lo tiene."""
        if self.parametro is not None:
            return self.funcion(self.parametro)
        else:
            return self.funcion()


def detectar_intent(texto):
    """Analiza el texto y devuelve un Intent si lo encuentra, sino None.
    
    Palabras clave buscadas:
    - "qué hora" / "hora" -> obtener_hora
    - "qué fecha" / "hoy" -> obtener_fecha
    - "calcul" (calcular/calcula) -> calcular
    - "recordar" / "recuerda" -> agregar_recordatorio
    - "mis recordatorios" / "lista de recordatorios" -> listar_recordatorios
    - "borrar recordatorio" / "elimina" -> borrar_recordatorio
    """
    texto_lower = texto.lower().strip(".,!? ")

    # Hora
    if any(kw in texto_lower for kw in ["qué hora", "que hora", "hora es", "horario"]):
        return Intent("hora", HABILIDADES["hora"])

    # Fecha
    if any(kw in texto_lower for kw in ["qué fecha", "que fecha", "hoy", "día de hoy"]):
        return Intent("fecha", HABILIDADES["fecha"])

    # Calculadora
    if re.search(r"(calcul|cuánto|cuanto|es\s+[\d+\-*/\s]|[\d+\-*/\s]+[\?])", texto_lower):
        # Extrae la expresión matemática después de "es " o directamente los números
        expr = None
        if " es " in texto_lower:
            expr = texto_lower.split(" es ", 1)[-1]
        else:
            # Busca la secuencia de números y operadores más larga
            expr = re.search(r"[\d+\-*/().\s]+", texto_lower)
            if expr:
                expr = expr.group(0)
        
        if expr:
            parametro = expr.strip()
            return Intent("calcular", HABILIDADES["calcular"], parametro)

    # Recordatorios - listar
    if any(kw in texto_lower for kw in [
        "mis recordatorios", "lista de recordatorios", "qué recordatorios",
        "que recordatorios", "cuáles son", "cuales son mis", "muéstrame",
        "muestrame", "listar recordatorios"
    ]):
        return Intent("recordatorios", HABILIDADES["recordatorios"])

    # Recordatorios - agregar
    if any(kw in texto_lower for kw in ["recordar", "recuerda", "anota", "nota que"]):
        # Extrae lo que sigue a "recordar que" o similar
        # Busca el texto después de estas palabras clave
        for kw in ["recordar que", "recuerda que", "anota que", "nota que"]:
            if kw in texto_lower:
                parametro = texto_lower.split(kw, 1)[-1].strip()
                if parametro:
                    return Intent("recordar", HABILIDADES["recordar"], parametro)

        # Si no hay "que" explícito, toma todo lo después de "recordar"
        if "recordar " in texto_lower:
            parametro = texto_lower.split("recordar ", 1)[-1].strip()
            return Intent("recordar", HABILIDADES["recordar"], parametro)

    # Recordatorios - borrar
    if any(kw in texto_lower for kw in ["borrar recordatorio", "borra recordatorio", "elimina recordatorio", "borra nota"]):
        # Busca un número después de "recordatorio"
        match = re.search(r"(recordatorio|nota)\s+(\d+)", texto_lower)
        if match:
            numero = match.group(2)
            return Intent("borrar_recordatorio", HABILIDADES["borrar_recordatorio"], int(numero))

    # No se detectó intent
    return None


if __name__ == "__main__":
    # Pruebas rápidas
    pruebas = [
        "qué hora es",
        "dime la fecha de hoy",
        "calcula 2 más 2",
        "cuánto es 10 * 5",
        "recordar que debo llamar a mamá",
        "mis recordatorios",
        "lista de recordatorios",
        "borra recordatorio 1",
        "hola",  # Sin intent detectado
    ]

    for prueba in pruebas:
        intent = detectar_intent(prueba)
        print(f"'{prueba}'")
        if intent:
            print(f"  → {intent.nombre}: {intent.ejecutar()}")
        else:
            print(f"  → Sin intent detectado, ir al LLM")
        print()
