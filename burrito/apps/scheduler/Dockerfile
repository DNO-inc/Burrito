FROM ghcr.io/dno-inc/burrito:main

COPY ./event_init.sql event_init.sql

CMD ["python", "-m", "burrito.apps.scheduler"]
