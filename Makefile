SIMULTANEOUS_TEST_JOBS=4

worker:
	docker compose exec django celery --app app --workdir /src worker --events -l info

test:
	cd src && pytest -n ${SIMULTANEOUS_TEST_JOBS}
	cd src && pytest --cov=.
	cd src && pytest --dead-fixtures