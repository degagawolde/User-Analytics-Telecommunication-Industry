FROM ubuntu:latest

EXPOSE 8501

WORKDIR /app
ADD . /app
RUN apt-get install software-properties-common
RUN apt-add-repository universe
RUN apt-get update
RUN apt-get install python3-pip
RUN python3 -m venv dockerenv
RUN source dockerenv/bin/activate
RUN python3 -m pip install -r requirements.txt