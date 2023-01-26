from rc5_py import RC5
import time

test_origin_char = '{}-{}'.format(99999999, int(time.time()))
key = 'pig'
cryptor = RC5(pwd)
cryptor.mode = "CBC"
enc_str = cryptor.encrypt_str(test_origin_char)
print(enc_str)
dec_str = cryptor.decrypt_str(enc_str)
print(dec_str)
