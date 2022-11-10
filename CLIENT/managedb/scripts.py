import mysql.connector

def connect_to_db(username,password):
	mydb = mysql.connector.connect(host="172.17.0.3",user="signupbot",password="signupbot",database="pyapp")
	print(mydb) 
