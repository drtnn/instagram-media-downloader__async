FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN sudo timedatectl set-timezone Europe/Moscow
RUN pip install -r requirements.txt
