"""
habilidades.py - Funciones que ASIRU puede ejecutar localmente (Fase 3)

Hora, calculadora, recordatorios, etc. Sin dependencias externas.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Base de datos de recordatorios
DB_PATH = "asiru_recordatorios.db"


def _init_db():
    """Crea la tabla de recordatorios si no existe."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS recordatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            fecha_creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


_init_db()


# --- Hora y fecha ---


def obtener_hora():
    """Devuelve la hora actual en formato legible."""
    return datetime.now().strftime("%H:%M")


def obtener_fecha():
    """Devuelve la fecha actual en formato legible."""
    hoy = datetime.now()
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    dia_semana = dias[hoy.weekday()]
    mes = meses[hoy.month - 1]
    return f"{dia_semana} {hoy.day} de {mes} de {hoy.year}"


# --- Calculadora ---


def calcular(expresion):
    """Evalúa una expresión matemática simple de forma segura.
    Ej: "2 + 2", "raiz cuadrada de 16", "5 * 3 + 2"
    """
    # Reemplaza palabras por operadores (para interpretar español)
    expr = expresion.lower()
    expr = expr.replace("mas", "+")
    expr = expr.replace("menos", "-")
    expr = expr.replace("multiplicado por", "*")
    expr = expr.replace("por", "*")
    expr = expr.replace("dividido entre", "/")
    expr = expr.replace("entre", "/")
    expr = expr.replace("raiz cuadrada de", "sqrt")
    expr = expr.replace("potencia", "**")
    expr = expr.replace("^", "**")

    # Importa sqrt y limpia espacios
    from math import sqrt
    expr = expr.replace(" ", "")

    try:
        resultado = eval(expr, {"sqrt": sqrt, "__builtins__": {}})
        return f"El resultado es: {resultado}"
    except Exception as e:
        return f"No pude calcular eso. Error: {e}"


# --- Recordatorios ---


def agregar_recordatorio(texto):
    """Guarda un nuevo recordatorio."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO recordatorios (texto) VALUES (?)", (texto,))
    conn.commit()
    conn.close()
    return f"Recordatorio guardado: {texto}"


def listar_recordatorios():
    """Lista todos los recordatorios guardados."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, texto FROM recordatorios ORDER BY id DESC")
    registros = c.fetchall()
    conn.close()

    if not registros:
        return "No hay recordatorios guardados."

    respuesta = "Tus recordatorios:\n"
    for rid, texto in registros:
        respuesta += f"  {rid}. {texto}\n"
    return respuesta.strip()


def borrar_recordatorio(id_recordatorio):
    """Borra un recordatorio por ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM recordatorios WHERE id = ?", (id_recordatorio,))
    conn.commit()
    borrados = c.rowcount
    conn.close()

    if borrados > 0:
        return f"Recordatorio {id_recordatorio} eliminado."
    else:
        return f"No encontré el recordatorio {id_recordatorio}."


# --- Exposición de todas las habilidades ---


HABILIDADES = {
    "hora": obtener_hora,
    "fecha": obtener_fecha,
    "calcular": calcular,
    "recordar": agregar_recordatorio,
    "recordatorios": listar_recordatorios,
    "borrar_recordatorio": borrar_recordatorio,
}


if __name__ == "__main__":
    print("Probando habilidades:")
    print(f"Hora: {obtener_hora()}")
    print(f"Fecha: {obtener_fecha()}")
    print(f"Cálculo: {calcular('2+2')}")
    print(f"Recordar: {agregar_recordatorio('Probar fase 3')}")
    print(f"Listado: {listar_recordatorios()}")
