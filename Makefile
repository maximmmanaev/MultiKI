.PHONY: up down logs check

up:
	@echo "🚀 Запуск MultiKI..."
	@docker compose --env-file .env.secret up -d

down:
	@echo "🛑 Остановка..."
	@docker compose --env-file .env.secret down

logs:
	@docker compose --env-file .env.secret logs -f --tail=50

check:
	@docker compose --env-file .env.secret ps
