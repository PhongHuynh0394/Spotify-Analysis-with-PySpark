FROM jupyter/minimal-notebook

USER root
RUN apt update 
RUN apt install -y openjdk-11-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64


WORKDIR /home/jovyan/work

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
