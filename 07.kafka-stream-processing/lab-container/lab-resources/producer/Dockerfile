FROM python:3.13-alpine

WORKDIR /app

RUN pip install kafka-python

COPY kafka_producer.py .
COPY data.csv .
