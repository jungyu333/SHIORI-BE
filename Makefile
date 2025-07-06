run-dev:
	python src/shiori/main.py --env dev --debug

run-prod:
	python src/shiori/main.py --env prod

start-dev-db:
	docker start shiori-mysql

stop-dev-db:
	docker stop shiori-mysql