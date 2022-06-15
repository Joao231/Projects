#!/usr/bin/python

import os, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

#mesmos valores do ficheiro enc.py
key = b'\x87\t/\x8d\xec\x1bF=`)\x17p\xba\xac\x13\xf8\xcc\xf8\x0c\x80\x1a`]\x1ab\xcd\x0ep\xefp\xa4\x14'
hmackey = b'R\x17O\x84d\x1e\xbb\xda\xc5\xf2_\xf8\x97\xc3s\x86\nAq8\xb5\xb77\xa4\xaf\xc4?u\xb4J\xdc\xd9'
nonce = b'\xcd|\x7f\xd8\xd7\xf7n\xc6\xc0\x9c_s\xb5al\xbd'

def rff(nomeficheiro):
	with open(nomeficheiro, 'rb') as f:
		return f.read()

def etm(): #Inverte o modo encrypt-then-mac

	data = rff("dados-etm.dat")

	ct = data[:-32] #extrai o ct
	tag = data[-32:] #extrai a tag
	
	algorithm = algorithms.ChaCha20(key, nonce)
	cipher = Cipher(algorithm, mode=None, backend=default_backend())

	h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
	h.update(ct)
	h.verify(tag) # verifica a tag

	#decifra o criptograma, caso a tag esteja correta.
	decryptor = cipher.decryptor() #algoritmo de decifragem
	msg = decryptor.update(ct) #decifra o criptograma

	print("mensagem:", msg.decode("utf-8"))



def eam(): #Inverte o modo encrypt-and-mac

	data = rff("dados-eam.dat")

	tag = data[-32:]#extrai a tag
	
	ct = data[:-32]#extrai o ct

	algorithm = algorithms.ChaCha20(key, nonce)
	cipher = Cipher(algorithm, mode=None, backend=default_backend())

	decryptor = cipher.decryptor() 
	msg = decryptor.update(ct) #decifra o criptograma

	h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
	h.update(msg) 
	h.verify(tag) # verifica a tag

	#decifra o criptograma, caso a tag esteja correta.
	print("mensagem:", msg.decode("utf-8"))


def mte(): #Inverte o modo mac-then-encrypt
	data = rff("dados-mte.dat")
	ct = data

	algorithm = algorithms.ChaCha20(key, nonce)
	cipher = Cipher(algorithm, mode=None, backend=default_backend())

	decryptor = cipher.decryptor() 
	dec = decryptor.update(ct)#decifra o criptograma(resultado da mensagem com a tag)

	msg = dec[:-32]# extrai a mensagem
	tag = dec[-32:]#extrai a tag

	h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
	h.update(msg) 
	h.verify(tag)# verifica a tag

	#decifra o criptograma, caso a tag esteja correta.
	print("mensagem:", msg.decode("utf-8"))
  


def main():

  if len(sys.argv) != 2:
    print("Please provide one of: eam, etm, mte")
  elif sys.argv[1] == "eam":
    eam()
  elif sys.argv[1] == "etm":
    etm()
  elif sys.argv[1] == "mte":
    mte()
  else:
    print("Please provide one of: eam, etm, mte")

if __name__ == '__main__':
  main()
