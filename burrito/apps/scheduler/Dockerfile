ARG PROJECT_BRANCH=main

FROM ghcr.io/dno-inc/burrito:${PROJECT_BRANCH}

COPY ./event_init.sql event_init.sql

CMD ["python", "-m", "burrito.apps.scheduler"]
