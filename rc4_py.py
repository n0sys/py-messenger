#https://pycryptodome.readthedocs.io/en/latest/src/public_key/dsa.html
#HKDF: https://www.ietf.org/rfc/rfc5869.txt
from binascii import hexlify,unhexlify
from numpy import roll

#TODO: use something other than numpy
#https://sandilands.info/sgordon/teaching/css322y07s2/protected/CSS322Y07S2H03-RC4-Example.pdf
#RC4 stream cipher and decipher
def message_rc4(key,message,op):
	#message should be a clear text message eg: "hello"
	#op == 1 >> encryption, op == 0 >> decryption
	if op == 1:
		hex_message=[]
		#transform each character in the message to hex
		for char in message:
			hex_message.append(str(hexlify(char.encode('utf8')))[2:-1])
	if op == 0:
		hex_message=[message[i:i+2] for i in range(0,len(message), 2)]
	#split key to a list of 2 hex characters
	key=[key[i:i+2] for i in range(0, len(key), 2)]

	#initialise R vector
	R=[i for i in range(256)]
	j=0
	#initial permutation
	for i in range(256):
		j=(j+R[i]+int(key[i % len(key)],16)) % 256
		R[i], R[j] = R[j], R[i]

	i=0; j=0; n=0
	enc=""
	while n<=len(hex_message)-1:
		i=(i+1) % 256
		j=(j+R[i]) % 256
		R[i], R[j] = R[j], R[i]
		t=(R[i]+R[j]) % 256
		#xor decimal values
		dec_res=int(str(hex_message[n]),16) ^ R[t]
		#enc contains the encrypted value of the message in hex
		val=hex(dec_res)[2:]
		if len(val)==1:
			val="0"+val
		enc+=val
		n+=1
	if op == 1:
		return enc
	elif op == 0:
		return str(unhexlify(enc))[2:-1]
