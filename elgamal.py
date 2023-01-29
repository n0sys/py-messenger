import random
from hashlib import sha256
import libnum
from math import gcd
from generate_keys import exprap

def sign_elgamal(key,priv_key,p,g):
	#p prime number, g generator >> fetch from db

	prime=False
	y=random.randrange(2,p-1)
	#verify that gcd y,p-1!=1
	while prime==False:
		if gcd(y,p-1)!=1:
			y=random.randrange(2,p-2)
		else:
			prime=True
	y_minus=(libnum.invmod(y, p-1))
	#transform key (which is an int) to bytes
	key=key.to_bytes((key.bit_length()+7) // 8,'big')
	#hash 256 of key
	#TODO:use sha256 own implementation  
	hash_key=sha256()
	hash_key.update(key)
	hash_key=hash_key.hexdigest()
	int_hash_key=int(hash_key,16)
	s1=exprap(g,y,p)
	s2=(y_minus*(int_hash_key-priv_key*s1)) % (p-1)
	if s2==0:
		sign_elgamal(message,priv_key)
	else: 
		return [s1,s2]

def verify_elgamal(key,s_list,pub_key,p,g):
	#p prime number, g generator, pub_key public key > fetch from db
	#key is SIGPK_pub // s_list is [s1,s2] signed in elgamal // pub_key is key to verify the signature (ID_pub)
	
	s1=int(s_list[0])
	s2=int(s_list[1])
	key=key.to_bytes((key.bit_length()+7) // 8,'big')
	hash_key=sha256()
	hash_key.update(key)
	hash_key=hash_key.hexdigest()
	int_hash_key=int(hash_key,16)
	k= (exprap(pub_key,s1,p)*exprap(s1,s2,p))%p
	if k==exprap(g,int_hash_key,p):
		#print("Signature verified")
		return True
	else:
		#print("wrong signature")
		return False
