FROM ubuntu:22.04
WORKDIR /sql
RUN apt-get update && apt-get install -y mysql-server net-tools iputils-ping
CMD service mysql start ; while true; do sleep 1000; done
