.PHONY: run \
		lint \
		test \

run:
	poetry run python main.py ${FILE}

lint:
	bin/run-black.sh && \
	bin/run-flake8.sh && \
	bin/run-mypy.sh

test:
	poetry run pytest tests
