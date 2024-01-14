run-bot:
	python3 bot.py
run-web:
	uvicorn main:app --host 0.0.0.0 --port 8000
