from re import *
from math import *

#abrir o ficheiro que contém o criptograma 2 que foi cifrado pela cifra affine
def file(f):
	with open(f,'r') as f1:
		arquivo1=f1.read()
	return arquivo1

#função que calcula a inersa de um número que, no final de contas, será a inversa do valor de a dado como argumento
def inversa(numero): 
	for i in range(0,27):
		if ((numero*i) % 26)==1:# para um numero ser o inverso de outra: o produto dos dois mod 26 deverá ser igual a 1
			return i
		
	sys.exit("Nao existe inversa para %d" %numero)	

#função que fará o brute force attack. Para cada valor de a(todos os números ímpares de 0 a 26 excluindo o 13) poderá haver 26 valores possíveis de b 
def affine(ciphertext):
	ncaracteres = [" ",",",";",".",")","(","-","\n","!"]
	for a in range(0,26):
		if (a%2 != 0) and (a != 13):
			for b in range(0,26):
				continuar = int(input("Deseja continuar prima 1 senao prima 0: "))
				plaintext=" "
				if continuar == 0:
					exit();
				if continuar==1:
					inversa1 = inversa(a)
					for caractere in ciphertext:
						if caractere not in ncaracteres:
							num = ord(caractere)
							car_plaintext = chr(((inversa1*(num -65 - b)) % 26)+65) #usar a expressão que está associada à cifra de affine
							plaintext += car_plaintext
						else:
							plaintext += caractere
					
				print(plaintext)		
	

def main():
	ciphertext = file('cripto2.txt')
	affine(ciphertext)
main()