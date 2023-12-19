FROM python:3.11

EXPOSE 8501

WORKDIR /usr/src/app

COPY . .

USER root

RUN chmod +x ./init.bash

RUN pip install -r requirements.txt
