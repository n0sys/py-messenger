#Diffie Hellman code

from exprapide import exprap
import random

def diffHellshared(pub,priv,p):
	skey=exprap(pub,priv,p)
	return skey

#pub is the public key of the other person we need to get from the server
#priv is the private key of the user genrated randomely

def diffHellkeys(p,g):
	priv=random.randrange(2,p)
	pub=exprap(gen,priv,p)
	return [priv,pub]

