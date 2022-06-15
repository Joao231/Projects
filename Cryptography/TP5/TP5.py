from re import *
from math import *
from decimal import *

# função que recebe dois números e retorna um tuplo, no qual o primeiro elemento corresponde ao máximo divisor comum entre os dois números
def gcdExtended(a, b):  
    
    if a == 0 :   
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a)  
     
    
    x = y1 - (b//a) * x1  
    y = x1  
     
    return gcd,x,y 


#função que descobre os fatores de um número que é passado como argumento. Retorna uma lista que contém todos os fatores do número
def print_factors(x):
	list_factors = []
	for i in range(1, x + 1):
   		if x % i == 0:
   			list_factors.append(i)
	return list_factors

#função que recebe uma lista de fatores de um número e retorna o valor de t necessário para descobrir o valor de d da primitiva RSA
def calculo_t(lista):
	a = lista[1] - 1
	b = lista[2] - 1
	tuplo = gcdExtended(a,b)
	print(tuplo)
	gcd = tuplo[0]
	

	t = (a*b) / gcd
	return t



def texto_limpo(d,n):
	lista = [6876, 90542, 209524, 180723, 68349, 24407, 1927, 183075, 37458,
	77446, 197372, 14551, 148450, 213237, 55592, 56745, 15085, 103645,
	154406, 67322, 2002, 39417, 127400, 178722, 76999, 37458, 79735,
	198950, 161111, 69856, 142050, 22632, 39091, 16950, 168529, 162080,
	83943, 72950, 24407, 207238, 18354, 38021, 186689, 59975, 125376,
	161647, 195221, 44657, 48754, 96701, 72273, 108266, 209524, 16077,
	112276, 69856, 142050, 22632, 84465, 162080, 36730, 27249, 34758,
	79735, 200474, 186981, 99905, 81699, 56760, 56967, 151769, 67608,
	137974, 76557, 187031, 103901, 128885, 148040, 128883, 54852,
	166919, 168279, 44550, 19456, 80788, 141636, 159372, 90688, 35758,
	168747, 142924, 190769, 174948, 2791, 69856, 142050, 22632, 84465,
	162080, 157426, 59221, 65034, 158258, 128733, 108251, 11016, 3376,
	31144, 79735, 162990, 200008, 141687, 136850, 22342, 196127, 117300,
	100284, 64381, 36124, 93455, 97454, 158631, 60424, 91786, 209412,
	57924, 183075, 101801, 55880, 56760, 68019, 164064, 2791, 37458,
	209662, 188390, 68954, 169696, 168434, 115729, 156200, 52926,
	73555, 193991, 37458, 12591, 64130, 61216, 79735, 132216, 194613,
	167517, 196127, 84228, 57242, 122520, 123552, 103901, 176508,
	43547, 145243, 69650, 209524, 202257, 99142, 51498, 162203, 117210,
	127989, 102955, 77762, 24166, 147550
	]# lista que contém os valores do criptograma

	texto_limpo = []
	for num in lista:
		
		T = (int(num)**int(d))%int(n) #calculo do valor que corresponde à decifragem de cada valor do criptograma

		l3 = int(T%27) #calculo do valor de L3 do polinómio mencionado no enunciado do TP5. A maneira como chegamos a esta expressão encontra-se no relatório.
		
		l2 = int(((T-l3)/27)%27)  #calculo do valor de L2 do polinómio mencionado no enunciado do TP5. A maneira como chegamos a esta expressão encontra-se no relatório.
		
		l1 = int((T-(27*l2)-l3)/(27**2))  #calculo do valor de L1 do polinómio mencionado no enunciado do TP5. A maneira como chegamos a esta expressão encontra-se no relatório.
		
		if l1 == 26:#caso o valor seja 26 não podemos usar a função chr(), por isso, obrigamos a que o caractere seja " "(espaço).
			letra1 = " "
		else:
			letra1 = chr(65+l1) #letra correspondente ao valor obtido
		texto_limpo.append(letra1)
		if l2 == 26:
			letra2 = " "
		else:
			letra2 = chr(65+l2)
		texto_limpo.append(letra2)#letra correspondente ao valor obtido
		if l3 == 26:
			letra3 = " "
		else:
			letra3 = chr(65+l3)
		texto_limpo.append(letra3)#letra correspondente ao valor obtido

	texto_limpo1 = "".join(texto_limpo) #converter a lista em string para obter o texto limpo.
	return texto_limpo1

def main():
	n = 213271
	t = calculo_t(print_factors(n))
	d = (t*12 +1)/17
	texto_limpo2 = texto_limpo(d,n)
	print(texto_limpo2)

main()
        