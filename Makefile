docker-run:
	docker-compose up --build

poetry-install:
	poetry install

local-run:
	poetry run python -m src.main
