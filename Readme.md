# WB Parser

Веб-сервис, состоящий из двух частей - Telegram-бота, и API.

## Установка
Создание виртуального окружения:

```bash
python3 -m venv venv
```
Активация виртуального окружения:
```bash
source venv/bin/activate
```

Установка зависимостей:

```bash
pip3 install -r requirements.txt
```

## Запуск
Запуск бота:
```bash
python3 bot.py
```
Запуск web-api:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Альтернатива - запуск через make:
```bash
# Запуск бота
make run-bot

# Запуск web-api
make run-web
```

## Запуск через Docker

```bash
docker-compose up
```

