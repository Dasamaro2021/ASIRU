# MODELOS.md — Cambiar el LLM de ASIRU

Por defecto, ASIRU usa **Ollama/Llama2** (100% local, gratis).

Este archivo explica cómo cambiar a otros LLMs.

## Opción 1: Claude (Anthropic) — recomendado para calidad

**Ventajas:**
- Mejor calidad de respuestas
- Más rápido que Llama2
- Soporta mejor razonamiento complejo

**Desventajas:**
- Cuesta dinero (pago por uso, muy barato)
- Requiere API key
- Necesita internet

### Cambiar a Claude

1. **Instalar SDK:**
   ```bash
   pip install anthropic
   ```

2. **Crear cuenta y obtener API key:**
   - Ve a [platform.claude.com](https://platform.claude.com)
   - Sign up (crear cuenta)
   - Settings → API keys → Create key
   - Copia la key (`sk-ant-...`)

3. **Editar `cerebro.py`** — reemplaza la sección de imports y configuración por:

   ```python
   from anthropic import Anthropic
   from intents import detectar_intent
   
   # Configuración de Claude
   MODELO = "claude-sonnet-5"  # o claude-opus-5 para más potencia
   
   PERSONALIDAD = """..."""  # igual que antes
   
   _cliente = None
   _historial = []
   
   
   def _cargar_cliente():
       """Crea el cliente de Anthropic una sola vez y lo reutiliza."""
       global _cliente
       if _cliente is None:
           import os
           api_key = os.environ.get("ANTHROPIC_API_KEY")
           if not api_key:
               raise ValueError(
                   "No encontre ANTHROPIC_API_KEY. "
                   "Copia .env.example a .env y pega ahi tu API key."
               )
           _cliente = Anthropic(api_key=api_key)
       return _cliente
   
   
   def pensar(texto_usuario):
       """Usa Claude para pensar."""
       # Fase 3: Detección de intents (igual que antes)
       intent = detectar_intent(texto_usuario)
       if intent:
           resultado_habilidad = intent.ejecutar()
           _historial.append({"role": "user", "content": texto_usuario})
           _historial.append({"role": "assistant", "content": resultado_habilidad})
           return resultado_habilidad
   
       # Fase 2: Manda a Claude
       cliente = _cargar_cliente()
       _historial.append({"role": "user", "content": texto_usuario})
   
       respuesta = cliente.messages.create(
           model=MODELO,
           max_tokens=300,
           system=PERSONALIDAD,
           messages=_historial,
       )
   
       texto_respuesta = respuesta.content[0].text
       _historial.append({"role": "assistant", "content": texto_respuesta})
       return texto_respuesta
   
   
   def reiniciar_historial():
       global _historial
       _historial = []
   ```

4. **Crear `.env` con tu API key:**
   ```bash
   cp .env.example .env
   ```
   Edita `.env` y pega:
   ```
   ANTHROPIC_API_KEY=sk-ant-tu-key-real
   ```

5. **Correr:**
   ```bash
   python main.py
   ```

---

## Opción 2: OpenAI (GPT) — buena calidad

**Ventajas:**
- Muy buena calidad
- Rápido
- Ampliamente disponible

**Desventajas:**
- Cuesta más que Claude
- Requiere API key
- Necesita internet

### Cambiar a OpenAI

1. **Instalar SDK:**
   ```bash
   pip install openai
   ```

2. **Obtener API key:**
   - Ve a [platform.openai.com](https://platform.openai.com)
   - API keys → Create new secret key
   - Copia la key

3. **Editar `cerebro.py`:**

   ```python
   from openai import OpenAI
   from intents import detectar_intent
   
   MODELO = "gpt-4"  # o "gpt-3.5-turbo" para más barato
   
   PERSONALIDAD = """..."""  # igual que antes
   
   _cliente = None
   _historial = []
   
   
   def _cargar_cliente():
       import os
       global _cliente
       if _cliente is None:
           api_key = os.environ.get("OPENAI_API_KEY")
           if not api_key:
               raise ValueError("No encontre OPENAI_API_KEY en .env")
           _cliente = OpenAI(api_key=api_key)
       return _cliente
   
   
   def pensar(texto_usuario):
       # Intents (igual que antes)
       intent = detectar_intent(texto_usuario)
       if intent:
           resultado_habilidad = intent.ejecutar()
           _historial.append({"role": "user", "content": texto_usuario})
           _historial.append({"role": "assistant", "content": resultado_habilidad})
           return resultado_habilidad
   
       # OpenAI
       cliente = _cargar_cliente()
       _historial.append({"role": "user", "content": texto_usuario})
   
       respuesta = cliente.chat.completions.create(
           model=MODELO,
           messages=[
               {"role": "system", "content": PERSONALIDAD},
               *_historial,
           ],
       )
   
       texto_respuesta = respuesta.choices[0].message.content
       _historial.append({"role": "assistant", "content": texto_respuesta})
       return texto_respuesta
   
   
   def reiniciar_historial():
       global _historial
       _historial = []
   ```

4. **Configurar .env:**
   ```bash
   cp .env.example .env
   ```
   Edita y pega:
   ```
   OPENAI_API_KEY=sk-proj-tu-key-real
   ```

---

## Opción 3: Groq (Llama 3.1 rápido) — buena relación calidad/velocidad

**Ventajas:**
- MUY rápido
- Gratis (con rate limits generosos)
- Buena calidad para Llama 3.1
- No requiere instalar nada local

**Desventajas:**
- Requiere API key (gratis pero con límites)
- Necesita internet

### Cambiar a Groq

1. **Obtener API key:**
   - Ve a [console.groq.com](https://console.groq.com)
   - Sign up (gratis)
   - API Keys → Create key
   - Copia la key

2. **Instalar SDK (usa openai compatible):**
   ```bash
   pip install openai  # Groq usa el SDK de OpenAI
   ```

3. **Editar `cerebro.py`:**

   ```python
   from openai import OpenAI
   from intents import detectar_intent
   
   MODELO = "llama-3.1-70b-versatile"
   
   PERSONALIDAD = """..."""  # igual que antes
   
   _cliente = None
   _historial = []
   
   
   def _cargar_cliente():
       import os
       global _cliente
       if _cliente is None:
           api_key = os.environ.get("GROQ_API_KEY")
           if not api_key:
               raise ValueError("No encontre GROQ_API_KEY en .env")
           _cliente = OpenAI(
               api_key=api_key,
               base_url="https://api.groq.com/openai/v1"
           )
       return _cliente
   
   
   def pensar(texto_usuario):
       # Intents (igual que antes)
       intent = detectar_intent(texto_usuario)
       if intent:
           resultado_habilidad = intent.ejecutar()
           _historial.append({"role": "user", "content": texto_usuario})
           _historial.append({"role": "assistant", "content": resultado_habilidad})
           return resultado_habilidad
   
       # Groq
       cliente = _cargar_cliente()
       _historial.append({"role": "user", "content": texto_usuario})
   
       respuesta = cliente.chat.completions.create(
           model=MODELO,
           messages=[
               {"role": "system", "content": PERSONALIDAD},
               *_historial,
           ],
       )
   
       texto_respuesta = respuesta.choices[0].message.content
       _historial.append({"role": "assistant", "content": texto_respuesta})
       return texto_respuesta
   
   
   def reiniciar_historial():
       global _historial
       _historial = []
   ```

4. **Configurar .env:**
   ```
   GROQ_API_KEY=gsk_tu-key-real
   ```

---

## Opción 4: Ollama + otro modelo local — como ahora pero distinto modelo

Ahora tienes `ollama run llama2`.

Para cambiar a otro modelo:

1. **Descargar el modelo:**
   ```bash
   ollama pull mistral      # Mistral, mejor que Llama2
   ollama pull neural-chat  # Más rápido
   ollama pull orca2        # Más capaz que Llama2
   ```

2. **Editar `cerebro.py`:**
   ```python
   MODELO = "mistral"  # Cambia este
   ```

3. **Correr:**
   ```bash
   # Terminal 1:
   ollama run mistral
   
   # Terminal 2:
   python main.py
   ```

---

## Comparación rápida

| Modelo | Costo | Velocidad | Calidad | Local | Config |
|--------|-------|-----------|---------|-------|--------|
| Llama2 (Ollama) | Gratis | Lento | Media | Sí | Fácil |
| Mistral (Ollama) | Gratis | Normal | Buena | Sí | Fácil |
| Claude | $ | Rápido | Excelente | No | Fácil |
| GPT-4 | $$ | Rápido | Excelente | No | Fácil |
| Groq/Llama3.1 | Gratis | MUY rápido | Buena | No | Fácil |

---

## Para volver a Ollama/Llama2

Si cambias a otro modelo y quieres volver a Ollama, revierte el archivo `cerebro.py` a la versión que te di — está guardada en `/mnt/user-data/outputs/asiru/cerebro.py`.

O copia la sección inicial de nuevo:
```python
from ollama import Client as OllamaClient
from intents import detectar_intent

OLLAMA_HOST = "http://localhost:11434"
MODELO = "llama2"
```

---

## Notas finales

- **La Fase 3 (intents) funciona igual** con cualquier LLM — no cambia nada.
- **La Fase 1 (voz)** es independiente — Whisper sigue igual.
- **Main.py no necesita cambios** — solo edita `cerebro.py`.

Si tienes dudas de cómo cambiar, pregunta y te ayudo con el código exacto.
