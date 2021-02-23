FROM ubuntu:latest
MAINTAINER James Williams <james.williams@packetgeek.net>

RUN apt-get update && apt-get install -y openssl python3

ENV DOMAIN="www.dev.jtdub.com" 
ENV SUBJECT="/C=US/ST=TX/L=Austin/CN=www.dev.jtdub.com"
ENV EXPIRE=365

WORKDIR /opt/sslbot

COPY sslbot.py .

CMD python3 sslbot.py 
