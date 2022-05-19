.PHONY: help build push all

help:
	@echo "Makefile commands:"
	@echo "build - builds and starts the docker container"
	@echo "up - starts the docker container"
	@echo "ssh - SSH into the blogapp container"
	@echo "server - executes the django python manage.py runserver command inside the running blogapp container"
	@echo "down - stops the docker container"
	@echo "flake8 - runs flake8 linting on the app"
	@echo "test - runs your python tests"

build:
	@docker-compose build

up:
	@docker-compose up --detach
ssh:
	@docker-compose exec blogapp sh

server:
	@docker-compose exec blogapp python manage.py runserver 0.0.0.0:8000

down:
	@docker-compose down

flake8:
	@docker-compose exec blogapp flake8

test:
	@docker-compose exec blogapp python manage.py test
