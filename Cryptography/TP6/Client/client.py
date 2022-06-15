#!/usr/bin/python

import socket
import threading
import sys, signal
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1, PKCS1v15

from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Foobar:
    pass

AES_BLOCK_LEN = 16 # bytes
AES_KEY_LEN = 32 # bytes
PKCS7_BIT_LEN = 128 # bits
SOCKET_READ_BLOCK_LEN = 4096 # bytes

def signal_handler(sig, frame):
  print('You pressed Ctrl+C; bye...')
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# An useful function to open files in the same dir as script...
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def path(fname):
  return os.path.join(__location__, fname)

host = "localhost"
port = 8080

# RFC 3526's parameters. Easier to hardcode...
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2
params_numbers = dh.DHParameterNumbers(p,g)
parameters = params_numbers.parameters(backend=default_backend())

def connect():
  #Attempt connection to server
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock
  except Exception as e:
    print("Could not make a connection to the server: %s" % e)
    input("Press enter to quit")
    sys.exit(0)

# Receives and returns bytes.
def encrypt(k, m):
  

  padder = padding.PKCS7(PKCS7_BIT_LEN).padder()
  padded_data = padder.update(m) + padder.finalize()
  iv = os.urandom(AES_BLOCK_LEN)
  cipher = Cipher(algorithms.AES(k), modes.CBC(iv),backend= default_backend())
  encryptor = cipher.encryptor()

  ct = encryptor.update(padded_data) + encryptor.finalize()
  return iv+ct

# Receives and returns bytes.
def decrypt(k, c):
  

  iv, ct = c[:AES_BLOCK_LEN], c[AES_BLOCK_LEN:]
  cipher = Cipher(algorithms.AES(k), modes.CBC(iv),backend=default_backend())
  decryptor = cipher.decryptor()
  pt = decryptor.update(ct) + decryptor.finalize()
  unpadder = padding.PKCS7(PKCS7_BIT_LEN).unpadder()
  pt = unpadder.update(pt) + unpadder.finalize()
  return pt

def handshake(socket):
  #certificado do cliente e correspondente chave pública
  with open(path("TC_Client.cert.pem"), "rb") as cert_client_file:
        client_certificate_as_bytes = cert_client_file.read()
        client_cert = load_pem_x509_certificate(client_certificate_as_bytes,backend=default_backend()) 
        client_public_key = client_cert.public_key()

  #chave privada do cliente do certificado do cliente
  with open(path("TC_Client.key.pem"), "rb") as client_file:
    client_certificate_as_byte = client_file.read()
    client_private_key = load_pem_private_key(client_certificate_as_byte, password=None,backend=default_backend())

  
  #passar a chave pública do cliente para bytes
  client_public_key_as_bytes = client_public_key.public_bytes(
                                        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)



  #passar a chave privada do cliente para bytes
  client_private_key_as_bytes = client_private_key.private_bytes(
  encoding=serialization.Encoding.PEM,
  format=serialization.PrivateFormat.PKCS8,
  encryption_algorithm=serialization.NoEncryption())

  #gerar um número, a partir dos parâmetros hard-coded no início do ficheiro, que corresponde ao x do protocolo Diffie-Hellman
  x = parameters.generate_private_key()

  #gerar a chave pública a partir do número anterior. Será o gx do protocolo Diffie-Hellman que será enviado para o servidor
  g_x = x.public_key()

  #passar o resultado anterior para bytes para se poder enviar ao servidor
  g_x_bytes = g_x.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

  #enviar para o servidor o resultado anterior
  socket.sendall(g_x_bytes)


  #o cliente recebe os dados enviados na forma de bytes pelo servidor
  data = socket.recv(SOCKET_READ_BLOCK_LEN)
  data = data.split(sep=b"\r\n\r\n")#fazer o split do resultado anterior(1º elemento corresponde ao gy, 2º elemento corresponde
  #à assinatura mas encriptada e 3º elemento corresponde ao certificado do servidor)



  #passar o certificado recebido para objecto, uma vez que se encontrava em bytes
  cert = load_pem_x509_certificate(data[2],backend=default_backend())
  server_public_key = cert.public_key()#extrair a chave publica desse certificado

  
  g_y = load_pem_public_key(data[0],backend=default_backend())#passar o 1ºelemento que estava em bytes para chave pública(gy)
  same_shared_key = x.exchange(g_y)
  same_derived_key = HKDF(
  algorithm=hashes.SHA256(),
  length=32,
  salt=None,
  info=b'handshake data',backend=default_backend()
  ).derive(same_shared_key)
  #calcular a partir do gy recebido e a partir do valor de x gerado antes, uma chave partilhada



  #a mensagem do servidor correspondia à concatenação do gy com gx(tudo em bytes)
  mensagem_servidor = data[0] + g_x_bytes 


  #decriptar o criptograma recebido que correspondia ao resultado da cifragem da assinatura
  pt = decrypt(same_derived_key,data[1])


  #verificar a partir da chave pública do servidor, se a chave privada do servidor foi usada para assinar a mensagem gerada no servidor,
  #uma vez que a chave pública e privada do servidor estão associadas uma com a outra
  verify(server_public_key,mensagem_servidor,pt)

  #validar o certificado recebido(a função validate_certificate está comentada, mostrando o seu propósito) 
  if validate_certificate(cert):
  
    #gerar uma mensagem que corresponde à concatenação do gx com o gy recebido(tudo em bytes)
    string = g_x_bytes + data[0]
    signature = sign(client_private_key,string)#assinar a mensagem anterior com a chave privada do certificado do cliente

    c = encrypt(same_derived_key,signature) #encriptar a assinatura a partir da chave partilhada
    data2 = c + b"\r\n\r\n" + client_certificate_as_bytes  
    socket.sendall(data2)#enviar o criptograma e o certificado em bytes para o servidor 
    
    return same_derived_key 
  else:
    return None

  

def process(socket):
  print("Going to do handshake... ", end='')
  k = handshake(socket)
  if k is None:
    print("FAILED.")
    return False
  print("done.")

  while True:#Neste ciclo colocamos uma parte comentada, uma vez que quando corríamos o código apenas permitia ao cliente
            #efetuar uma mensagem, visto que ao clicar no enter, o cliente era desconectado. Portanto, alteramos ou melhor comentamos
            #uma parte para que assim o cliente pudesse enviar várias mensagens. Quando não enviasse uma mensagem, então
            #aí seria desconectado.
    pt = input("Client message: ")
    if len(pt) > 0:
      socket.sendall(encrypt(k, pt.encode("utf-8")))
      
      data = socket.recv(SOCKET_READ_BLOCK_LEN)
      pt = decrypt(k, data)
      print(pt.decode("utf-8"))
      
      '''print("You have been disconnected from the server")
      socket.close()
      break'''
    
    else:
      print("You have been disconnected from the server")
      socket.close()
      break
    '''try:
      data = socket.recv(SOCKET_READ_BLOCK_LEN)
      pt = decrypt(k, data)
      print(pt.decode("utf-8"))
    except:
      print("You have been disconnected from the server")
      socket.close()
      break'''

# Message is bytes.
def sign(private_key, message):#A função sign é necessária no protocolo S-t-S, uma vez que irá retornar uma assinatura realizada
                              #a partir da chave privada do certificado do cliente para a mensagem que corresponde à concatenação
                              # das chave pública do protocolo Diffie-Hellman (gx com gy)
  signature = private_key.sign(
      message,
      PSS(mgf=MGF1(hashes.SHA256()),
                  salt_length=PSS.MAX_LENGTH),
      hashes.SHA256())
  return signature

# Message and signature bytes.
def verify(public_key, message, signature):#A função verify é também necessária para o protocolo S-t-S, uma vez que vai
#verificar a partir da chave pública do certificado que o cliente recebeu, se a chave privada associada a essa chave pública foi 
#usada para assinar a mensagem gerada no servidor que correspondia à concatenação de gy com gx
  
  public_key.verify(
      signature,
      message,
      PSS(mgf=MGF1(hashes.SHA256()),
                  salt_length=PSS.MAX_LENGTH),
      hashes.SHA256())

# Receives the certificate object (not the bytes).
def validate_certificate(certificate, debug = False):
  ca_public_key = None
  ca_cert = None
  with open(path("TC_CA.cert.pem"), "rb") as cert_file:
    ca_cert = load_pem_x509_certificate(cert_file.read(), backend = default_backend())
    ca_public_key = ca_cert.public_key()

  if ca_cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.COUNTRY_NAME)
        return False

  if ca_cert.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.STATE_OR_PROVINCE_NAME)
        return False

  if ca_cert.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.LOCALITY_NAME)
        return False

  if ca_cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.ORGANIZATION_NAME)
        return False

  if ca_cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value:
        debug and print("Mismatched field: %s" %
            NameOID.ORGANIZATIONAL_UNIT_NAME)
        return False

  if ca_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != \
      certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.COMMON_NAME)
        return False

  if certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != "TC Server":
    debug and print("Wrong field (server cert): %s" % NameOID.COMMON_NAME)
    return False

  ca_public_key.verify(
    certificate.signature,
    certificate.tbs_certificate_bytes,
    PKCS1v15(),
    certificate.signature_hash_algorithm)

  return True

def main():
  s = connect()
  process(s)

if __name__ == '__main__':
  main()
