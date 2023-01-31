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
		print("'"+message+ "' was encrypted to the following hex: "+str(enc))
		return enc
	elif op == 0:
		#a=unhexlify(enc))[2:-1]
		#print("'"+message+ "' was decrypted to the following: "+str(a.strip())
		return str(unhexlify(enc))[2:-1]
	else:
		print("error")

#rc4 usage
#from encrypter import message_rc4
#message="82b48016f3"
#key="aa1246ff"
#op=0
##message_rc4 returns a string of hex characters
#h=message_rc4(key,message,op)

#############################################################################
#pn=16158503035655624599199696032452650342710968885578229456162378335772580871983620425783369741838218029778896156965010037619521531733905047652217350086577114973392159715698716514419001289057806277453028228525265330724353766644011669371609415047878735101647376965245825194508405352411063929145760100689409966103853282694690612574488732679462386255416600836502218970971436599862605743486396647217301249954917411323277055713632149068959449047039230081137886186557820842348986572349840259390139717280755298451208192732415057010807528548525624132123361795757236582071520211100928398845793700347389203879804586887931894956613
