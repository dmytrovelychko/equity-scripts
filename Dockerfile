FROM python:3.10

WORKDIR /usr/app/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
