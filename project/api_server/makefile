start: connect
	python3 app/app.py

connect:
	. venv/bin/activate

celery:
	cd app/
	celery -A app.Tasks worker --loglevel=info

redis:
	sh ./app/run-redis.sh
