DOCKER_COMPOSE := deploy/docker-compose.yml
DOCKER_ENV := deploy/.env
DOCKER_COMPOSE_RUNNER := docker compose
ifneq ($(ENV),)
	DOCKER_COMPOSE := deploy/dev.docker-compose.yml
	DOCKER_ENV := deploy/.env.dev
	DOCKER_COMPOSE_RUNNER := docker compose
	include deploy/.env.dev
	export $(shell sed 's/=.*//' deploy/.env.dev)
endif


.PHONY: run-backend
run-backend:
	poetry run gunicorn search_by_document_texts.presentation.api.main:app --reload -b $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level $(LOG_LEVEL)

.PHONY: migrate-create
migrate-create:
	poetry run alembic -c search_by_document_texts/config/alembic.ini revision --autogenerate

.PHONY: migrate-up
migrate-up:
	poetry run alembic -c search_by_document_texts/config/alembic.ini upgrade head

.PHONY: es-create-indexs
es-create-indexs:
	poetry run python -m search_by_document_texts.presentation.cli.create_es_indexs

.PHONY: dump_data
dump_data:
	poetry run python -m search_by_document_texts.presentation.cli.dump_data

.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up

.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) build

.PHONY: compose-pull
compose-pull:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) pull

.PHONY: compose-down
compose-down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) down

.PHONY: compose-logs
compose-logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) logs -f