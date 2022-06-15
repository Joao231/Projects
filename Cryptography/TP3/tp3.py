#!/usr/bin/python

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from PIL import Image
import numpy as np
import io

# Gera uma chave (string) aleatória de 16 caracteres 
#key = os.urandom(16)
#iv = os.urandom(16) # Initialization vector: garante a aleatoriedade (garante que ao cifrar o mesmo texto não se obtém o mesmo criptograma)
#filename = "pinguim.bmp"            # foto escolhida
#format = "bmp"                    # foto da imagem

key=b'\x8c\xf3\x1b\xaeS\x9f\x05\x84\xa4\xdb*\x12\xddZ1#'
iv=b'\x9d}\x84\xb3\x1c\r\xbd\x8b\xb8\xfa\xee\xf5\x9f\xb6\x0e\x14'

filename = "new_image.bmp"            
format = "bmp"

fileName = "new_imageECB.bmp"
fileName2 = "new_imageCBC.bmp"

def pad(im_bytes):
	#O espaço de texto simples criptografado AES é um múltiplo inteiro de 16, que não pode ser dividido igualmente, por isso precisa 
	#ser preenchido no ascii correspondente ou seja, se nao for multiplo de 16, ele enfia quantos 0 precisar no fim  ate ser
    padder = padding.PKCS7(128).padder()
    padded_pt = padder.update(im_bytes) + padder.finalize()
    return padded_pt


#Mapeia os dados da imagem para RBG (sistema de cores aditivas em que o Vermelho, o Verde e o Azul são combinados de várias formas de modo a reproduzir um largo espectro cromático)
def trans_formato_RGB(data):
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels



def AES(padded_pt,modo): # O AES gera uma string de 128 bits (= 16 bytes = 16 pixéis).
    # Cifra e o modo.
    if modo=='ECB':
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    elif modo=='CBC':
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    else:
        return -1
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_pt) + encryptor.finalize()
    #decryptor = cipher.decryptor()
    #decryp = decryptor.update(ct) + decryptor.finalize()
    return ct 


def AES_decifra(ct,modo):
    if modo=='ECB':
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    elif modo=='CBC':
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    else:
        return -1
    decryptor = cipher.decryptor()
    decryp = decryptor.update(ct) + decryptor.finalize()
    return decryp 


def cifra(filename,modo):
    im = Image.open(filename)

    #Abrir a imagem bmp e converte-la em imagem RGB
    im_bytes = im.convert("RGB").tobytes()
    im_tamanho = len(im_bytes) # tamanho
    print(im_tamanho)
    print(im.size)
    resultado = trans_formato_RGB(AES(pad(im_bytes),modo)[:im_tamanho]) #Executa o mapeamento de valor de pixel nos dados criptografados
    #resultado = AES(pad(im_bytes),modo)
    #print(type(resultado))
    
    print(len(resultado))
    print(im.mode)
    #Criar uma nova imagem, armazenando o valor correspondente
    im2 = Image.new("RGB", im.size)
    #im2.putdata([tuple(pixel) for pixel in resultado])
    #resultado = resultado.flatten()
    im2.putdata(resultado)

    #Guardar como imagem no formato correspondente
    im2.save(rf"new_image{modo}" + rf".{format}")


def decifra(filename, modo):
    im = Image.open(filename)
    im_bytes = im.convert("RGB").tobytes()
    im_tamanho = len(im_bytes) # tamanho
    print(im_tamanho)
    print(im.size)
    resultado = trans_formato_RGB(AES_decifra(im_bytes,modo)[:im_tamanho])
    print(type(resultado))

    im2 = Image.new("RGB", im.size)
    #im2.putdata([tuple(pixel) for pixel in resultado])
    #resultado = resultado.flatten()
    im2.putdata(resultado)
    im2.save(rf"new_image3{modo}" + rf".{format}")
#------------------------------------------------------------------------------------------------------------------

def main():
    
    #cifra(filename,'ECB')
    #cifra(filename,'CBC')
    #print("Imagem cifrada!")
    print(key)
    print(iv)
    decifra(fileName,'ECB')
    decifra(fileName2,'CBC')
    print("Imagem decifrada!")

main()