.PHONY : help clean lint

TESTS_F_COMPOSE = tests/functional/docker-compose.yml
TESTS_F_COMPOSE_DEV = tests/functional/docker-compose.dev.yml

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-11s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-docker: ## Create docker networks, volumes etc
	docker network create nginx
	docker network create auth
	docker network create redis
	docker volume create --name auth_redis
	docker volume create --name auth_pgdata

install: install-docker ## Prepare prod env
	cp .env.example .env
	cp ./auth/.env.example ./auth/.env
	cp ./tests/functional/.env.example ./tests/functional/.env

clean: ## Remove python compiled cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

lint: ## Make lint with ruff
	ruff check .

contrib: install-docker ## Development stuff
	pip install -r development/requirements.txt
	cp .env.example .env
	cp ./auth/.env.example ./auth/.env
	cp ./auth/.env.example ./development/.env
	cp ./tests/functional/.env.example ./tests/functional/.env

.ONESHELL:
flask: ## FLASK CLI
	@(
			while read line; do
					if test $$line; then
							export $$line
					fi
			done < ./development/.env
			cd ./auth/src/
			flask $(command)
	)

build: ## Build prod containers
	docker compose --profile prod build $(c)

run: build ## Run prod docker env
	docker compose --profile prod up -d $(c)

migrate: ## Upgrade database from alembic migrations
	@bash -c ' \
		docker exec -it auth flask db upgrade'

stop: ## Stop prod container
	docker compose --profile prod stop $(c)
	docker compose --profile prod rm -f $(c)

down: ## Shutdown prod docker env
	docker compose --profile prod down

logs: ## Logs on prod env
	docker compose --profile prod logs -f $(c)

dev-logs: ## Logs on dev env
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml logs -f $(c)

dev-build: ## Build dev docker env
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml build $(c)

dev-run: dev-build ## Run dev docker env
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml up -d $(c)

dev-stop: ## Stop dev docker env
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml stop $(c)
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml rm -f $(c)

dev-down: ## Shutdown dev docker env
	docker compose --profile dev -f docker-compose.yml -f docker-compose.dev.yml down

test: test-run ## Run tests from ./tests/functional in docker env
	@bash -c ' \
		docker exec -it test-auth flask db upgrade; \
		docker compose -f $(TESTS_F_COMPOSE) run --rm pytest bash -c \
			"python3 utils/wait_for_pg.py && python3 utils/wait_for_redis.py && pytest"; \
			docker compose -f $(TESTS_F_COMPOSE) down'

test-run: test-build ## Up ./tests/functional docker env
	docker compose -f $(TESTS_F_COMPOSE) up -d auth redis postgres

test-build: ## Build ./tests/functional docker env
	docker compose -f $(TESTS_F_COMPOSE) build

test-down: ## Down ./tests/functional docker env
	docker compose -f $(TESTS_F_COMPOSE) down

.ONESHELL:
test-dev: test-dev-run ## Run ./tests/functional locally like dev
	docker exec -it test-auth flask db upgrade
	pytest -s -vv

test-dev-run: test-dev-build ## Up ./tests/functional dev docker env
	docker compose -f $(TESTS_F_COMPOSE) \
		-f $(TESTS_F_COMPOSE_DEV) up -d auth redis postgres

test-dev-build: ## Build ./tests/functional dev docker env
	docker compose -f $(TESTS_F_COMPOSE) \
		-f $(TESTS_F_COMPOSE_DEV) build

test-dev-down: ## Down ./tests/functional dev docker env
	docker compose -f $(TESTS_F_COMPOSE) \
		-f $(TESTS_F_COMPOSE_DEV) down
