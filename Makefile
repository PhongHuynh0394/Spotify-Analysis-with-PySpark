include .env

up:
	docker compose up -d

down:
	docker compose down

prefect-up:
	docker compose -f prefect-compose.yml up -d

prefect-down:
	docker compose -f prefect-compose.yml down

prefect-build:
	docker compose -f prefect-compose.yml build
