FROM python:3.12.1-alpine3.18
WORKDIR /code

COPY . .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 users_dao.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

