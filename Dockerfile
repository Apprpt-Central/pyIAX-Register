FROM python:3-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /srv/register
WORKDIR /srv/register
