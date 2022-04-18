FROM python:3.8-alpine

WORKDIR /app

RUN apk add --update --upgrade build-base ca-certificates python3 python3-dev py3-pip ffmpeg gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

COPY . /app

RUN pip3 install -r ./requirements.txt

RUN mkdir -p /etc/chaperone.d
RUN rm -rf /tmp/*
RUN rm -rf /var/cache/*

CMD [ "python3", "src/main.py" ]
