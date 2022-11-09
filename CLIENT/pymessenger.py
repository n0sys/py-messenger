#!/usr/bin/python3
from managedb.scripts import *

def welcome():
	print("----------------------------------------\nWelcome to SPM (Secure Python-Messenger)\n----------------------------------------\n")
	print("Please Login or Signup to use the app")

#Authentification pour se connecter a l'application
def auth():
	a= input("L(ogin)/S(ignup)?")
	if a=="L" or a =="login" or a == "Login":
		print("LOGINFUNCTION")
	elif a=="S" or a=="signup" or a=="Signup":
		print("SIGNUPFUNCTION")
		signup()
	else:
		print("Wrong input, type L to login or S to signup")
		auth()
		
def signup():
	#identifiants temporaires pour la premiere connexion a la base de donnees // ne possede de permission que l'insertion de nouveaux utilisateurs
	username="signupbot"
	password="signupbot"
	connect_to_db(username,password)

if __name__ == "__main__":
	welcome()
	auth()
