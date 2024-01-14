run-bot:
	python3 bot.py
run-web:
    uvicorn main:app --host 127.0.0.1 --port 8000
