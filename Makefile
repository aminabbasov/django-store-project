SIMULTANEOUS_TEST_JOBS=4

install-deps: deps
	pip-sync requirements.txt

deps:
	pip install --upgrade pip pip-tools
	pip-compile --output-file requirements.txt --resolver=backtracking pyproject.toml

install-dev-deps: dev-deps
	pip-sync dev-requirements.txt

dev-deps: deps
	pip install --upgrade pip pip-tools
	pip-compile --extra=dev --output-file dev-requirements.txt --resolver=backtracking pyproject.tom

server:
	cd src && ./manage.py migrate && ./manage.py runserver

worker:
	docker compose exec django celery --app app --workdir /src worker --events -l info

test:
	cd src && pytest -n ${SIMULTANEOUS_TEST_JOBS}
	cd src && pytest --cov=.
	cd src && pytest --dead-fixtures

format:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .