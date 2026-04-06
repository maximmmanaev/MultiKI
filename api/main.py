from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="MultiKI API")

# Конфиг из окружения
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")


# ─── Модели данных ─────────────────────────────────────────────
class TaskInput(BaseModel):
    text: str


class TaskClassification(BaseModel):
    category: str
    priority: str
    pillar: str
    subtasks: list[str] = []
    reasoning: str = ""


# ─── Системный промпт для классификации ────────────────────────
SYSTEM_PROMPT = """Ты — Parser Agent системы MultiKI.
Классифицируй задачу и верни ТОЛЬКО валидный JSON без пояснений и markdown.
Схема: {"category": "str", "priority": "str", "pillar": "str", "subtasks": ["str"], "reasoning": "str"}"""


# ─── Эндпоинт: классификация задачи ────────────────────────────
@app.post("/api/classify", response_model=TaskClassification)
async def classify_task(task: TaskInput):
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"{SYSTEM_PROMPT}\n\nЗадача: {task.text}",
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=90
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()

        # Убираем markdown-обёртку, если модель её добавит
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:].strip()

        return TaskClassification.model_validate_json(raw)
    except Exception as e:
        logger.error(f"❌ Classification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── Эндпоинт: чат с нейросетью ────────────────────────────────
@app.post("/api/chat")
async def chat(message: dict):
    prompt = message.get("text", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Пустое сообщение")
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=120
        )
        resp.raise_for_status()
        return {"response": resp.json().get("response", "").strip()}
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ollama error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Health check ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "service": "multiki_api"}