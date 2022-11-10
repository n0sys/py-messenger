import config
import mysql.connector

def connect_to_db(username,password):
	#add IP from config https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python
	mydb = mysql.connector.connect(host="172.17.0.3",user="signupbot",password="signupbot",database="pyapp")
	print(mydb) 
