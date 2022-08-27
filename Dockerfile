FROM python:3.10.2

EXPOSE 8501

WORKDIR /app
ADD . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
