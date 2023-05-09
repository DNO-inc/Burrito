VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python3

run:
	$(PYTHON) -m burrito

docs_:
	doxygen docs.conf

create_user: tests/create_user.py
	$(PYTHON) tests/create_user.py

create_db_env: tests/create_db_env.py
	$(PYTHON) tests/create_db_env.py

clear_db:
	$(PYTHON) tests/clear_db.py

tests_:
	$(PYTHON) tests/run_tests.py
