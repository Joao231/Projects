from re import *
from math import *

#função que descobre os fatores de um número qu é passado como argumento
def print_factors(x):
	list_factors = []
	for i in range(1, x + 1):
   		if x % i == 0:
   			list_factors.append(i)
	return list_factors



#função que determina o tamanho da chave da cifra
def key_lenght(ciphertext):
	ncaracteres = [" ",",",";",".",")","(","-","\n","?","!"]
	dic ={}
	for caractere in ciphertext:#com este ciclo substitui-se na cifra, todos os caracteres presentes na lista ncaracteres por espaços, uma vez que não é necessário saber padrões de palavras que contenham esse caracteres
		if caractere in ncaracteres:
			ciphertext = ciphertext.replace(caractere," ")
	for i in range(0,len(ciphertext)):#com este ciclo calcular e colocar num dicionário as posições de palavras formadas por três letras que se repetem ao longo do criptograma 
		subseq = ciphertext[i:i+3]
		if subseq in dic:
			continue
		for j in range(i+3,len(ciphertext)-3):
			if subseq == ciphertext[j:j+3]:
				if subseq not in dic:
					dic[subseq] = [i,j]
				else:
					dic[subseq].append(j)				
	dic_fatores = {}
	for element in dic:#com este ciclo colocar num dicionário onde as chaves são os fatores das posições do dicionário anterior e os valores são o número de vezes que esse fatores aparecem
		for i in range(len(dic[element])):
			x = print_factors(dic[element][i])
			for j in x:
				if j not in dic_fatores:
					dic_fatores[j] = 1
				else:
					dic_fatores[j] += 1
	key_lenght = 5# o tamanho da chave foi obtido através da leitura e análise do dicionário em que o fator 5 aparecia muitas vezes sendo, por isso, provável o seu valor como tamanho da chave

	return key_lenght 



def viginere(key_lenght,ciphertext):
	ncaracteres = [" ",",",";",".",")","(","-","\n","?","!"]
	for i in range(0, key_lenght):#obter a letra que mais aparece no subcriptograma, o qual corresponde ao criptograma original, contudo com as letras nas posições 5 em 5
		subseq = ciphertext[i:len(ciphertext):key_lenght]
		letra_maisco= ""
		maximo = 0
		for caractere in subseq:
			if caractere not in ncaracteres:
				co = ciphertext.count(caractere)
				if co > maximo:
					letra_maisco = caractere
		print(letra_maisco)
		shift =[]#lista que contém as letras correspondentes à chave
		letra_shift = chr((((ord(letra_maisco)-65) - (ord("A")-65))%26) +65)#a letra que mais aparece por análise do ciclo anterior é a letra D a qual fizemos corresponder à letra A do alfabeto inglês
		shift.append(letra_shift)
		print(shift)
		index = 0
		subciphertext = ver_cifra(ciphertext,index,shift,key_lenght)
		print(subciphertext)
		variavel = int(input("Se souber uma correspondencia prima 2. Senao prima 1 e continue: "))
		if variavel == 1:
			continue
		if variavel == 2:#assumimos que o utilizador sabe a correspondência 
			a = True
			while a ==True:
				correspondencia = input("Diga qual é o shift: ")
				shift.append(correspondencia)
				index = index + 1
				subciphertext = ver_cifra(subciphertext,index,shift,key_lenght)#função a qual retorna um criptograma onde as letras do criptograma anterior são substituídas pela letra da chave na posição correspondente
				print(subciphertext)
				print(shift)
				if correspondencia == "":
					a = false
				if correspondencia != "":
					continue
			print(shift)
			return shift


def ver_cifra(ciphertext,index,lista,key_lenght):
	ncaracteres = [" ",",",";",".",")","(","-","\n","?","!"]
	shift = lista
	ciphertext = list (ciphertext)
	for i in range(index,len(ciphertext),key_lenght):
		if ciphertext[i] not in ncaracteres:
			ciphertext[i] = chr((((ord(ciphertext[i])-65)-(ord(shift[index])-65))%26)+65)
	ciphertext = "".join(ciphertext)
	return ciphertext



'''esta função foi implementada, uma vez que quando foi descoberta a chave, esta estava a ser aplicada ao primeiro parágrafo,
contudo não estava a ser aplicada ao segundo e, por isso, obtíamos um texto em inglês para o primeiro mas não para o segundo
parágrafo. Portanto, aplicamos a chave agora na forma ['Y','D','F','L','V'], uma vez que à última letra do primeiro parágrafo
foi aplicado o shift correspondente à letra V. Com isto obtemos o texto inglês para o segundo parágrafo.'''
def decode2(ciphertext):
	ncaracteres = [" ",",",";",".",")","(","-","\n","?","!"]
	shift = ['Y','D','F','L','V']
	ciphertext = list (ciphertext)
	for i in range(len(shift)):
		for j in range(i,len(ciphertext),5):
			if ciphertext[j] not in ncaracteres:
				ciphertext[j] = chr((((ord(ciphertext[j])-65)-(ord(shift[i])-65))%26)+65)
	ciphertext = "".join(ciphertext)
	return ciphertext


def file(f):
	with open(f,'r') as f1:
		arquivo1=f1.read()
	return arquivo1


def main():
	ciphertext = file('cripto1.txt')
	ciphertext2 = file('cripto4.txt')
	key_lenght(ciphertext)
	texto_limpo= viginere(key_lenght(ciphertext),ciphertext)
	print(texto_limpo)
	texto_limpo2 = decode2(ciphertext2)
	print(texto_limpo2)
main()



      
