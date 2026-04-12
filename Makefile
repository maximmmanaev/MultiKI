.PHONY: up down logs check

up:
	@echo "🚀 Запуск MultiKI..."
	@docker compose  up -d

down:
	@echo "🛑 Остановка..."
	@docker compose  down

logs:
	@docker compose  logs -f --tail=50

check:
	@docker compose  ps

# === UPDATE ===
# Обновление из репозитория + перезапуск изменённых сервисов
# Фронтенд — статика, Nginx подхватит файлы сразу после перезагрузки
.PHONY: update
update:
	@git pull origin master
	@echo "🔄 Пересборка сервисов (api, parser-agent, planner-agent)..."
	@docker compose  up -d --build api parser-agent planner-agent
	@echo "🔄 Обновление статики фронтенда..."
	@docker compose  exec nginx nginx -s reload 2>/dev/null || true
	@echo "✅ Update complete. Stack running."
