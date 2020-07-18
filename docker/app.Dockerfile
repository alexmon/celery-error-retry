FROM python:3.8

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./src/main.py .