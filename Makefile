include .env
export

VENV_PATH = .venv

ifeq ("$(wildcard $(VENV_PATH))", "")
	PYTHON=$(shell which python3)
else
	PYTHON=$(VENV_PATH)/bin/python3
endif


run:
	$(PYTHON) -m burrito

docs_:
	doxygen docs.conf

clear_db: tests/utils/clear_db.py
	$(PYTHON) tests/utils/clear_db.py

tests_:
	$(PYTHON) tests/run_tests.py

docker_build: Dockerfile
	docker build -t burrito .

_delete_docker_container:
	docker rm burrito_love || true

docker_run: _delete_docker_container Dockerfile
	docker run --env-file .env --name burrito_love burrito

rmi:
	scripts/docker_rm_all_images.sh

db_conn:
	scripts/connect_to_db.sh
