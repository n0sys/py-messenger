Install Docker : sudo apt-get install docker.io
Create 2 clients containers ubuntu+python (https://docs.docker.com/build/building/packaging/):
		Create image: sudo docker build -t client:v1 .
		Create container: docker container create -it --name CONTAINER_NAME IMAGE:TAG
Create DB container:
		docker run --name SQL -e MYSQL_ROOT_PASSWORD=PASS -d mysql:latest
Setup Database in SQL container:
	mysql
	CREATE DATABASE pyapp;
	use pyapp;
	CREATE TABLE users ( username varchar(255) NOT NULL, password varchar(70), PRIMARY KEY (username) ); 
	CREATE USER 'signupbot'@'172.17.%.%' IDENTIFIED BY 'signupbot';
	GRANT INSERT ON pyapp.users TO 'signupbot'@'172.17.%.%';
	
TODO: dont specify ip addresses
		






NB:
	docker cp src/. container_id:/target
	Password SHA-256
