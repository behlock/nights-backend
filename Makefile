.PHONY: run \
		lint \
		test \

install:
	poetry install

run-service:
	poetry run python -m nightsservice

retrieve-nights:
	poetry run python -m nightsretrieval

lint:
	bin/run-black.sh && \
	bin/run-flake8.sh && \
	bin/run-mypy.sh

test:
	poetry run pytest tests
