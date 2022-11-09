Install Docker : sudo apt-get install docker.io
Create 2 clients containers ubuntu+python and 1 db container (https://docs.docker.com/build/building/packaging/):
		Create image: sudo docker build -t client:v1 .
		Create container: docker container create -it --name CONTAINER_NAME IMAGE:TAG
Setup Database in SQL container:
	mysql
	CREATE DATABASE pyapp;
	use pyapp;
	CREATE TABLE users ( username varchar(255) NOT NULL, password varchar(70), PRIMARY KEY (username) ); 
	
		






NB:
	docker cp src/. container_id:/target
	Password SHA-256
