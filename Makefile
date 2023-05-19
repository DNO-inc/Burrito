VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python3

export BURRITO_DB_NAME=burrito
export BURRITO_DB_USER=burrito_user
export BURRITO_DB_PASSWORD=Qwerty123
export BURRITO_DB_HOST=192.168.0.173
export BURRITO_DB_PORT=3306

export BURRITO_HOST=127.0.0.1
export BURRITO_PORT=8080

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
