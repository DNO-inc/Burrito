
# Burrito API

> **Note:** Documentation will be updated in soon.

## About the project
Hi there, this project developing to provide you with a fast way to deploy your ticket system. You can use our other project TreS as a bridge between users and Burrito API. Burrito API can run in several modes:
* `burrito standalone` (monolithic)
* `burrito cluster` (microservices)



## Burrito standalone

### Introduction

This mode runs in a single process.

### Setup test environment
- First of all, you need to prepare environment variables. You can create .env file in the same directory as `burrito` folder, this file contains environment variables to configure our app, tests, and database.

> **Note:** Firstly, Burrito API reads config from the local `.env` file, then it can be overwritten by variables prepared from the console.


```bash
touch .env
```
- Necessary variables for containers
  - `burrito_app` - contain main logic
    - `BURRITO_DB_NAME` - table name
    - `BURRITO_DB_USER` - username allowed to interact with the table
    - `BURRITO_DB_PASSWORD` - user password
    - `BURRITO_DB_HOST` - database IP or domain
    - `BURRITO_DB_PORT` - database port
    - `BURRITO_REDIS_HOST` - redis IP or domain
    - `BURRITO_REDIS_PORT` - redis port
    - `BURRITO_JWT_SECRET` - this key is used to encrypt/decrypt JWT tokens
    - `BURRITO_JWT_TTL` - token's expiration time
    - `BURRITO_HOST` - specify `Burrito API` host
    - `BURRITO_PORT` - specify `Burrito API` port
  - `burrito_db` - contain MySQL database (you can find more information about MySql docker container and its environment variables [here](https://hub.docker.com/_/mysql)
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
  - `burrito_redis` - contains access/refresh tokens (no variables are needed)
- Launch Burrito API
```bash
docker-compose up
```
- Run tests
```bash
make tests_
```


## Burrito cluster

### Introduction

This mode runs in several processes.

### Setup test environment
- The environment variables are necessary as well as in the `burrito standalone` mode. All rules related to environment variables are the same as in the mentioned mode.


```bash
touch .env
```
- Necessary variables for containers
  - `burrito_app` - contain main logic
    - `BURRITO_DB_NAME` - table name
    - `BURRITO_DB_USER` - username allowed to interact with the table
    - `BURRITO_DB_PASSWORD` - user password
    - `BURRITO_DB_HOST` - database IP or domain
    - `BURRITO_DB_PORT` - database port
    - `BURRITO_REDIS_HOST` - redis IP or domain
    - `BURRITO_REDIS_PORT` - redis port
    - `BURRITO_JWT_SECRET` - this key used to encrypt/decrypt JWT tokens
    - `BURRITO_JWT_TTL` - token's expiration time
    - `BURRITO_HOST` - specify `Burrito API` host
    - `BURRITO_PORT` - specify `Burrito API` port (for each container of cluster)
  - `burrito_db` - contain MySQL database (you can find more information about MySql docker container and its environment variables [here](https://hub.docker.com/_/mysql)
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
  - `burrito_nginx` - proxy-server and load balancer for `burrito cluster` (no variables are needed)
  - `burrito_redis` - contains access/refresh tokens (no variables are needed)
- Launch Burrito API
```bash
make burrito_cluster_run
```
- Ping `apps`
```bash
make burrito_cluster_ping
```
- Run tests
```bash
make tests_
```