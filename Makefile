.PHONY: install run-service retrieve-nights-local retrieve-nights-prod retrieve-nights lint format typecheck test

install:
	poetry install

run-service:
	poetry run python -m nightsservice

retrieve-nights-local:
	poetry run python -m nightsretrieval --local

retrieve-nights-prod:
	poetry run python -m nightsretrieval --prod

retrieve-nights: retrieve-nights-local

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format src tests
	poetry run ruff check --fix src tests

typecheck:
	poetry run mypy src

test:
	poetry run pytest tests
