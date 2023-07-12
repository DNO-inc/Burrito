FROM python:3.10-slim-buster as burrito-build-base

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/pysetup/.venv/bin:$PATH"

RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential

WORKDIR /opt/pysetup

RUN pip3 install poetry

COPY pyproject.toml ./

RUN poetry install --only main


FROM python:3.10-slim-buster

ENV PATH="/opt/pysetup/.venv/bin:$PATH"

COPY --from=burrito-build-base /opt/pysetup/ /opt/pysetup/
COPY ./preprocessor_config.json /preprocessor_config.json
COPY ./CONTRIBUTORS.md /CONTRIBUTORS.md
COPY ./CHANGELOG.md /CHANGELOG.md
COPY ./burrito /burrito

WORKDIR ./

CMD ["python", "-m", "burrito.apps.comments"]