import sha256 

def paddingleft(constant, length):
	l=len(constant)
	while len(constant)<length:
		constant = "0" + constant
		l=l+1
	return constant
	


def xorstring(string1, string2):
	result=""
	if len(string1)==len(string2):
		l=len(string1)
		for i in range (l):
			if string1[i]==string2[i]:
				result=result + "0"
			else:
				result=result + "1"
	else:
		print("strings not the same size consider padding")
	
	return result
		
def hmac(sk, k, iv):

	#1: Append zeros to the left end of K to create a b- bit string K+. 
	k=bin(k)
	k=k.split('b')[1]
	
	b=2048 # length of b chunks
	
	kplus=paddingleft(k,b)
	
	
	#2. XOR K+ with ipad to produce the b-bit block Si. 
	ipad="00110110"*256
	opad="01011100"*256
	si=xorstring(kplus,ipad)
	
	
	#3. Append M to Si. 
	newsk=si+sk
	
	#4. Apply H to the stream generated in step 3. 
	hashed=sha256.sha256(newsk)
	hashed=paddingleft(hashed,b)
	
	#5. XOR K+ with opad to produce the b-bit block S0 
	s0=xorstring(kplus,opad)
	
	#6. Append the hash result from step 4 to S0 
	newsk=s0+hashed
	
	#7. Apply H to the stream generated in step 6 and output the result.
	hashed=sha256.sha256(newsk)
	
	return hashed
	
	
	
#a=2**8190
#a=str(a)
#b=1
#c=hmac(a,b,0)
#print(c)
