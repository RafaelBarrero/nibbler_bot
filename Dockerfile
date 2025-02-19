FROM python:3.13-alpine

WORKDIR /app

RUN apk add --update --upgrade --no-cache build-base ca-certificates ffmpeg musl-dev zlib-dev libffi-dev opus-dev

COPY . /app

RUN pip3 install -r ./requirements.txt

RUN mkdir -p /etc/chaperone.d
RUN rm -rf /tmp/*
RUN rm -rf /var/cache/*

ENV PYTHONPATH="/app"

CMD [ "python3", "src/main.py" ]
