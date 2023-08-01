worker:
	docker compose exec django celery --app app --workdir /src worker --events -l info