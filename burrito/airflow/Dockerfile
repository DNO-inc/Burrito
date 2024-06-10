FROM python:3.10-slim-buster as build-base

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/pysetup/.venv/bin:$PATH"

RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential

WORKDIR /opt/pysetup

RUN pip3 install poetry

COPY pyproject.toml ./

RUN poetry install --only main

RUN apt -y install netcat iputils-ping

FROM apache/airflow:2.9.1-python3.10

ENV PATH="/opt/pysetup/.venv/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/opt/burrito_project"

RUN mkdir -p /opt/airflow/{config,dags,logs,plugins}

COPY --chown=airflow ./burrito/airflow /opt/airflow

COPY --from=build-base /opt/pysetup/ /opt/pysetup/
COPY ./preprocessor_config.json /opt/burrito_project/burrito/preprocessor_config.json
COPY ./CONTRIBUTORS.md /opt/burrito_project/burrito/CONTRIBUTORS.md
COPY ./CHANGELOG.md /opt/burrito_project/burrito/CHANGELOG.md
COPY ./burrito /opt/burrito_project/burrito
COPY ./event_init.sql /opt/burrito_project/burrito/event_init.sql

CMD []
