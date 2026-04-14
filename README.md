# MultiKI Controller v0.2.1

Веб-интерфейс для управления персональной системой искусственного интеллекта.

## Требования

- Docker + Docker Compose v2+
- NVIDIA GPU + NVIDIA Container Toolkit (для Ollama)
- 16+ GB RAM, 16+ GB VRAM (рекомендуется)

## Быстрый старт

1. **Клонируй репозиторий:**
   ```bash
   git clone https://github.com/maximmmanaev/multiki.git
   cd multiki
   cp .env.example .env
   # Отредактируй .env, заменив значения на свои пароли
   make up
   # или вручную:
   docker compose --env-file .env up -d
Запусти сервисы:
🌐 Интерфейс: https://127.0.0.1
📊 Langfuse: http://127.0.0.1:3000
🔮 Qdrant UI: http://127.0.0.1:6333/dashboard
🕸 Neo4j Browser: http://127.0.0.1:7474
Основные команды
Команда	Описание
make up	Запустить все сервисы
make down	Остановить и удалить контейнеры
make update	Git pull + rebuild API + reload
make logs	Показать логи всех сервисов
Переменные окружения
Смотри .env.example для полного списка параметров.

⚠️ Важно: Никогда не коммить .env с реальными паролями!

Устранение неполадок
Проблема	Решение
502 Bad Gateway	Проверь docker compose ps, API должен быть Up (healthy)
Langfuse Authentication failed	Синхронизируй POSTGRES_PASSWORD и DATABASE_URL в .env
Ollama не отвечает	Убедись, что OLLAMA_BASE_URL указывает на хост с запущенным Ollama
VRAM = 0	Проверь, что nvidia-smi работает на хосте, и контейнер имеет доступ к GPU
Структура проекта
Code
multiki/
├── api/                 # FastAPI бэкенд
├── frontend/            # Статический веб-интерфейс
├── nginx/               # Конфигурация прокси + SSL
├── docker-compose.yml   # Оркестрация сервисов
├── Makefile            # Удобные команды
├── .env.example        # Шаблон переменных окружения
└── README.md           # Этот файл
