FROM python:3.9-slim

RUN  mkdir -p /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y gcc g++ git build-essential tesseract-ocr tesseract-ocr-eng
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8888
