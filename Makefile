.PHONY: run \
		lint \
		test \

install:
	poetry install

run:
	poetry run python -m nightsservice

lint:
	bin/run-black.sh && \
	bin/run-flake8.sh && \
	bin/run-mypy.sh

test:
	poetry run pytest tests
