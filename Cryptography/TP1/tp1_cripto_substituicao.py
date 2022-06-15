
from re import *
def substituicao(ciphertext,letra_ingles,lista_ingles):
	dic1= {}
	dic1['A'] = 8.2
	dic1['B'] = 1.5
	dic1['C'] = 2.8
	dic1['D'] = 4.3
	dic1['E'] = 12.7
	dic1['F'] = 2.2
	dic1['G'] = 2.0
	dic1['H'] = 6.1
	dic1['I'] = 7.0
	dic1['J'] = 0.2
	dic1['K'] = 0.8
	dic1['L'] = 4.0
	dic1['M'] = 2.4
	dic1['N'] = 6.7
	dic1['O'] = 1.5
	dic1['P'] = 1.9
	dic1['Q'] = 0.1
	dic1['R'] = 6.0
	dic1['S'] = 6.3
	dic1['T'] = 9.1
	dic1['U'] = 2.8
	dic1['V'] = 1.0
	dic1['W'] = 2.4
	dic1['X'] = 0.2
	dic1['Y'] = 2.0
	dic1['Z'] = 0.1
	lista_char =[" ",",",";",".",")","(","-","\n"]
	maximo = 0
	lista = lista_ingles
	lista_com_posicoes=[]
	letra_maisco= ""
	for caractere in ciphertext:   #encontrar a letra que mais ocorre no criptograma
		if caractere not in lista and caractere not in lista_char:
			co = ciphertext.count(caractere)
			if co > maximo:
				letra_maisco = caractere
	print(letra_maisco)
	lista_com_posicoes = posicoes(letra_maisco,ciphertext)
	subciphertext = ciphertext.replace(letra_maisco, letra_ingles)
	lista.append(letra_ingles)
	print(subciphertext)
	variavel = int(input(("Deseja continuar. Se sim prima 2 se souber a proxima correspondencia. Se nao souber prima 1. Se quiser acabar senao prima 0")))
	dic2 = {}    #dicionario que contem como chaves as letras do criptograma e como valores as letras do alfabeto inglês que eles correspondem
	dic2[letra_maisco] = letra_ingles
	if variavel == 2:
		a = True
		while a ==True:
			letra_cifra = input("Introduza a letra da cifra que quer decifrar: ")
			letra_ing = input("Introduza a letra inglesa para decifrar: ")
			dic2[letra_cifra] = letra_ing
			lista.append(letra_ing)
			cripto = subs(subciphertext,letra_cifra,letra_ing,lista_com_posicoes)
			lista_com_posicoes = lista_com_posicoes+(posicoes(letra_cifra,subciphertext))

			print(cripto)
			print(dic2)
			if letra_cifra == "":
				a = false
			if letra_cifra != "":
				subciphertext = cripto


	return subciphertext


#retorna uma lista com as posicoes onde foram feitas as substituicoes para que na proxima iteracao nao ocorram substituicoes nessas posicoes
def posicoes(letra,cifra):
	lista_posicoes=[]
	for i in range(len(cifra)):
		if cifra[i] == letra:
			lista_posicoes.append(i)
	return lista_posicoes		



#substituir a letra da cifra dado como input pela letra inglesa dada como input e recebe uma lista com as posicoes onde já foram feitas substituicoes 
def subs(ciphertext,letra_cifra, letra_inglesa,lista):
	ciphertext = list(ciphertext)
	for i in range(len(ciphertext)):
		if (i not in lista) and (ciphertext[i] == letra_cifra):
			ciphertext[i] = letra_inglesa			
	ciphertext = "".join(ciphertext)
	return ciphertext



#Ler o ficheiro que contem o criptograma
def file(f):
	with open(f,'r') as f1:
		arquivo1=f1.read()
	return arquivo1


def main():
	ciphertext = file('cripto3.txt')
	substituicao(ciphertext,'S',[])
main()