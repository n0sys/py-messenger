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
	CREATE USER 'signupbot'@'172.17.%.%' IDENTIFIED WITH mysql_native_password BY 'signupbot';
	GRANT SELECT,INSERT,DELETE,UPDATE ON pyapp.* TO 'signupbot'@'172.17.%.%';
	CREATE TABLE keylists ( username varchar(255) NOT NULL, pg text(32765), id_pub text(32765),sigpk_pub text(32765),sig_sigpk text(32765),otpk_pub text(32765),eph_pub text(32765), PRIMARY KEY (username) );
	INSERT INTO keylists VALUES ('default',$pg,'NA','NA','NA','NA','NA');  ##pg='[1,2]'
	CREATE TABLE messages_table ( username varchar(255) NOT NULL, message_number varchar(70), enc_message text(32765), message_type text(10000));
TODO: dont specify ip addresses
		






NB:
	docker cp src/. container_id:/target
	Password SHA-256
	sudo docker cp pymessengermaster/mainapp.py Bob:/py-app
