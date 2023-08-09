SIMULTANEOUS_TEST_JOBS=4

install-deps: deps
	pip-sync requirements.txt

deps:
	pip install --upgrade pip pip-tools
	pip-compile --output-file requirements.txt --resolver=backtracking pyproject.toml

install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

dev-deps: deps
	pip-compile --extra=dev --output-file dev-requirements.txt --resolver=backtracking pyproject.toml

server:
	cd src && ./manage.py migrate && ./manage.py runserver

worker:
	docker compose exec django celery --app app --workdir /src worker --events -l info

lint:
	cd src && ./manage.py makemigrations --check --no-input --dry-run
	flake8 src
	# cd src && mypy

format:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .

test:
	cd src && pytest -n ${SIMULTANEOUS_TEST_JOBS}
	cd src && pytest --cov=.
	cd src && pytest --dead-fixtures
