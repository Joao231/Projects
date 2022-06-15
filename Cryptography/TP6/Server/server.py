#!/usr/bin/python

import socket
import threading
import signal, sys
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

# An useful function to open files in the same dir as script...
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def path(fname):
  return os.path.join(__location__, fname)

host = "localhost"
port = 8080
connections = []
total_connections = 0

# RFC 3526's parameters. Easier to hardcode...
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2
params_numbers = dh.DHParameterNumbers(p,g)
parameters = params_numbers.parameters(backend=default_backend())

AES_BLOCK_LEN = 16 # bytes
AES_KEY_LEN = 32 # bytes
PKCS7_BIT_LEN = 128 # bits
SOCKET_READ_BLOCK_LEN = 4096 # bytes

def signal_handler(sig, frame):
  print('You pressed Ctrl+C; bye...')
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class Client(threading.Thread):
  def __init__(self, socket, address, id, name):
      threading.Thread.__init__(self)
      self.socket = socket
      self.address = address
      self.id = id
      self.name = name

      # Don't wait for child threads (client connections) to finish.
      self.daemon = True

      self.dh_y = None
      self.dh_g_y = None
      self.dh_g_y_as_bytes = None
      self.dh_g_x_as_bytes = None
      self.dh_g_x = None

      # Symmetric (shared) key
      self.key = None

      # Private key from the server's certificate
      self.private_key = None
      with open(path("TC_Server.key.pem"), "rb") as key_file:
        self.private_key = load_pem_private_key(key_file.read(), password=None,backend=default_backend())

      # Certificate and public key from the server's certificate
      self.public_key = None
      self.certificate_as_bytes = None
      with open(path("TC_Server.cert.pem"), "rb") as cert_file:
        self.certificate_as_bytes = cert_file.read()
        cert = load_pem_x509_certificate(self.certificate_as_bytes,backend=default_backend())
        self.public_key = cert.public_key()

      self.client_certificate = None
      self.client_public_key = None
    
  def __str__(self):
      return str(self.id) + " " + str(self.address)

  # Receives and returns bytes.
  def encrypt(self, m):
    

    padder = padding.PKCS7(PKCS7_BIT_LEN).padder()
    padded_data = padder.update(m) + padder.finalize()
    iv = os.urandom(AES_BLOCK_LEN)
    cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv),backend = default_backend())
    encryptor = cipher.encryptor()

    ct = encryptor.update(padded_data) + encryptor.finalize()
    return iv+ct

  # Receives and returns bytes.
  def decrypt(self, c):
    

    iv, ct = c[:AES_BLOCK_LEN], c[AES_BLOCK_LEN:]
    cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(PKCS7_BIT_LEN).unpadder()
    pt = unpadder.update(pt) + unpadder.finalize()
    return pt

  def handshake(self, debug = False):



    #o servidor recebe o gx do cliente em bytes
    self.dh_g_x_bytes = self.socket.recv(SOCKET_READ_BLOCK_LEN)
    self.dh_g_x = load_pem_public_key(self.dh_g_x_bytes,backend=default_backend())#passar o resultado anterior para chave pública
    
    #gerar um número, a partir dos parâmetros hard-coded no início do ficheiro, que corresponde ao y do protocolo Diffie-Hellman
    self.dh_y = parameters.generate_private_key()
    
    


    shared_key = self.dh_y.exchange(self.dh_g_x)
    derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',backend=default_backend()
    ).derive(shared_key)
    #calcular a partir do gx recebido e a partir do valor de y gerado antes, uma chave partilhada

    self.key = derived_key
    


    #gerar a chave pública a partir do número gerado anteriormente. Será o gy do protocolo Diffie-Hellman que será enviado para o cliente
    self.dh_g_y = self.dh_y.public_key()

    #passar o resultado anterior para bytes
    self.dh_g_y_as_bytes = self.dh_g_y.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    


    #gerar uma mensagem que corresponde à concatenação do gy com o gx recebido(tudo em bytes)
    data =  self.dh_g_y_as_bytes + self.dh_g_x_bytes
    signature = self.sign(data)#assinar a mensagem anterior com a chave privada do certificado do servidor
    
    
    c = self.encrypt(signature)#encriptar a assinatura a partir da chave partilhada
    
    data2 = self.dh_g_y_as_bytes + b"\r\n\r\n" + c + b"\r\n\r\n" + self.certificate_as_bytes

    
    self.socket.sendall(data2)#enviar o gy, o criptograma e o certificado em bytes para o cliente 


    conjunto = self.socket.recv(SOCKET_READ_BLOCK_LEN)#recebe o criptograma e o certificado do cliente em bytes
    conjunto1 = conjunto.split(sep=b"\r\n\r\n")#fazer o split do resultado anterior(1º elemento corresponde ao criptograma da assinatura feita no cliente, 2º elemento corresponde
  #ao certificado do cliente)



    #passar o certificado do cliente para objecto, uma vez que foi recebido em bytes
    self.client_certificate = load_pem_x509_certificate(conjunto1[1],backend=default_backend())


    #extrair a chave pública a partir do certificado do cliente
    self.client_public_key = self.client_certificate.public_key()
    


    #decriptar o criptograma recebido que corresponde ao resultado da cifragem da assinatura realizada do lado do cliente
    pt = self.decrypt(conjunto1[0])



    #a mensagem do cliente correspondia à concatenação do gx com gy(tudo em bytes)
    mensagem_cliente = self.dh_g_x_bytes + self.dh_g_y_as_bytes



    #verificar a partir da chave pública do cliente se a chave privada do cliente foi usada para assinar a mensagem gerada no cliente,
    #uma vez que a chave pública e privada do cliente estão associadas uma com a outra
    self.verify(self.client_public_key,mensagem_cliente,pt)
    

    #validar o certificado recebido(a função validate_certificate está comentada, mostrando o seu propósito) 
    if self.validate_certificate():
      
        return True
    else:
      return None



    

  def run(self):
    print("Going to do handshake for client " + str(self.address) + "... ", end='')
    hs = self.handshake()
    if hs is None or self.key is None:
      print("FAILED.")
      print("Client " + str(self.address) + ": closing connection.")
      self.socket.close()
      connections.remove(self)
      return False
    print("done.")

    data = ""
    while True:
      try:
        data = self.socket.recv(SOCKET_READ_BLOCK_LEN)
      except:
        pass
      if len(data) > 0:
        pt = self.decrypt(data)
        print("ID " + str(self.id) + ": " + pt.decode("utf-8"))

        self.socket.sendall(self.encrypt("Server received: ".encode("utf-8") + pt))
      else:
        print("Client " + str(self.address) + " has disconnected")
        self.socket.close()
        connections.remove(self)
        break

  # Message is bytes.
  def sign(self, message):#A função sign é necessária no protocolo S-t-S, uma vez que irá retornar uma assinatura realizada
                          #a partir da chave privada do certificado do servidor para a mensagem que corresponde à concatenação
                          # das chaves públicas do protocolo Diffie-Hellman (gy com gx)
    signature = self.private_key.sign(
      message,
      PSS(mgf=MGF1(hashes.SHA256()),
                  salt_length=PSS.MAX_LENGTH),
      hashes.SHA256())
    return signature





  # m and sig are bytes.
  def verify(self, public_key, m, sig):#A função verify é também necessária para o protocolo S-t-S, uma vez que vai
#verificar a partir da chave pública do certificado que o servidor recebeu, se a chave privada associada a essa chave pública foi 
#usada para assinar a mensagem gerada no cliente que correspondia à concatenação de gx com gy
    public_key.verify(
      sig,
      m,
      PSS(mgf=MGF1(hashes.SHA256()),
                  salt_length=PSS.MAX_LENGTH),
      hashes.SHA256())




  # Receives the certificate object (not the bytes).
  def validate_certificate(self, debug = False):
    certificate = self.client_certificate
                                        #In essence, the certificate authority is responsible for saying 
                                        #"yes, this person is who they say they are, and we, the CA, certify that"
    ca_public_key = None                #certificate authorities são entidades que armazenam chaves públicas e os seus donos.
                                        #Quando o servidor recebe a chave pública a partir do certificado do cliente, recebe
    ca_cert = None                      #também uma assinatura digital dessa chave(X.509 certificate). Como o servidor já possui a chave pública do CA, então
                                        #,consequentemente, pode verificar a assinatura digital feita na chave pública que recebeu e, por isso, 
                                        #pode acreditar no certificado e na chave pública que recebeu. Como o cliente usa a chave pública 
                                        #que a CA já certificou, então qualquer adversário só podia usar a mesma chave pública. No entanto como o adversário
                                        #não conhece a correspondente chave privada, logo não consegue criar uma assinatura necessária para verificar a sua autenticidade. 

    with open(path("TC_CA.cert.pem"), "rb") as cert_file:                                 
      ca_cert = load_pem_x509_certificate(cert_file.read(),backend = default_backend())  #digital certificate
      ca_public_key = ca_cert.public_key()#chave pública do certificado digital

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

    if certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != "TC Client":
      debug and print("Wrong field (server cert): %s" % NameOID.COMMON_NAME)
      return False


      #A função validate_certificate irá retornar False se a identidade do certificado do cliente que recebeu não corresponder 
      #àquela que está descrita no certificado digital. Para tal é necessário comparar características como: o nome, identidade, localidade,
      #organização, estado ou província ou outras que são necessárias para provar a identidade do certificado que recebeu.


    ca_public_key.verify(
      certificate.signature,
      certificate.tbs_certificate_bytes,
      PKCS1v15(),
      certificate.signature_hash_algorithm)

    #A função validate_certificate só retornará True caso a chave pública do certificado digital verificar a assinatura digital contida
    #na chave pública do certificado que recebeu, a qual foi assinada com a correspondente chave privada.


    return True

def main():
  # Create new server socket. Set SO_REUSEADDR to avoid annoying "address
  # already in use" errors, when doing Ctrl-C plus rerunning the server.
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(5)

  # Create new thread to wait for connections.
  while True:
    client_socket, address = sock.accept()
    global total_connections
    connections.append(Client(client_socket, address, total_connections, "Name"))
    connections[len(connections) - 1].start()
    total_connections += 1
  for t in connections:
    t.join()
  
if __name__ == '__main__':
  main()
