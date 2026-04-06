import os
import time
import json
import logging
import requests
from pydantic import BaseModel, ValidationError
from typing import List

# ─── Логирование ─────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/parser.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ─── Конфиг из окружения ─────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

# ─── Pydantic-схема для строгой валидации ────────────────────
class TaskClassification(BaseModel):
    category: str          # WORK | LIFE | HEALTH | LEARNING
    priority: str          # LOW | MEDIUM | HIGH | URGENT
    pillar: str            # EARTH | WATER | AIR | FIRE
    subtasks: List[str] = []
    reasoning: str = ""

# ─── Системный промпт ────────────────────────────────────────
SYSTEM_PROMPT = """Ты — Parser Agent системы MultiKI.
Твоя задача: классифицировать входящую задачу и разбить её на подзадачи.
Верни ТОЛЬКО валидный JSON, соответствующий схеме. Без пояснений, без markdown.
Схема: {"category": "str", "priority": "str", "pillar": "str", "subtasks": ["str"], "reasoning": "str"}"""

def classify_task(task_text: str):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nЗадача: {task_text}",
        "stream": False,
        "options": {"temperature": 0.1}
    }

    try:
        resp = requests.post(url, json=payload, timeout=90)
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()

        # Убираем обёртку ```json ... ``` если модель её добавит
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:].strip()

        data = json.loads(raw)
        result = TaskClassification(**data)
        logger.info(f"✅ Успех: {result.model_dump_json(indent=2)}")
        return result

    except requests.RequestException as e:
        logger.error(f"❌ Сбой запроса к Ollama: {e}")
    except (json.JSONDecodeError, ValidationError, KeyError) as e:
        logger.error(f"❌ Ошибка валидации JSON: {e}")
        logger.error(f"📝 Сырой ответ: {raw}")
    return None

def main():
    logger.info("🚀 Parser Agent запущен. Тестовый запуск...")
    
    # Демо-тест при старте (потом заменим на очередь/HTTP)
    test_task = "Сделать дизайн письма про падение биткоина в Figma: обложка + вёрстка текста"
    classify_task(test_task)
    
    logger.info("💤 Агент в режиме ожидания (подключится к очереди задач позже)...")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
