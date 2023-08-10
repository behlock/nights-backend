FROM duffn/python-poetry:3.10.7-slim AS builder

WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY src ./src

RUN poetry install

RUN ln -s /usr/bin/python3 /usr/bin/python

# TODO: Find way not to rely on cache
ENV PYTHONPATH=/app/src:/root/.cache/pypoetry/virtualenvs/nights-service-9TtSrW0h-py3.10/lib/python3.10/site-packages/

EXPOSE 5002

ENTRYPOINT python3 -m nightsservice
