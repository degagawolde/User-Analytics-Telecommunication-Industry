FROM ubuntu:latest

EXPOSE 8501

WORKDIR /app
ADD . /app
RUN apt install python3
RUN python3 -m venv dockerenv
RUN source dockerenv/bin/activate
RUN python3 -m pip install -r requirements.txt