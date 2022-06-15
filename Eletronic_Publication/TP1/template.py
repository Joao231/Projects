from re import *
import re
import jinja2  as j2
import lxml
from bs4 import BeautifulSoup as bs
	
'''funcao que recebe atributos, sendo estes colocados no template. Para nós existem dois tipos de reports. Num tipo existe uma
estrutura com titulo, subtitulo, imagem de capa, autores, informaçao do curso, introducao, estrutura do tipo: questao e respetiva resposta e resolucao,
referencias e um link para o relatorio em pdf.
 '''

def preenche1(tit,subt,iimage,authors,Masters,Introduction,questions,references,link):
	t1 = j2.Template( """
	<!DOCTYPE html>
	<html>
	<head>
		<style>
		body{
		background-color: linen;
		}
		h1{
		color: red;
		}
		<meta charset="UTF-8"/>
		<title> {{tit}} </title>
	</style>
	</head>
	<body>
		<img alt="logotipo EEUM" src="https://i.ibb.co/9njRV20/EEUM.png"/>
		<h1 style="text-align: center;"> {{tit}} </h1><br>
		<h2 style="text-align: center;"> {{subt}} </h2><br>
		<center><img src="{{iimage}}"/></center><br>
	
		<h3>Autores</h3>
		<ul>
			{% for el in authors  %}
				<li> {{el['name']}} : {{el['number']}} </li>
			{% endfor %}
		</ul>
		<h3 style="text-align: center;"> {{Masters}} </h3><br>
		<center><a href="#section1">Introdução</a>
        <a href="#section2">Referências</a></center>
        <hr>
		<p id="section1" align="justify">{{Introduction}}</p>
		<ol>
			{% for el in questions  %}
				<li><h3>{{el['enunciated']}}</h3></li>
				<p>{{el['answer']}}</p>
				<p>{{el['resolution']}}</p>
			{% endfor %}
		</ol>
		<h2 id="section2" style="text-align: center;">Referências</h2>
		<ul>
			{% for el in references  %}
				<li><h4><a href="{{el}}" target="_blank">{{el}}</a></h4></li>
			{% endfor %}
		</ul><br>
		<center>
		<h4><a href="{{link}}" target="_blank">Aceder ao relatório completo em PDF</a></h4>
		<a href="javascript:history.back()">Go back</a><br><br>
		</center>
	</body>
	</html>

	""")
	return(t1.render(tit=tit, subt = subt, iimage=iimage, authors=authors, Masters = Masters, Introduction = Introduction, questions = questions, references = references, link=link))
	

'''funcao que recebe atributos, sendo estes colocados no template. Para nós existem dois tipos de reports. Num outro tipo existe uma
estrutura com titulo, subtitulo, imagem de capa, autores, informaçao do curso, introducao, texto com informacao relevante do assunto do relatorio,
 imagem final, conclusao, referencias e um link para o relatorio em pdf.'''
def preenche2(tit,subt,iimage,authors,Masters,content,image,Conclusion,references,link):
	t2 = j2.Template( """
	<!DOCTYPE html>
	<html>
	<head>
		<style>
		body{
		background-color: linen;
		}
		h1{
		color: red;
		}
		<meta charset="UTF-8"/>
		<title> {{tit}} </title>
	</style>
	</head>
	<body>
		<img alt="logotipo EEUM" src="https://i.ibb.co/9njRV20/EEUM.png"/>
		<h1 style="text-align: center;"> {{tit}} </h1><br>
		<h2 style="text-align: center;"> {{subt}} </h2><br>
		<center><img src="{{iimage}}"/></center><br>
	
		<h3>Autores</h3>
		<ul>
			{% for el in authors  %}
				<li> {{el['name']}} : {{el['number']}} </li>
			{% endfor %}
		</ul>
		<h3 style="text-align: center;"> {{Masters}} </h3><br>
		<center><a href="#section1">Conclusão</a>
        <a href="#section2">Referências</a></center>
        <hr>
		{% for el in content  %}
			<p align="justify">{{el}}</p>
		{% endfor %}
		<center><img src={{image}}></center>
		<p id="section1" align="justify">{{Conclusion}}</p>
		<h2 id="section2" style="text-align: center;">Referências</h2>
		<ul>
			{% for el in references  %}
				<li><h4><a href="{{el}}" target="_blank">{{el}}</a></h4></li>
			{% endfor %}
		</ul>

		<center>
		<h4><a href="{{link}}" target="_blank">Aceder ao relatório completo em PDF</a></h4>
		<a href="javascript:history.back()">Go back</a><br><br>
		</center>
	</body>
	</html>

	""")
	return(t2.render(tit=tit, subt = subt, iimage=iimage,authors=authors, Masters = Masters, content = content, image=image, Conclusion = Conclusion, references = references, link=link))

''' funcao que recebe um dicionario que possui como chaves relatorio1, relatorio2, relatorio3 e assim sucessivamente, sendo
os respetivos valores o subtitulo do relatorio respetivo.'''
def gera_index(dic_subt):
	t = j2.Template("""
	<!DOCTYPE html> 
	<html>
		<head>
			<style>
			body{
			background-color: linen;
			}
			h1{
			color: red;
			}
			<title>PORTFÓLIO</title>
			<meta charset="utf-8"/>
			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		</style>		
		</head>

		<body>
			<img alt="logotipo EEUM" src="https://i.ibb.co/9njRV20/EEUM.png"/>
			<h1 style="text-align: center;">PORTFÓLIO</h1>
			<hr>
			<br><br>
			{% for el in dic_subt  %}
				<center><h2><a href="{{el}}.html">{{dic_subt[el]}}</a></h2><br></center>
			{% endfor %}

			<center><h2><a href="autores_relatorios.html">Autores dos Relatórios</a></h2><br></center>
			<center><h2><a href="Description.html" target="_blank">Description</a></h2><br></center><br><br><br><br>
			
			
			<h2 style="text-align: center;">Mestrado Integrado em Engenharia Biomédica</h2>
			<h2 style="text-align: center;">Publicação Eletrónica 2020/2021</h2> 
			<center><h2><a href="dados_pessoais.html">Autores do Portfólio</a></h2><br><br></center>

		</body>

	</html>""")

	return(t.render(dic_subt = dic_subt))

'''funcao que recebe um dicionario que contem como chaves relatorio1, relatorio2, relatorio3 e assim sucessivamente e, sendo os valores
uma lista, cujos elementos são dicionarios que contem informacao dos autores do respetivo relatorio como o nome, numero, telefone e email.'''
def gera_autores(dic_autores):
	t = j2.Template("""
		<!DOCTYPE html>
		<html>
			<head>
				<style>
				body{
				background-color: LightYellow;
				}
				<title>AUTORES DOS RELATÓRIOS</title>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
			</style>
			</head>

			<body>
				<img alt="logotipo EEUM" src="https://i.ibb.co/9njRV20/EEUM.png"/>
				<h1 style="text-align: center;">AUTORES DOS RELATÓRIOS</h1>
				<hr>
				{% for el in dic_autores  %}
					{% for i in dic_autores[el]  %}
						<center><h3><a href="{{el}}.html">{{i['name']}}</a></h3>
						<p>Número: {{i['number']}}</p>
						<p>Email: <a href="mailto:{{i['email']}}"> {{i['email']}}</a></p>
						<p>Telefone: <a href="tel:{{i['telephone']}}">{{i['telephone']}}</a></p><br>
					{% endfor %}

				{% endfor %}

				<a href="javascript:history.back()">Go back</a><br><br>
				</center>

			</body>

		</html>""")
	return(t.render(dic_autores = dic_autores))


'''funcao que recebe um dicionario que contem como chaves o texto da tag description de cada relatorio, sendo os seus valores uma lista
cujos valores são tuplos em que no primeiro index se encontra o relatorio e no index seguinte o subtitulo desse mesmo relatorio.'''
def gera_description(dic_descript):
	t = j2.Template("""
	<!DOCTYPE html> 
	<html>
		<head>
			<style>
				body{
				background-color: LightYellow;
				}
				h1{
					color:maroon;
				}
			<title>Description</title>
			<meta charset="utf-8"/>
			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		</style>
		</head>

		<body>
			<img alt="logotipo EEUM" src="https://i.ibb.co/9njRV20/EEUM.png"/>
			<h1 style="text-align: center;">Description</h1>
			<hr>
			<br>
			{% for el in dic_descript  %}
				<br><br><center><h3>{{el}}</h3></center>
				{% for i in dic_descript[el]  %}
					<center><h3><a href="{{i[0]}}.html">{{i[1]}}</a></h3></center>
				{% endfor %}
			{% endfor %}
			<center><br><br><br><a href="index.html">Go back</a><br></center>

		</body>

	</html>""")

	return(t.render(dic_descript = dic_descript))



'''funcao que recebe um ficheiro e retorna uma string com o conteudo desse ficheiro'''
def abrir(file):
	with open(file,'r') as f:
		a=f.read()
	return a



'''funcao que recebe um report e uma tag desse report e retorna o conteudo dessa mesma tag.'''
def tags(report,tag):
	info =[]
	for miolo in findall(rf'<{tag}>(.*)</{tag}>',report):
		info.append(miolo)
	if info:
		resultado = info[0]
		return resultado




''' funcao que recebe uma lista e um report e retorna um dicionario cujas chaves são cada elemento na lista e os valores sao
o conteudo que se encontra dentro desse elemento '''
def extract_dict(l,report): # devolve dicionário

	info = {}
	for elem in l:
		v=search(rf"<{elem}>((?:.|\n)*?)</{elem}>",report)
		if v:
			info[elem]=v[1]

	return info




'''funcao que recebe um dicionario e uma tag e retorna uma lista com o conteudo que se ecnontra dentro dessa tag'''
def extrai_listaH(xml,tag):

	info = []

	for miolo in findall(rf'<{tag}>((?:.|\n)*?)</{tag}>',xml):
		info.append(miolo)

	return info






def main():
	f = abrir("portfolio.xml")#abrir ficheiro 
	reports = extrai_listaH(f,'report')#retorna uma lista em que em cada index, está presente o conteudo de um report no seu todo
	ficheiro = "relatorio"


	'''loop que vai iterar para elemento da lista, ou seja, para cada report e inicializa as varias variaveis que serao depois necessárias
	substituir nos templates. Verifica pela tag tipo qual e o tipo do report e vai buscar o conteudo para cada respetiva tag necessaria.
	Depois verifica se de facto esse conteudo existe e se exista cada variavel passa a ter esse valor respetivamente. No final do loop
	cria-se um ficheiro escreve-se o conteudo nesse ficheiro depois de se fazer o render no template e a extensao é .html para se 
	abrir uma pagina html.'''
	for i in range(len(reports)):
		tipo = tags(reports[i],'tipo')
		tit = ""
		subt=""
		iimage=""
		authors=""
		Masters=""
		content=""
		image=""
		Conclusion =""
		references = ""
		link=""
		Introduction=""
		questions=""
		if tipo == "2":
			if tags(reports[i],'title'):
				tit =tags(reports[i],'title')

			if tags(reports[i],'subtitle'):
				subt =tags(reports[i],'subtitle')

			if tags(reports[i],'iimage'):
				iimage = tags(reports[i],'iimage')

			if extract_dict(['authors'],reports[i]):
				dic = extract_dict(['authors'],reports[i])
				if extrai_listaH(dic['authors'],'author'):
					aux = extrai_listaH(dic['authors'],'author')
					if  [extract_dict(['name','number'],el) for el in aux]:
						authors = [extract_dict(['name','number'],el) for el in aux]

			if tags(reports[i],'masters'):
				Masters = tags(reports[i],'masters')

			if extract_dict(['content'],reports[i]):
				dic1 = extract_dict(['content'],reports[i])
				if extrai_listaH(dic1['content'],'text'):
					content = extrai_listaH(dic1['content'],'text')

			if tags(reports[i],'image'):
				image=tags(reports[i],'image')

			if  tags(reports[i],'conclusion'):
				Conclusion = tags(reports[i],'conclusion')

			if tags(reports[i],'references'):
				references= tags(reports[i],'references')
				references = references.split(";")

			if tags(reports[i],'link'):
				link= tags(reports[i],'link')


			conteudo = preenche2(tit,subt,iimage,authors,Masters,content,image,Conclusion,references,link)
			j = str(i+1)
			my_file = open(ficheiro + j+".html","w")
			my_file.write(conteudo)
			my_file.close()


		if tipo == "1":
			if tags(reports[i],'title'):
				tit =tags(reports[i],'title')

			if tags(reports[i],'subtitle'):
				subt =tags(reports[i],'subtitle')

			if tags(reports[i],'iimage'):
				iimage = tags(reports[i],'iimage')

			if extract_dict(['authors'],reports[i]):
				dic = extract_dict(['authors'],reports[i])
				if extrai_listaH(dic['authors'],'author'):
					aux = extrai_listaH(dic['authors'],'author')
					if  [extract_dict(['name','number'],el) for el in aux]:
						authors = [extract_dict(['name','number'],el) for el in aux]

			if tags(reports[i],'masters'):
				Masters = tags(reports[i],'masters')

			if tags(f,'introduction'):
				Introduction= tags(f,'introduction')

			if extract_dict(['questions'],reports[i]):
				dic1 = extract_dict(['questions'],reports[i])
				if extrai_listaH(dic1['questions'],'question'):
					aux1 = extrai_listaH(dic1['questions'],'question')
					if [extract_dict(['enunciated','answer','resolution'],el) for el in aux1]:
						questions = [extract_dict(['enunciated','answer','resolution'],el) for el in aux1]


			if tags(reports[i],'references'):
				references= tags(reports[i],'references')
				references = references.split(";")

			if tags(reports[i],'link'):
				link= tags(reports[i],'link')


			conteudo = preenche1(tit,subt,iimage,authors,Masters,Introduction,questions,references,link)
			j = str(i+1)
			my_file = open(ficheiro + j +".html","w")
			my_file.write(conteudo)
			my_file.close()

	print("Gerados",i+1, "relatorios com sucesso!")



	'''loop que itera para cada relatorio e encontra o conteudo da tag subtitulo. Cria-se um dicionario cujas chaves são o relatorio
	e os valores o respetivo subtitulo.'''
	ficheiro = "Index"
	dic_subt = {}
	for i in range(len(reports)):
		report = "relatorio" + str(i+1)
		subt = tags(reports[i],'subtitle')
		dic_subt[report] = subt
	conteudo = gera_index(dic_subt)
	my_file = open(ficheiro + ".html","w")
	my_file.write(conteudo)
	my_file.close()

	print("Index gerado com sucesso!")




	'''loop que itera para cada relatorio e cria-se uma variavel authors que corresponde ao valores da chave authors no dicionario 
	criado. A variavel authors contem informação relativa aos autores de cada relatorio.'''
	ficheiro = "Autores_relatorios"
	dic_autores = {}
	for i in range(len(reports)):
		report = "relatorio" + str(i+1)
		dic = extract_dict(['authors'],reports[i])
		aux = extrai_listaH(dic['authors'],'author')
		dic['authors'] = [extract_dict(['name','number','email','telephone'],el) for el in aux]
		authors = dic['authors']
		dic_autores[report] = authors
			
	conteudo = gera_autores(dic_autores)
	my_file = open(ficheiro + ".html","w")
	my_file.write(conteudo)
	my_file.close()


	'''loop que itera para cada relatorio e cria-se um dicionario cujas chaves são o conteudo da tag description de cada relatorio e
	as respetivas chaves são uma lista em que cada elemento é um tuplo em que o primeiro index corresponde ao relatorio e o segundo
	index corresponde ao subtitulo do respetivo relatorio.'''
	ficheiro = "Description"
	dic_descript = {}
	for i in range(len(reports)):
		report = "relatorio" + str(i+1)
		subt = tags(reports[i],'subtitle')
		descript = tags(reports[i],'description')
		if descript not in dic_descript:
			dic_descript[descript] = [(report,subt)]
		else:
			dic_descript[descript].append((report,subt))
	conteudo = gera_description(dic_descript)
	my_file = open(ficheiro + ".html","w")
	my_file.write(conteudo)
	my_file.close()


main()
	
