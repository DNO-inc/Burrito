
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
- First of all, you need to prepare environment variables. You can create .env file in the same directory as the `burrito` folder, this file contains environment variables to configure our app, tests, and database.

> **Note:** Firstly, Burrito API reads config from the local `.env` file, then it can be overwritten by variables prepared from the console.


```bash
touch .env
```
- Necessary variables for containers
  - `burrito_app` - contain main logic
    - `BURRITO_DB_NAME` - database name
    - `BURRITO_DB_USER` - username allowed to interact with the database
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
- Available containers
  - `burrito_about` - container to provide information about development teams
  - `burrito_admin` - contain logic for admins
  - `burrito_anon` - logic for anon users
  - `burrito_auth` - provides authorization ability
  - `burrito_comments` - provide access to manipulate with comments attached to the ticket
  - `burrito_iofiles` - process file uploading/downloading
  - `burrito_meta` - provide meta information related to the project
  - `burrito_notifications` - send/receive notifications
  - `burrito_profile` - allow to manipulate with own profile and view other
  - `burrito_registration` - user registration (will be deleted soon from this branch, this ability will be available on the `burrito_base` branch)
  - `burrito_tickets` - provides the ability to manipulate users with their tickets, view other tickets ...
  - `burrito_db` - contain MySQL database (you can find more information about MySql docker container and its environment variables [here](https://hub.docker.com/_/mysql)
  - `burrito_nginx` - proxy-server and load balancer for `burrito cluster` (no variables are needed)
  - `burrito_redis` - contains access/refresh tokens (no variables are needed)
- Launch Burrito API
```bash
make burrito_cluster_run
```
- Run tests
```bash
make tests_
```
