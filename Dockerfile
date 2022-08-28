FROM python:3.10.2

EXPOSE 8501

WORKDIR /app
ADD . /app

RUN python3 -m venv docker-env
RUN source docker-env/bin/activate
RUN python3 -m pip install -r requirements.txt