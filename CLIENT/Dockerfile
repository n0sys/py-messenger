FROM ubuntu:22.04
WORKDIR /py-app
RUN apt-get update && apt-get install -y python3 python3-pip net-tools iputils-ping
RUN pip3 install mysql-connector-python
CMD while true; do sleep 1000; done
