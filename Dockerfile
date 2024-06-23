# Этап, на котором выполняются подготовительные действия
FROM python:3.9-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc


COPY requirements.txt .
RUN pip install -r requirements.txt
COPY tg_vector ./tg_vector
ENV PYTHONPATH=$PYTHONPATH:/app/tg_vector
EXPOSE 8000
ENTRYPOINT ["python", "tg_vector/main.py"]