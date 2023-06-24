# Burrito API

## Setup test environment
- First of all, you need to create .env file in the same directory as `burrito` folder, this file contains environment variables to configure our app, tests, and database
```bash
touch .env
```
- Necessary variables for containers
  - `burrito_app` - contain main logic
    - `BURRITO_DB_NAME` - table name
    - `BURRITO_DB_USER` - username allowed to interact with the table
    - `BURRITO_DB_PASSWORD` - user password
    - `BURRITO_DB_HOST` - database IP
    - `BURRITO_DB_PORT` - database port
  - `tests` - it's a container, tests should know where Burrito API is located
    - `BURRITO_HOST` - specify `Burrito API` IP to make test connections
    - `BURRITO_PORT` - specify `Burrito API` port to make test connections
  - `burrito_db` - contain MySQL database (you can find more information about MySql docker container and its environment variables [here](https://hub.docker.com/_/mysql)
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
- Launch Burrito API
```bash
docker-compose up
```
- Run tests
```bash
make tests_
```
