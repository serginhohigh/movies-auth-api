COMPOSE = docker compose
COMPOSE_FILE = docker-compose.yml
COMPOSE_FILE_DEV = docker-compose.dev.yml
COMPOSE_FILE_TEST = tests/functional/docker-compose.yml

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-11s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove python compiled cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

lint: ## Make lint with ruff
	ruff .

install: ## Prepare prod env
	cp .env.example .env
	cp ./auth/.env.example ./auth/.env
	cp ./tests/functional/.env.example ./tests/functional/.env

migrate: ## Upgrade database from alembic migrations
	docker exec -it auth flask db upgrade

up: ## UP prod containers
	${COMPOSE} up -d --build

stop: ## Stop prod container
	${COMPOSE} stop $(c) && ${COMPOSE} rm -f $(c)

down: ## Down prod containers
	${COMPOSE} down

dev-up: ## UP dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} up -d $(c) --build

dev-stop: ## Stop dev container
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} stop $(c) \
		&& ${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} rm -f $(c)

dev-down: ## Down dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} down

test: ## Run functional tests
	${COMPOSE} -f ${COMPOSE_FILE_TEST} up -d auth redis postgres --build; \
		sleep 5s; \
		docker exec -it test-auth flask db upgrade; \
		${COMPOSE} -f ${COMPOSE_FILE_TEST} run --rm --build \
		pytest bash -c 'python3 utils/wait_for_pg.py; python3 utils/wait_for_redis.py; pytest -vv -s'; \
		${COMPOSE} -f ${COMPOSE_FILE_TEST} down
