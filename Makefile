include .env

up:
	docker compose -f prefect-compose.yml up -d

down:
	docker compose -f prefect-compose.yml down
