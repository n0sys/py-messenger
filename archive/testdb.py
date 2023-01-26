import db

default_username="signupbot"
default_password="signupbot"
identity='hanna'
a='yara'
query1 = "SELECT * FROM messages_table where username=concat('{}','_','{}');".format(a,identity)
res1=db.execute_query(default_username,default_password,query1)
query2="SELECT * FROM messages_table where username=concat('{}','_','{}');".format(identity,a)
res2=db.execute_query(default_username,default_password,query2)
if res1!=[] and res2==[]:
	print('yes')
