FROM python:3.12
LABEL authors="Crocussys"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/Nedelapare
COPY . .
RUN pip install -r requirements.txt
