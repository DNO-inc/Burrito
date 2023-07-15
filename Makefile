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

check_burrito_cluster:
	$(PYTHON) scripts/check_burrito_cluster.py

run_burrito_cluster:
	scripts/run_burrito_cluster.sh

burrito_cluster_status:
	$(PYTHON) scripts/burrito_cluster_status.py
