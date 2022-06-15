#!/usr/bin/python

import os, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

#gerados usando o os.urandom() num terminal python.
key = b'\x87\t/\x8d\xec\x1bF=`)\x17p\xba\xac\x13\xf8\xcc\xf8\x0c\x80\x1a`]\x1ab\xcd\x0ep\xefp\xa4\x14'#chave hard-coded para encriptar
hmackey = b'R\x17O\x84d\x1e\xbb\xda\xc5\xf2_\xf8\x97\xc3s\x86\nAq8\xb5\xb77\xa4\xaf\xc4?u\xb4J\xdc\xd9'#chave hard-coded para efetuar o mac
nonce = b'\xcd|\x7f\xd8\xd7\xf7n\xc6\xc0\x9c_s\xb5al\xbd'

msg = "Isto é uma mensagem não muito secreta!".encode('utf-8')


def w2f(nomeficheiro, data):
  with open(nomeficheiro, 'wb') as f:
    f.write(data)


def etm(): # Implementação do modo encrypt-then-mac

  print("key:",key)
  print("hmackey:",hmackey)
  
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor() #algoritmo de cifragem
  ct = encryptor.update(msg) + encryptor.finalize() #cifra a mensagem

  h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  h.update(ct) # faz MAC do criptograma
  tag=h.finalize() # cria a tag
  print("tag:",tag)
  dados=ct+tag

  w2f("dados-etm.dat", dados)
  print("ct e tag escritos no ficheiro")


def eam():  # Implementação do modo encrypt-and-mac

  print("key:",key)
  print("hmackey:",hmackey)

  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor()
  ct = encryptor.update(msg) + encryptor.finalize()#cifra a mensagem

  hh = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  hh.update(msg) # faz MAC da mensagem
  tag = hh.finalize()# cria a tag
  print("tag:",tag)

  dados = ct+tag 

  w2f("dados-eam.dat", dados) 
  print("ct e tag escritos no ficheiro")


def mte(): # Implementação do modo mac-then-encrypt


  hh = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  hh.update(msg)# faz MAC da mensagem
  tag = hh.finalize() # cria a tag
  

  msg_tag = msg+tag 
  
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor()

  ct = encryptor.update(msg_tag) + encryptor.finalize()#cifra o resultado da mensagem com a tag
  print("ct:",ct)

  w2f("dados-mte.dat", ct)
  print("ct escrito no ficheiro")



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
