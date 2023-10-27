
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

> **Note:** Firstly Burrito API reads config from the local `.env` file, then it can be overwritten by  environment variables prepared from the console.


```bash
touch .env
```
- Necessary variables for containers
  - `burrito_api` - contain main logic
    - `BURRITO_DB_NAME` - database name
    - `BURRITO_DB_USER` - username allowed to interact with the database
    - `BURRITO_DB_PASSWORD` - user password
    - `BURRITO_DB_HOST` - database IP or domain
    - `BURRITO_DB_PORT` - database port
    - `BURRITO_HOST` - specify `Burrito API` host
    - `BURRITO_PORT` - specify `Burrito API` port
    - `BURRITO_REDIS_HOST` - redis IP or domain
    - `BURRITO_REDIS_PORT` - redis port
    - `BURRITO_REDIS_USER` - user for authorization
    - `BURRITO_REDIS_PASSWORD` - user password
    - `BURRITO_JWT_SECRET` - this key is used to encrypt/decrypt JWT tokens
    - `BURRITO_JWT_ACCESS_TTL` - access token's expiration time
    - `BURRITO_JWT_REFRESH_TTL` - refresh token's expiration time
    - `BURRITO_MONGO_HOST` - mongo host
    - `BURRITO_MONGO_PORT` - mongo port
    - `BURRITO_MONGO_DB` - database name to store date in mongo
    - `BURRITO_MONGO_USER` - mongo user
    - `BURRITO_MONGO_PASSWORD` - password for authorization
    - `BURRITO_SSU_KEY` - used for authorization via SSU cabinet (only for students of this university however you can write your own auth plugin)
    - `BURRITO_WEBSOCKET_HOST`
    - `BURRITO_WEBSOCKET_PORT`
    - `BURRITO_SMTP_SERVER` - SMTP server IP or domain
    - `BURRITO_EMAIL_LOGIN` - login for Burrito email
    - `BURRITO_EMAIL_PASSWORD` - password for Burrito email
  - `burrito_db` - contain MySQL database (you can find more information about `MySql` docker container and its environment variables [here](https://hub.docker.com/_/mysql)
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
  - `burrito_redis` - contains access/refresh tokens (no variables are needed)
  - `burrito_mongo` - contains comments, ticket changelog (full history), notifications data and files using GridFS. (you can find more information about `mongo` docker container and its environment variables [here](https://hub.docker.com/_/mongo)
    - `MONGO_INITDB_ROOT_USERNAME`
    - `MONGO_INITDB_ROOT_PASSWORD`

- Build Burrito API
```bash
docker build -t burrito_api .
```
- Launch needed databases
```bash
make dbs
```
- Launch Burrito API
```bash
docker run --rm -p8080:8080 --env-file .env --name burrito_api --network burrito_party burrito_api
```


## Burrito cluster

### Introduction

This mode runs in several processes.

### Setup test environment
- The environment variables are necessary as well as in the `burrito standalone` mode. All rules related to environment variables are the same as in the mentioned mode.

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
  - `burrito_scheduler` - contain scheduled tasks and it's able to setup database if it was not already done
  - `burrito_tickets` - provides the ability to manipulate users with their tickets, view other tickets ...
  - `burrito_db` - contain MySQL database
  - `burrito_nginx` - proxy-server and load balancer for `burrito cluster` (no variables are needed)
  - `burrito_redis` - contains access/refresh tokens (no variables are needed)

- Launch needed databases (if you would not setup own) in docker compose
```bash
make dbs
```
- Launch Burrito API (as you run first time the containers will fail to start, but they will be restarting while setuping database by container `burrito_scheduler`)
```bash
docker-compose -f docker-compose-separated.yml up 
```
