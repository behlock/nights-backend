FROM duffn/python-poetry:3.10.7-slim AS builder

# Set the working directory inside the container
WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# RUN poetry install --no-dev --no-root

COPY src ./src

# RUN poetry install --no-dev

RUN poetry install

# FROM duffn/python-poetry:3.10.7-slim AS runtime

# RUN apt-get -q update && \
#     apt-get install -qq \
#     --no-install-recommends \
#     --allow-downgrades \
#     openssl=1.1.1n-0+deb11u3  \
#     curl=7.74.0-1.3+deb11u3 \
#     libp11-kit0=0.23.22-1 \
#     libpq5=13.9-0+deb11u1 \
#     graphviz=2.42.2-5 \
#     liblz4-1=1.9.3-2 \
#     libexpat1=2.2.10-2+deb11u5  && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# WORKDIR /
# COPY --from=builder /app /app
# COPY bin ./

# ENV PYTHONPATH=/app/src:/app/.venv/lib/python3.10/site-packages
ENV PYTHONPATH=/app/src:/root/.cache/pypoetry/virtualenvs/nights-service-9TtSrW0h-py3.10/lib/python3.10/site-packages/


EXPOSE 5002

# Set the entrypoint command
ENTRYPOINT ["python3", "-m", "nightsservice"]
# CMD ["echo", "No command specified"]
