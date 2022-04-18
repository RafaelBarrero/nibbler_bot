FROM alpine:latest

RUN apk add --update build-base ca-certificates python3 python3-dev ffmpeg

RUN cd /usr/bin \
  && ln -sf python3.8 python \
  && ln -sf pip3.8 pip

# for numpy install
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install --no-cache-dir --upgrade \
  pip \
  wheel>0.25.0 \
  distribute \
  chaperone \
  numpy==1.12.0 \
  pycrypto==2.6.1 \
  pyyaml==3.11 \
  pytest==2.9.2 \
  sortedcontainers==1.5.3

RUN pip install -r requirements.txt

RUN mkdir -p /etc/chaperone.d
RUN rm -rf /tmp/*
RUN rm -rf /var/cache/*

CMD [ "python3", "src/main.py" ]
