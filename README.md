# Django store project

An e-commerce website using Django (4.2) with PostgreSQL, Docker, Celery, and Redis. Dependencies managed with pip-tools. Maintains code quality with extra dev tools like Black, isort, and Flake8. Configured for testing with Pytest.

## Configuration
Configuration is stored in `src/app/.env`, for examples see `src/app/.env.dev`

## Installing on a local machine
This project requires python 3.11. Python **virtual environment** should be installed and activated.

Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools) with requirements stored in [pyproject.toml](https://github.com/jazzband/pip-tools#requirements-from-pyprojecttoml).

Install requirements:

```bash
pip install --upgrade pip pip-tools
```

Install dependencies:
```bash
pip-sync dev-requirements.txt
```

Configure postgres and redis. Use docker-compose:

```bash
docker-compose up -d
```

Run the server:

```bash
cd src && cp app/.env.dev app/.env  # default environment variables
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

If you want, populate the database with test records:

```bash
./manage.py loaddata demodb.json
```

## Usage

By default, website is at http://localhost:8000/. Besides, pg-admin for postgres is available at http://localhost:80/ and flower for celery at http://localhost:5555/.

For testing and formatting code use `make` commands:

```bash
# run format
make format

# run lint
make lint

# run unit tests
make test
```

## License

[MIT](https://choosealicense.com/licenses/mit/)