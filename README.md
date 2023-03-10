# Burrito API

## Setup
1. Launch Postgres in Docker:
```bash
docker run --name burrito-postgres -e POSTGRES_PASSWORD=root -p 5432:5432 -d postgres
```
2. Install `poetry`.
3. Configure the project:
```bash
poetry install
```
4. Activate virtual env:
```bash
poetry shell
```
5. Run app:
```bash
python -m buritto
```

P.S. Or you can configure everything in PyCharm.