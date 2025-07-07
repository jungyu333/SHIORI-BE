.PHONY: alembic-revision alembic-upgrade run-rollback

MESSAGE ?= "Default migration message"

run-dev:
	python src/shiori/main.py --env dev --debug

run-prod:
	python src/shiori/main.py --env prod

start-dev-db:
	docker start shiori-mysql

stop-dev-db:
	docker stop shiori-mysql

run-migration:
	alembic upgrade head

run-rollback:
	alembic downgrade -1

run-revision:
	alembic revision --autogenerate -m "$(MESSAGE)"

run-test:
	pytest tests -s