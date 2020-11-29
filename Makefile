APP_DOCKER_COMPOSE=docker-compose.yml


.PHONY: build
build:
	@docker-compose -f ${APP_DOCKER_COMPOSE} build

.PHONY: serve
serve:
	@docker-compose -f ${APP_DOCKER_COMPOSE} up --remove-orphans
