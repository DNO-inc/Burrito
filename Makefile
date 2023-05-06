VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python3

docs_:
	doxygen docs.conf

create_user: tests/create_user.py
	$(PYTHON) tests/create_user.py

tests_:
	$(PYTHON) tests/run_tests.py

run:
	$(PYTHON) -m burrito
