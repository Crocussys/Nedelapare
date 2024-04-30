FROM python
LABEL authors="Crocussys"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/Nedelapare
COPY www ./www/
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
