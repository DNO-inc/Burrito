FROM ghcr.io/dno-inc/burrito-dependencies:document_db_test AS burrito-dependencies

FROM python:3.10-slim-buster

ENV PATH="/venv/.venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app/burrito

COPY --from=burrito-dependencies /venv /venv
COPY --from=burrito-dependencies /certs /certs
COPY ./preprocessor_config.json preprocessor_config.json
COPY ./CONTRIBUTORS.md CONTRIBUTORS.md
COPY ./CHANGELOG.md CHANGELOG.md
COPY ./burrito ./

CMD ["python3", "-m", "burrito"]
