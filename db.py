import mysql.connector

#identifiants temporaires pour la premiere connexion a la base de donnees 
#TODO: Add IP to project settings

def execute_query(username,password,query,typ='SELECT'):
	#add IP from config https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python
	mydb = mysql.connector.connect(host="172.17.0.2",user=username,password=password,database="pyapp",auth_plugin='mysql_native_password')
	cursor = mydb.cursor(buffered=True)
	cursor.execute(query)
	if typ=='INSERT':
		mydb.commit()
	elif typ=='SELECT':
		return cursor.fetchall()
	cursor.close()
	mydb.close()
	


