.PHONY: alembic-revision alembic-upgrade run-rollback run-seed

MESSAGE ?= "Default migration message"

SEED_USER_ID ?= 1
SEED_START ?= 20250810
SEED_END ?= 20250816

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
	poetry run pytest tests -v -s

run-seed:
	poetry run python scripts/seed_diary.py \
		--user-id $(SEED_USER_ID) \
		--start $(SEED_START) \
		--end $(SEED_END)