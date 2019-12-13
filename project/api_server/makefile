start: connect
	python3 app/app.py

connect:
	. venv/bin/activate

celery:
	celery -A app.Tasks worker --loglevel=info --concurrency=6

redis:
	sh ./app/run-redis.sh
