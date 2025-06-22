FROM ghcr.io/dno-inc/burrito-dependencies:main AS burrito-dependencies

FROM python:3.10-slim-buster

ENV PATH="/venv/.venv/bin:$PATH" \
    PYTHONPATH="/app:/venv/.venv/lib/python3.10/site-packages"

WORKDIR /app/burrito

COPY --from=burrito-dependencies /venv /venv
COPY ./preprocessor_config.json preprocessor_config.json
COPY ./CONTRIBUTORS.md CONTRIBUTORS.md
COPY ./CHANGELOG.md CHANGELOG.md
COPY ./burrito ./

CMD ["python3", "-m", "burrito"]
