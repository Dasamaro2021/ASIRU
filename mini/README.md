# ASIRU — Fase 1 + Fase 2 + Fase 3: Voz, Cerebro y Habilidades

## Qué hace cada archivo

- `escuchar.py` — graba tu voz y la transcribe a texto (Whisper local)
- `hablar.py` — convierte texto en voz y lo reproduce (motor del sistema)
- `cerebro.py` — **Fase 2:** conecta con Llama2 (vía Ollama) para pensar y conversar, con memoria
- `habilidades.py` — **Fase 3:** hora, calculadora, recordatorios en SQLite
- `intents.py` — **Fase 3:** detector de intents — interpreta "qué hora es", "calcula 2+2", etc.
- `main.py` — une todo: escucha → detecta intents → piensa/ejecuta → responde por voz

Ahora ASIRU:
- Habla en español e entiende lo que dices (Fase 1)
- Piensa respuestas con criterio propio usando Llama2 (Fase 2)
- Hace cosas útiles al instante: hora, cálculos, recordatorios (Fase 3)

## Instalación

### 1. Dependencias del sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install espeak-ng portaudio19-dev
```

**Mac:** `brew install portaudio`

**Windows:** no necesitas nada extra (SAPI5 viene incluido).

### 2. Librerías de Python

```bash
pip install -r requirements.txt
```

### 3. Descargar e instalar Ollama + Llama2

1. Descarga [ollama.ai](https://ollama.ai)
2. Instala y abre (en Mac/Linux abre terminal; en Windows abre la app)
3. En terminal/consola, descarga Llama2:
   ```bash
   ollama run llama2
   ```
   Esto descarga ~4GB del modelo la primera vez (tarda 5-10 minutos).
   Cuando termine, verá un prompt `>>>` — puedes escribir ahí o presionar Ctrl+C para salir.
   **Ollama sigue corriendo de fondo** — eso es lo que ASIRU necesita.

## Uso

Abre **dos terminales**:

**Terminal 1: Mantener Ollama corriendo**
```bash
ollama serve
```
(O simplemente mantén Ollama abierto si estás en Mac/Windows)

**Terminal 2: Correr ASIRU**
```bash
python main.py
```

**Comandos que ASIRU entiende:**
- "qué hora es" → devuelve la hora al instante
- "cuál es la fecha" → devuelve la fecha
- "calcula 2 más 2" → resuelve matemáticas
- "recordar que debo..." → guarda un recordatorio
- "mis recordatorios" → muestra todos
- "borra recordatorio 1" → borra por ID
- (cualquier otra cosa) → pregunta a Llama2

Para salir: di "salir", "adiós" o "apágate".

## Cambiar a otro LLM

Por defecto usamos **Llama2 (Ollama)** — es local, gratis y funciona bien.

Si quieres cambiar a **Claude, OpenAI, Groq, o un modelo diferente de Ollama**, lee **`MODELOS.md`**.

Es muy fácil: solo cambiar 5-10 líneas en `cerebro.py` + crear un `.env` con una API key (si el modelo lo requiere).

## Fase 3: Habilidades locales

Los comandos simples (hora, calculadora, recordatorios) **NO pasan por Llama2**. Se ejecutan localmente al instante.

Esto es:
- **Rápido**: 1-10ms en vez de 1-3s
- **Gratis**: no consume recursos
- **Funciona offline**: no necesita internet

Nuevos comandos:
1. Agrega función en `habilidades.py`
2. Agrega palabra clave en `intents.py`
3. Listo

## Troubleshooting

- **"No puedo conectar a Ollama en http://localhost:11434"**
  → ¿Corriste `ollama run llama2` o `ollama serve`? Debe estar activo en otra terminal.

- **"OSError: No Default Input Device"**
  → Revisa permisos de micrófono del SO.

- **ASIRU responde muy largo**
  → En `cerebro.py`, reduce el prompt o cambia la personalidad.

- **Llama2 está muy lento**
  → Es normal. Llama2 es un modelo grande que corre localmente.
  → Opción: cambiar a **Mistral** (`ollama pull mistral`, más rápido).
  → O cambiar a **Groq/Claude** (vía API, mucho más rápido — ver `MODELOS.md`).

## Próximos pasos

- **Fase 4: Automatización** — controlar apps, ajustar volumen, etc.
- **Fase 5: Proactividad** — ASIRU te avisa antes de que preguntes
- **Fase 6: Integración externa** — clima, noticias, etc.

Diviértete. ASIRU es tu asistente.
