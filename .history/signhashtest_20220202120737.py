import time
import hashlib
import string
from Crypto.PublicKey import RSA
import random
from ecdsa import SigningKey, SECP256k1
import codecs
from hashlib import sha256
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

# privkeyhex = hex(random.getrandbits(256))[2:]
# print("priv key hex ")
# print(privkeyhex)
# privkey = codecs.decode(privkeyhex, 'hex')
# print("priv key decoded from  hex")
# print(privkey)
# key = SigningKey.from_string(privkey, curve=SECP256k1).verifying_key
# print("key straight from signing")
# print(key)
# key_bytes = key.to_string()
# print("publickey in bytes")
# print(key_bytes)
# publickey = codecs.encode(key_bytes, 'hex')
# print("publickey in hex")
# print(publickey)

# below is a test to do it in one line
testpriv = 'e6cc0f061bf1be523c92032a8c436a4b6729ce34ec7a9244f01b3e33abf28a66'
testpub = '9fabbb30cbce815530e4c7d201c1110d78432d4708b06ced582f69288e299c04cb9517a8d68d5a0d75fd1261b114dc80cb436c795aa8e82c5cde93cc4fc3f195'
print(testpriv)
print(testpub)
#print(codecs.encode(SigningKey.from_string(codecs.decode(testpriv, 'hex'), curve=SECP256k1).verifying_key.to_string(), 'hex'))
##############################
# signing key = private key  #
# verifying key = public key #
##############################
# privatekey from string
privatekey = SigningKey.from_string(
    codecs.decode(testpriv, 'hex'), curve=SECP256k1)
# making public string from private string
publickey = privatekey.get_verifying_key()
print(privatekey)
print(publickey)
print(privatekey.to_string().hex())
print(publickey.to_string().hex())

message = "my message"

signedmessage = privatekey.sign(str.encode(message))
# finally
try:
    print(publickey.verify(signedmessage, b"my message"))
except:
    print("signed message cannot be verified")

password = ''.join(random.choice(string.ascii_letters) for x in range(4))
hashedpassword = hashlib.md5(password.encode())
guess = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
print(password)
start_time = time.time()
try:
    for q in range(52):
        for w in range(52):
            for e in range(52):
                for r in range(52):
                    if hashedpassword.hexdigest() == (hashlib.md5(str(guess[q]+guess[w]+guess[e]+guess[r]).encode())).hexdigest():
                        raise StopIteration
except StopIteration:
    print("--- %s seconds ---" % (time.time() - start_time))
    print("found it")
