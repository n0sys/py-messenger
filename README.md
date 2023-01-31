# Py Messenger
## Introduction
This app was written in python as part of a university project in Cryptography. The objective was to build a python app that transmits message's end to end encrypted between users. Algorithms used are RC4 for text messages encryption, RC5 for text files encryption and X3DH (Diffie Hellman) for key exchange. 

---

## Installation
### Docker
As communication was not the main subject of the project, I decided to use docker to set up a simple communication environment. It consists of 2 docker containers (clients) that communicate with each other and a server in between that hosts a MySQL database. The database will contain user's info, encrypted messages and public encryption keys.
On linux, install Docker using CLI:
```bash
$ apt-get install docker.io
```

#### Client Containers 
Using the Dockerfile in the source code, we can create the image that will be used to create the containers. Go to the cloned project directory and run:
```bash
$ docker build -t client:v1 .
$ docker network create --subnet=172.18.0.0/16 mynet
```
We create then 2 containers by running the below commands twice
```
$ docker container create -it --name CONTAINER_NAME client:v1
$ docker network connect mynet CONTAINER_NAME
```
We can then copy the source code into the containers with:
```bash
$ docker cp py-messenger/. CONTAINER_NAME:/py-app
```

#### Database Container
A simple command will create for us the database MySQL container:
```bash
$ docker run --name SQL --net mynet --ip 172.18.0.2 -e MYSQL_ROOT_PASSWORD=PASS -d mysql:latest
```
#### Database Setup
After connecting to the container, access the database with:
```bash
$ mysql -p
```
You should then get the network address of the containers and run the following commands (Substitute the host address with % eg '172.17.%.%' at NETWORK_ADDRESS)
```MySQL
CREATE DATABASE pyapp;
use pyapp;
CREATE TABLE users ( username varchar(255) NOT NULL, password varchar(70), PRIMARY KEY (username) ); 
CREATE USER 'signupbot'@NETWORK_ADDRESS IDENTIFIED WITH mysql_native_password BY 'signupbot';
GRANT SELECT,INSERT,DELETE,UPDATE ON pyapp.* TO 'signupbot'@NETWORK_ADDRESS;
CREATE TABLE keylists ( username varchar(255) NOT NULL, pg text(32765), id_pub text(32765),sigpk_pub text(32765),sig_sigpk text(32765),otpk_pub text(32765),eph_pub text(32765), PRIMARY KEY (username) );
CREATE TABLE messages_table ( username varchar(255) NOT NULL, message_number varchar(70), enc_message text(32765), message_type text(10000));
```
