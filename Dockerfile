FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# Install system dependencies required for Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean

# Install Poetry using pip (you can also use the official install script if preferred)
RUN pip install poetry

# Copy only the requirements and poetry.lock files to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install the project dependencies
RUN poetry install --no-root --no-dev

# Copy the entire project code into the container
COPY . /app

ENV PYTHONPATH=/app/src:/app/.venv/lib/python3.10/site-packages

EXPOSE 5002

# Set the entrypoint command
ENTRYPOINT ["python", "-m", "nightsservice"]
