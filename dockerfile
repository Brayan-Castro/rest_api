# syntax=docker/dockerfile:1

FROM python:3.13

WORKDIR /rest_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=rest_api.py

CMD ["flask", "run", "--debug"]