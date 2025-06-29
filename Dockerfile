ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-alpine AS burrito-build-base


FROM burrito-build-base AS burrito-dependencies

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apk update && \
    apk add --no-cache --no-interactive poetry cargo

WORKDIR /venv

COPY pyproject.toml ./

RUN poetry install --no-root --only main


FROM burrito-build-base AS burrito-runtime

ENV PATH="/venv/.venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

COPY --from=burrito-dependencies /venv /venv
COPY ./preprocessor_config.json preprocessor_config.json
COPY ./CONTRIBUTORS.md CONTRIBUTORS.md
COPY ./CHANGELOG.md CHANGELOG.md
COPY ./burrito ./burrito

CMD ["python3", "-m", "burrito"]
