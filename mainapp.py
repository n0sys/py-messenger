#!/usr/bin/python3
import db
from generate_keys import diffHellkeys,diffHellshared,get_pg
import elgamal
import configparser
import os
from rc4_py import message_rc4
from hmac_py import hmac
from rc5_py import RC5
import time

default_username="signupbot"
default_password="signupbot"

#TODO: Stable mysql container IP
#TODO: fix db tables structure
def welcome():
	print("----------------------------------------\nWelcome to SPM (Secure Python-Messenger)\n----------------------------------------\n")
	print("Please Login or Signup to use the app")

#Authentification pour se connecter a l'application
def auth():
	a= input("L(ogin)/S(ignup)?")
	if a=="L" or a =="login" or a == "Login":
		login()
	elif a=="S" or a=="signup" or a=="Signup":
		signup()
	else:
		print("Wrong input, type L to login or S to signup")
		auth()
		
#create an account
def signup():
	a=input("Type your username :")
	query = "SELECT username FROM users WHERE username='{}';".format(a)
	res=db.execute_query(default_username,default_password,query)
	if res!=[]:
		print("Username exists!")
		signup()
	else: 
		b=input("Type your password :")
		query = "INSERT INTO users VALUES ('{}','{}')".format(a,b)
		db.execute_query(default_username,default_password,query,'INSERT')
		auth()
	#fetch db for username || check if it already exists

#login with your username and password
def login():
	a=input("Type your username :")
	query = "SELECT username FROM users WHERE username='{}'".format(a)
	res=db.execute_query(default_username,default_password,query)
	if res!=[]:
		b=input("Type your password :")
		query = "SELECT username FROM users WHERE username='{}' and password='{}'".format(a,b)
		res=db.execute_query(default_username,default_password,query)
		if res!=[]:
			print("Successfully logged in")
			print("You may now message your contacts (M) and read messages they sent you (R).")
			choice=input("M(essage)/R(read)/G(enerate)?")
			if choice=='M':
				message(identity=a)
			elif choice=='R':
				read_received_messages(identity=a)
			elif choice=='G':
				#check if the message sender stored his keys in the db
				query = "SELECT * from keylists where username='{}'".format(a)
				res=db.execute_query(default_username,default_password,query)
				if res==[]:
					#generate keys and send to db
					ans=generate_keys(identity=a)
					if ans==False:
						print("Unknow error occurred. Please try again")
					login()
					exit()
			else:
				print("Wrong input")
				login()
		else:
			print("Wrong password")
			login()
	else:
		print("username doesn't exist")
		login()

#Encrypts and stores the message in the db
def message(identity):
	a=input("Type the username of the person you want to contact : ")
	query = "SELECT username FROM users WHERE username='{}'".format(a)
	res=db.execute_query(default_username,default_password,query)
	if res==[]:
		print("This username doesnt exist")
		message(identity)
	else:
		print("username exists")
		#check if the contacted user had already contacted us before and we havent yet
		query1 = "SELECT * FROM messages_table where username=concat('{}','_','{}');".format(a,identity)
		res1=db.execute_query(default_username,default_password,query1)
		query2="SELECT * FROM messages_table where username=concat('{}','_','{}');".format(identity,a)
		res2=db.execute_query(default_username,default_password,query2)
		if res1!=[] and res2==[]:
			generate_sk_as_receiver(a)
		#get the users sent message
		query = "SELECT * from keylists where username='{}'".format(identity)
		res=db.execute_query(default_username,default_password,query)
		if res==[]:
			print("You haven't yet generated your keys")
			login()
			exit()
		#check if message receiver stored his keys in the db
		query = "SELECT * from keylists where username='{}'".format(a)
		res=db.execute_query(default_username,default_password,query)
		if res==[]:
			print("Receiver is yet to set up his account. Try again later")
			#send_notif(identity,a)
			exit()
		#if receiver stored his key in the db > check if corresponding Shared Key already generated
		Config = configparser.ConfigParser()
		Config.read("config.ini")
		#if shared key not generated yet > generate it and store it
		if not "sk_"+a in Config.options("PrivateKeys"):
			generate_sk_as_first_sender(a)
		#if shared key was generated
		Config = configparser.ConfigParser()
		Config.read("config.ini")
		SK=str(Config.get('PrivateKeys',"sk_"+a))
		#get message_number:
		query = "SELECT message_number from messages_table where username='{}'".format(identity+'_'+a)
		message_number1=db.execute_query(default_username,default_password,query)
		if message_number1==[]:
			message_number1=0
		else:
			message_number1=int(message_number1[-1][0])
		query = "SELECT message_number from messages_table where username='{}'".format(a+'_'+identity)
		message_number2=db.execute_query(default_username,default_password,query)

		if message_number2==[]:
			message_number2=0
		else:
			message_number2=int(message_number2[-1][0])
		message_number=message_number1+message_number2+1
		msg_type=input("Do you want to send a (M)essage or a (F)ile? : ")
		if msg_type=='M':
			msg_type="message"
			msg=input("Type the message you want to send: ")
		elif msg_type=='F':
			msg_type="file"
			file_loc=input("Please specify the full path to the file you want to send: ")
			try:
				sent_file=open(file_loc,"r")
			except:
				print("Error : file not found")
				message(identity)
				exit()
			#read the content of the file
			msg=sent_file.readlines()
			msg=''.join(msg)
			msg=msg.strip()
		else:
			print("wrong choice")
			message(identity)
			exit()
		for i in range(message_number):
			#double ratchet | generate chain key corresponding to message number
			SK=hmac(SK,1,0)
		chain_key=SK
		message_key=hmac(chain_key,2,0)
		#encrypt message | rc4 if file - rc5 if plain message
		if msg_type=="file":
			enc_message=message_rc4(message_key,msg,op=1)
		#TODO: fix file encryption - RC5 key taken as string
		elif msg_type=="message":
			message_key = string_to_bytesarray(message_key)
			cryptor = RC5(message_key)
			cryptor.mode = "CBC"
			enc_message = cryptor.encrypt_str(msg)
		#store encrypted message in db
		query="INSERT INTO messages_table VALUES (concat('{}','_','{}'),'{}','{}','{}')".format(identity,a,str(message_number),enc_message,msg_type)
		res=db.execute_query(default_username,default_password,query,'INSERT')
		print("Message sent!")
		
			
def read_received_messages(identity):
	query = "SELECT * from keylists where username='{}'".format(identity)
	res=db.execute_query(default_username,default_password,query)
	if res==[]:
		print("You haven't yet generated your keys")
		login()
		exit()
	query = "SELECT * from messages_table where username like concat('%_','{}')".format(identity)
	res=db.execute_query(default_username,default_password,query)
	#contains value of username of previous row
	un_prev_row=''
	#
	started=0
	all_received_messages_list=[]
	#get names of all people who contacted us
	usernames=[]
	for row in res:
		u=row[0].split('_')[0]
		if not u in usernames:
			usernames.append(u)
	#check if Shared key was generated with these users else generate it now
	sk_dict={}
	Config = configparser.ConfigParser()
	Config.read("config.ini")
	for i in usernames:
		if not "sk_"+i in Config.options("PrivateKeys"):
			generate_sk_as_receiver(i)
		Config = configparser.ConfigParser()
		Config.read("config.ini")
		sk_dict[i]=str(Config.get('PrivateKeys',"sk_"+i))
	counter=0
	for row in res:
		SK=sk_dict[row[0].split("_")[0]]
		for i in range(int(row[1])):
			#double ratchet | generate chain key corresponding to message number
			SK=hmac(SK,1,0)
		chain_key=SK
		message_key=hmac(chain_key,2,0)
		if row[3]=='file':
			#then decrypt as file | rc4
			dec_message=message_rc4(message_key,row[2],op=0)
		elif row[3]=='message':
			#then decrypt as message | rc5
			message_key = string_to_bytesarray(message_key)
			cryptor = RC5(message_key)
			cryptor.mode = "CBC"
			dec_message = cryptor.decrypt_str(row[2])
		#decrypt row[2]
		#first iteration
		if started==0:
			same_user_messages=str(row[0].split('_')[0])+':::#?'+str(dec_message)+'-?!:,:'+row[3]+',,,,,,?'
			un_prev_row=row[0]
		if un_prev_row==row[0] and started != 0:
			same_user_messages+=str(dec_message)+'-?!:,:'+row[3]+',,,,,,?'
		elif un_prev_row!=row[0] and un_prev_row!='':
			un_prev_row=row[0]
			all_received_messages_list.append(same_user_messages)
			same_user_messsages=''
			same_user_messages=str(row[0].split('_')[0])+':::#?'+str(dec_message)+'-?!:,:'+row[3]+',,,,,,?'
		started=1
		counter+=1
		if counter == len(res):
			all_received_messages_list.append(same_user_messages)
	for chat in all_received_messages_list:
		#TODO: fix below
		user=chat.split(":::#?")[0]
		print("Showing messages received from "+user+ " :")
		msgs=chat.split(":::#?")[1]
		cnt=1
		msgs=msgs.split(",,,,,,?")
		for msg in msgs:
			if msg == '':
				continue
			content=msg.split('-?!:,:')[0]
			typ=msg.split('-?!:,:')[1]
			if typ == "file":
				print("You have received a file from "+user+ " !")
				if not "Downloads" in os.listdir():
					os.mkdir("Downloads")
				path="Downloads/"+content.split(" ")[0]+".txt"
				fil=open(path,"w")
				fil.write(content)
				fil.write("\n")
				fil.close()
				print("File saved in "+path)
			elif typ == "message":
				print(str(cnt)+") "+content)
				cnt+=1

#generates users keys and stores them in db
def generate_keys(identity):
	#fetch p and g from the database
	pg=get_pg()
	p=int(pg[0])
	g=int(pg[1])
	#generate ID key pair
	ID_keypair=diffHellkeys()
	ID_priv=ID_keypair[0]
	ID_pub=ID_keypair[1]
	#generate SIGPK key pair
	SIGPK_keypair=diffHellkeys()
	SIGPK_pub=SIGPK_keypair[1]
	#calculate Sig(SIGPK_pub,ID_priv) || elgamal signature
	SIG_SIGPK=elgamal.sign_elgamal(SIGPK_pub,ID_priv,p,g)
	#generate OTPK key pair
	OTPK_keypair=diffHellkeys()
	#generate EPH key pair
	EPH_keypair=diffHellkeys()
	#store priv keys + eph pub key in config file
	Config = configparser.ConfigParser()
	if Config.read("config.ini")==[]:
		#executes if config.ini doesnt exist
		Config.add_section('PrivateKeys')
	Config.set('PrivateKeys','ID_priv',str(ID_priv))
	Config.set('PrivateKeys','SIGPK_priv',str(SIGPK_keypair[0]))
	Config.set('PrivateKeys','OTPK_priv',str(OTPK_keypair[0]))
	Config.set('PrivateKeys','EPH_priv',str(EPH_keypair[0]))
	Config.set('PrivateKeys','EPH_pub',str(EPH_keypair[1]))
	cfgfile = open("config.ini",'w')
	Config.write(cfgfile)
	cfgfile.close()
	#store pub keys in db
	pg=[int(pg[i]) for i in range(len(pg))]
	query = "INSERT INTO keylists VALUES ('{}','{}','{}','{}','{}','{}','{}');".format(identity,pg,ID_keypair[1],SIGPK_keypair[1],SIG_SIGPK,OTPK_keypair[1],EPH_keypair[1])
	res=db.execute_query(default_username,default_password,query,'INSERT')
	return True

def generate_sk_as_first_sender(contact):
	#fetch contact's keys from the db
	Config = configparser.ConfigParser()
	Config.read("config.ini")
	query = "SELECT * from keylists where username='{}'".format(contact)
	res=db.execute_query(default_username,default_password,query)
	pg=res[0][1]
	pg=pg[1:-1]
	pg=pg.split(',')
	p=int(pg[0])
	g=int(pg[1])
	IDB_pub=res[0][2]
	SIGPKB_pub=int(res[0][3])
	SIG_SIGPKB=res[0][4]
	SIG_SIGPKB=SIG_SIGPKB[1:-1]
	SIG_SIGPKB=SIG_SIGPKB.split(',')
	OTPKB_pub=int(res[0][5])
	#exit if elgamal signature not verified
	if elgamal.verify_elgamal(SIGPKB_pub,SIG_SIGPKB,int(IDB_pub),p,g)==False:
		exit()
	#signature verified > 
	#get user's ID and EPH private keys
	IDA_priv=int(Config.get('PrivateKeys','id_priv'))
	EPHA_priv=int(Config.get('PrivateKeys','eph_priv'))
	#generate SK
	DH1=diffHellshared(SIGPKB_pub,IDA_priv)
	DH2=diffHellshared(int(IDB_pub),EPHA_priv)
	DH3=diffHellshared(SIGPKB_pub,EPHA_priv)
	DH4=diffHellshared(OTPKB_pub,EPHA_priv)
	all_DH=int(str(DH1)+str(DH2)+str(DH3)+str(DH4))
	SK=hmac(str(all_DH),1,0)
	Config.set('PrivateKeys','sk_'+str(contact),str(SK))
	cfgfile = open("config.ini",'w')
	Config.write(cfgfile)
	cfgfile.close()

def generate_sk_as_receiver(contact):
	Config = configparser.ConfigParser()
	Config.read("config.ini")
	#fetch contact's keys from the db
	query = "SELECT * from keylists where username='{}'".format(contact)
	res=db.execute_query(default_username,default_password,query)
	pg=res[0][1]
	pg=pg[1:-1]
	pg=pg.split(',')
	p=int(pg[0])
	g=int(pg[1])
	IDS_pub=res[0][2]
	SIGPKS_pub=int(res[0][3])
	SIG_SIGPKS=res[0][4]
	SIG_SIGPKS=SIG_SIGPKS[1:-1]
	SIG_SIGPKS=SIG_SIGPKS.split(',')
	OTPKS_pub=int(res[0][5])
	EPHS_pub=int(res[0][6])
	#exit if elgamal signature not verified
	if elgamal.verify_elgamal(SIGPKS_pub,SIG_SIGPKS,int(IDS_pub),p,g)==False:
		exit()
	#signature verified > 
	#get user's ID and EPH private keys
	IDR_priv=int(Config.get('PrivateKeys','id_priv'))
	SIGPKR_priv=int(Config.get('PrivateKeys','sigpk_priv'))
	OTPKR_priv=int(Config.get('PrivateKeys','otpk_priv'))
	#generate SK
	DH1=diffHellshared(int(IDS_pub),SIGPKR_priv)
	DH2=diffHellshared(EPHS_pub,IDR_priv)
	DH3=diffHellshared(EPHS_pub,SIGPKR_priv)
	DH4=diffHellshared(EPHS_pub,OTPKR_priv)
	all_DH=int(str(DH1)+'_'+str(DH2)+'_'+str(DH3)+'_'+str(DH4))
	SK=hmac(str(all_DH),1,0)
	Config.set('PrivateKeys','sk_'+str(contact),str(SK))
	cfgfile = open("config.ini",'w')
	Config.write(cfgfile)
	cfgfile.close()
	
def string_to_bytesarray(string: str) -> bytearray:
	counter = 0
	s = [string[2*i:2*i+2] for i in range(len(string)//2)]
	bytes_array = bytearray(len(s))

	for item in s:
		bytes_array[counter]=int(item, 16)
		counter+=1
	return bytes_array
		
if __name__ == "__main__":
	welcome()
	auth()
