FROM python:3.8

RUN pip install --upgrade pip

RUN mkdir -p /tgbot
WORKDIR /tgbot
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /tgbot
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
