VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python3

run:
	$(PYTHON) -m burrito

docs_:
	doxygen docs.conf

create_user: tests/utils/create_user.py
	$(PYTHON) tests/utils/create_user.py

create_db_env: tests/utils/create_db_env.py
	$(PYTHON) tests/utils/create_db_env.py

clear_db: tests/utils/clear_db.py
	$(PYTHON) tests/utils/clear_db.py

tests_:
	$(PYTHON) tests/run_tests.py
