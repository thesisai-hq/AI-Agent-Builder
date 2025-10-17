# Agent Builder - Docker Commands

# Detect Docker Compose command
COMPOSE := $(shell command -v docker-compose 2> /dev/null)
ifndef COMPOSE
    COMPOSE := docker compose
endif

.PHONY: help

help:
	@echo "Agent Builder - Docker Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Basic Commands
start: ## Start PostgreSQL database
	@echo "🐘 Starting database..."
	$(COMPOSE) down --remove-orphans || true
	$(COMPOSE) up -d postgres
	@echo "⏳ Waiting for database..."
	@sleep 5
	@echo "✅ Database started!"
	@echo "   Connection: postgresql://agent_user:agent_password@localhost:5432/agentbuilder"

stop: ## Stop database
	$(COMPOSE) down

restart: ## Restart database
	$(COMPOSE) restart postgres

logs: ## View database logs
	$(COMPOSE) logs -f postgres

shell: ## Open PostgreSQL shell
	docker exec -it agentbuilder_db psql -U agent_user -d agentbuilder

status: ## Check status
	$(COMPOSE) ps

# Advanced
clean: ## Remove containers (keeps data)
	$(COMPOSE) down --remove-orphans

clean-all: ## Remove everything including data
	$(COMPOSE) down -v --remove-orphans
	@echo "⚠️  All data deleted!"

reset: ## Complete reset
	$(COMPOSE) down -v --remove-orphans
	$(COMPOSE) up -d postgres
	@sleep 10
	@echo "✅ Database reset complete"

# Database Operations  
test: ## Test database connection
	docker exec agentbuilder_db psql -U agent_user -d agentbuilder -c "SELECT 'OK' as status;"

seed: ## Load mock data
	docker exec -i agentbuilder_db psql -U agent_user -d agentbuilder < database/mock_data.sql
	@echo "✅ Data loaded"

backup: ## Backup database
	@mkdir -p backups
	docker exec agentbuilder_db pg_dump -U agent_user agentbuilder > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/"

restore: ## Restore from backup (usage: make restore FILE=backups/backup.sql)
	docker exec -i agentbuilder_db psql -U agent_user -d agentbuilder < $(FILE)
	@echo "✅ Restored from $(FILE)"

# Tools
admin: ## Start pgAdmin
	$(COMPOSE) --profile tools up -d
	@echo "✅ pgAdmin: http://localhost:5050"
	@echo "   Email: admin@agentbuilder.com"
	@echo "   Password: admin"

admin-stop: ## Stop pgAdmin
	$(COMPOSE) --profile tools down
