FROM python:3.11.2

WORKDIR /usr/src/app
ENV FLASK_APP=app

COPY ./docker/py/entrypoint.sh /app/entrypoint.sh
RUN apt-get update
RUN apt-get install -y gcc openssl libssl-dev libbz2-dev wget zip tar gzip make vim unzip lsof

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]