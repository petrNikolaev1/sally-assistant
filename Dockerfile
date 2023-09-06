FROM python:3.10-slim

RUN apt update && apt install git g++ -y

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /service
COPY service /service

WORKDIR /
COPY run.py .

CMD python run.py
