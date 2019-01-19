FROM python:3.7.2-alpine3.8

COPY requirements.txt /app/

RUN apk add --no-cache git \
 && pip install -r /app/requirements.txt \
 && apk del git

COPY *.py /app/

