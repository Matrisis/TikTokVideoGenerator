FROM python:3.9

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r app/requirements.txt

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y ffmpeg
