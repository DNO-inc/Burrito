FROM ghcr.io/dno-inc/burrito:document_db_test

COPY ./event_init.sql event_init.sql

CMD ["python", "-m", "burrito.apps.scheduler"]
