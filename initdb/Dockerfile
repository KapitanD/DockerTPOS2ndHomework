FROM python:latest
COPY init.py /initdb/
COPY requirements.txt /initdb/
WORKDIR /initdb/
RUN mkdir /initdb/data && pip3 install -r requirements.txt