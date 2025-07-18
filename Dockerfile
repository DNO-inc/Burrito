ARG BASE_IMAGE_TAG=3.10-alpine
ARG CONTAINER_USER=nobody
ARG CONTAINER_GROUP=nobody
ARG DEPENDENCIES_DIR=/venv
ARG RUNTIME_WORKING_DIR=/app


FROM python:${BASE_IMAGE_TAG} AS burrito-build-base


FROM burrito-build-base AS burrito-dependencies
ARG DEPENDENCIES_DIR

RUN apk update && \
    apk add --no-cache --no-interactive \ 
        abseil-cpp-dev \
        build-base \
        cargo \
        poetry \
        py3-pybind11-dev \
        re2-dev

ENV POETRY_NO_INTERACTION=true \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml ./

RUN python -m venv ${DEPENDENCIES_DIR} && \
    source ${DEPENDENCIES_DIR}/bin/activate && \
    poetry install --no-root --only main


FROM burrito-build-base AS burrito-runtime
ARG CONTAINER_USER
ARG CONTAINER_GROUP
ARG DEPENDENCIES_DIR
ARG RUNTIME_WORKING_DIR

RUN getent group "${CONTAINER_GROUP}" >/dev/null 2>&1 || addgroup -S "${CONTAINER_GROUP}" && \
    id -u "${CONTAINER_USER}" >/dev/null 2>&1 || adduser -S "${CONTAINER_USER}" -G "${CONTAINER_GROUP}"

ENV PATH="${DEPENDENCIES_DIR}/bin:${PATH}" \
    PYTHONPATH=${RUNTIME_WORKING_DIR}

WORKDIR ${RUNTIME_WORKING_DIR}

COPY --from=burrito-dependencies --chown=${CONTAINER_USER}:${CONTAINER_GROUP} ${DEPENDENCIES_DIR} ${DEPENDENCIES_DIR}
COPY --chown=${CONTAINER_USER}:${CONTAINER_GROUP} ./preprocessor_config.json preprocessor_config.json
COPY --chown=${CONTAINER_USER}:${CONTAINER_GROUP} ./CONTRIBUTORS.md CONTRIBUTORS.md
COPY --chown=${CONTAINER_USER}:${CONTAINER_GROUP} ./CHANGELOG.md CHANGELOG.md
COPY --chown=${CONTAINER_USER}:${CONTAINER_GROUP} ./burrito ./burrito

USER ${CONTAINER_USER}:${CONTAINER_GROUP}

CMD ["python3", "-m", "burrito"]