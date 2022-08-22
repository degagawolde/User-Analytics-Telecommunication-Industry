FROM python:3.10.2

EXPOSE 8501

WORKDIR /dashboard
ADD . /dashboard

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
