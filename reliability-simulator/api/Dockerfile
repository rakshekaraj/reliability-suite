FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./main.py /app/app/main.py

RUN pip install prometheus_client

ENV PYTHONUNBUFFERED=1