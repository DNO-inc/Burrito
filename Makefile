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

rmi:
	scripts/docker_rm_all_images.sh

db_conn:
	scripts/connect_to_db.sh

redis_conn:
	scripts/connect_to_redis.sh

burrito_cluster_ping:
	$(PYTHON) scripts/burrito_cluster_ping.py

burrito_cluster_run:
	scripts/burrito_cluster_run.sh

burrito_cluster_ps:
	$(PYTHON) scripts/burrito_cluster_ps.py

changelog:
	scripts/generate_changelog.sh

prepare_db:
	$(PYTHON) scripts/prepare_db.py
