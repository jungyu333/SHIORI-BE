run-dev:
	python src/kokoro_be/main.py --env dev --debug

run-prod:
	python src/kokoro_be/main.py --env prod

start-dev-db:
	docker start kokoro-mysql

stop-dev-db:
	docker stop kokoro-mysql