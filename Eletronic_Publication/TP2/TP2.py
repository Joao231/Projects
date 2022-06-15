from flask import Flask, render_template, request
#export FLASK_ENV=development
#export FLASK_APP=app.py
import json
import requests
import jinja2 as j2
import random
import shelve
import re
#-*- coding: utf-8 -*- 


app=Flask(__name__)



#route para renderizar a nossa página "index" onde aparecem butons para podermos carregar e que, por sua vez, levam-nos para outras routes.
#Temos butons como: Relatórios para ver os relatorios e pesquisar palavras, Autores dos relatórios para ver os autores dos relatorios, Description para ver
#relatorios por descrições, Adicionar Relatórios para poder adicionar um relatorio, Update de relatórios para alterar os relatorios
#que já existem, Remover Relatórios para remover os relatorios que quiser e Autores do Projeto onde se encontram as informações dos autores deste projeto
@app.route('/')
def index():
	return render_template('index.html',title = 'Relatorios')



#route que permite obter uma lista de listas. Cada sublista contém toda informação relativa a um relatório. Portanto, a lista que
#é retornada contém tantas sublistas quanto relatórios que existem na nossa "base de dados". A primeira sublista contém o conteúdo 
#do relatório1, a segunda sublista contém todo o contéudo do relatório2 e assim sucessivamente
@app.route('/api/relatorios')
def api_relatorios():
	s = shelve.open("relatorios.db")
	ps = list(s.keys())#as chaves que existem no ficheiro "relatorios.db" contidas numa lista
	ls = []
	lista_ordenada = []
	contador = 0

	for relatorio in ps:
		numero = relatorio[-1]
		ls.append(int(numero))

	ls.sort()
	
	for numero in ls:
		for k in range(len(ps)):
			if str(numero) in ps[k]:
				lista_ordenada.append(ps[k])#processamento de forma a obter uma lista ordenada, de forma a termos uma lista
											#em que o primeiro elemento fosse "relatorio1", o segundo fosse "relatorio2" e assim sucessivamente.

	
	lista = []
	i = 0
		
	for relatorio in s:
		title = ""
		subtitle = ""
		iimage = ""
		authors = ""
		masters = ""
		introduction = ""
		content = ""
		questions = ""
		image = ""
		Conclusion = ""
		references = ""
		link = ""
		description = ""
		lista_rel = []
		chave = lista_ordenada[i]
		tipo = s[chave]["tipo"]
		if "title" in s.get(chave):
			title = s[chave]["title"]#title corresponde a uma string
		if "subtitle" in s.get(chave):
			subtitle = s[chave]["subtitle"]#subtitle corresponde a uma string
		if "iimage" in s.get(chave):
			iimage = s[chave]["iimage"]#iimage corresponde a uma string
		if "authors" in s.get(chave):
			auts = s[chave]["authors"]
			authors=[]#authors corresponde a uma lista, cujos elementos são dicionários que contém informação de cada autor do respetivo relatorio
			for aut in auts:
				author = {}
				author["name"] = aut[0]
				author["number"] = aut[1]
				author["email"] = aut[2]
				author["telephone"] = aut[3]
				authors.append(author)
		if "masters" in s.get(chave):
			masters = s[chave]["masters"]#masters corresponde a uma string
		if "introduction" in s.get(chave):
			introduction = s[chave]["introduction"]#introduction corresponde a uma string
		if "content" in s.get(chave):
			content = s[chave]["content"]#content corresponde a uma lista, cujos elementos correspondem a cada parágrafo no contéudo
		if "questions" in s.get(chave):
			quests = s[chave]["questions"]
			questions = []#questions corresponde a uma lista, cujos elementos são dicionários com informação de cada questão
			for quest in quests:
				question = {}
				question["enunciated"] = quest[0]
				question["answer"] = quest[1]
				question["resolution"] = quest[2]
				questions.append(question)
		if "image" in s.get(chave):
			image = s[chave]["image"]#image corresponde a uma string
		if "conclusion" in s.get(chave):
			Conclusion = s[chave]["conclusion"]#conclusion corresponde a uma string
		if "references" in s.get(chave):
			references = s[chave]["references"]#references corresponde a uma lista, cujos elementos são uma referencia
		if "link" in s.get(chave):
			link = s[chave]["link"]#link corresponde a uma string
		if "description" in s.get(chave):
			description = s[chave]["description"]#description corresponde a uma lista, cujos elementos correspondem a um descrição

		lista_rel.append(tipo)
		lista_rel.append(title)
		lista_rel.append(subtitle)
		lista_rel.append(iimage)
		lista_rel.append(authors)
		lista_rel.append(masters)
		lista_rel.append(introduction)
		lista_rel.append(content)
		lista_rel.append(questions)
		lista_rel.append(image)
		lista_rel.append(Conclusion)
		lista_rel.append(references)
		lista_rel.append(link)
		lista_rel.append(description)
		lista.append(lista_rel)
		i +=1
	s.close()
	return json.dumps(lista)#passar a lista para formato json. A lista foi já explicada no ínicio da função




#route chamada quando se carrega em Relatórios na página index
@app.route('/relatorios')
def relatorios_view():

	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função anterior
	lista = json.loads(res.content)#passar o objeto para lista

	if len(lista) == 0:
		string = "Não existem relatórios! É necessário adicionar relatórios!"
		return render_template("erros.html", string = string)
	dic_subt ={}#obter um dicionário que contém como chaves o valor de "1", "2", etc consoante o numero de relatorios que existem
				#e os seus valores correspondem ao subtítulo do respetivo relatorio
	for i in range(len(lista)):
		j = i+1
		j = str(j)
		relatorio = j
		dic_subt[relatorio] = (lista[i][0],lista[i][2])
	return render_template('relatorios.html', dic_subt = dic_subt)


#route chamada quando na pagina relatorios se carrega num determinado relatorio. A função relatorios recebe um id que corresponde
#ao numero do relatorio e renderiza um template com toda a informação do respetivo relatorio. Para tal necessita de verificar
#se o relatorio é do tipo 1 ou do tipo 2. O tipo 1 corresponde a um relatorio com questões, enquanto que o do tipo 2 corresponde a
#um relatorio com conteúdo, ou seja, parágrafos com texto em detrimento das questões.
@app.route('/relatorios/relatorio/<id_>')
def relatorios(id_):
	res = requests.get('http://localhost:5000/api/relatorios')
	lista = json.loads(res.content)
	string = id_.replace("<","")
	string1 = string.replace(">","")
	num = int(string1)-1
	relatorio = lista[num]
	if relatorio[0] == 1:
		return render_template("tipo1.html", tit = relatorio[1], subt = relatorio[2], iimage = relatorio[3], authors = relatorio[4],Masters = relatorio[5], Introduction = relatorio[6],
			questions = relatorio[8], references = relatorio[11], link = relatorio[12])


	else:
		return render_template("tipo2.html",tit = relatorio[1], subt = relatorio[2], iimage = relatorio[3], authors = relatorio[4],Masters = relatorio[5], content = relatorio[7],
			image = relatorio[9],Conclusion = relatorio[10], references = relatorio[11], link = relatorio[12])



#route chamada quando se carrega em Adicionar Relatorios na pagina index que irá renderizar o template "escolha_tipo.html",
#que mostra duas caixas consoante o tipo de relatorio que quer adicionar (tipo 1 ou tipo 2) 
@app.route('/add')
def escolher_tipo():
	return render_template("escolha_tipo.html",title = "Escolha o tipo de relatorio que pretende submeter:")

#route chamada quando se carrega no tipo 1 da pagina anterior
@app.route('/relatorio_adiciona1')
def relatorio_adiciona1():
	return render_template("adiciona_tipo1.html",title = "Preencha os espaços em branco para submeter o seu relatório do tipo 1:")

#route chamada quando se carrega no tipo 2 da pagina anterior
@app.route('/relatorio_adiciona2')
def relatorio_adiciona2():
	return render_template("adiciona_tipo2.html",title = "Preencha os espaços em branco para submeter o seu relatório do tipo 2:")


#route chamada quando se efetua o submit com todas as informações de um relatório que se quer adicionar do tipo 1
@app.route('/relatorio/novo1', methods=['POST'])
def relatorio_novo1():
	s = shelve.open("relatorios.db")
	ps = list(s.keys())
	maior = 0
	if len(ps) !=0:
		for relatorio in ps:
			numero = relatorio[-1]
			if int(numero) > maior:
				maior = int(numero)#buscar o maior número do relatório que se encontra na "base de dados"
	else:
		pass
	maior1 = maior +1#o novo relatorio será o numero a seguir do numero calculado anteriormente
	contador = str(maior1)
	title = request.form.get('title')
	subtitle = request.form.get('subtitle')
	iimage = request.form.get('iimage')

	name = request.form.get('name')
	number = request.form.get('number')
	email = request.form.get('email')
	telephone = request.form.get('telephone')


	#se o utilizador submeteu vários nomes de autores ocorre este processamento
	if "&" in name:

		lista_name = name.split("&")

		lista_number = number.split("&")

		lista_email = email.split("&")

		lista_telephone = telephone.split("&")

		if len(lista_name) != len(lista_number) or len(lista_name) != len(lista_email) or len(lista_name)!=len(lista_telephone):
			string = " Coloque o mesmo número de argumentos nos nomes dos autores, seus números, emails e telefone!"
			s.close()
			return render_template("erros.html", string = string)
		authors = []
		for i in range(len(lista_name)):
			author = []
			author.append(lista_name[i])
			author.append(lista_number[i])
			author.append(lista_email[i])
			author.append(lista_telephone[i])
			authors.append(author)#lista que contém sublistas, em que cada uma tem a informação de um autor
	
	#caso tenha apenas submetido um autor
	else:
		authors = []
		author=[]
		author.append(name)
		author.append(number)
		author.append(email)
		author.append(telephone)
		authors.append(author)#lista que contém a informação de um único autor


	masters = request.form.get('masters')
	introduction = request.form.get('introduction')

	enunciated = request.form.get('enunciated')
	answer = request.form.get('answer')
	resolution = request.form.get('resolution')

	#se o utilizador submeteu várias questões ocorre este processamento
	if "&" in enunciated:

		lista_enunciated = enunciated.split("&")
		
		lista_answer = answer.split("&")

		lista_resolution = resolution.split("&")
		if len(lista_enunciated) != len(lista_answer) or len(lista_enunciated) != len(lista_resolution):
			string = " Coloque o mesmo número de argumentos nos enunciados, suas respostas e resoluções!"
			s.close()
			return render_template("erros.html", string = string)

		questions = []#lista que contém sublistas, em que cada uma contém informação de cada questão(enunciado, resposta e resolução)
		for i in range(len(lista_enunciated)):
			question = []
			question.append(lista_enunciated[i])
			question.append(lista_answer[i])
			question.append(lista_resolution[i])
			questions.append(question)
	
	#caso tenha apenas submetido uma questão
	else:
		questions = []
		question = []
		question.append(enunciated)
		question.append(answer)
		question.append(resolution)
		questions.append(question)#lista que contém apenas uma sublista com as informações da única questão



	reference = request.form.get('references')

	#se o utilizador submeteu várias referências ocorre este processamento
	if "&" in reference:
		lista_reference = reference.split("&")
		references = []
		for i in range(len(lista_reference)):
			references.append(lista_reference[i])#lista que contém as várias referências

	else:
		references = [reference]#lista que contém a única referência submetida




	link = request.form.get('link')



	description = request.form.get('description')

	#se o utilizador submeteu várias descrições ocorre este processamento
	if "&" in description:
		lista_description = description.split("&")
		descriptions = []
		for i in range(len(lista_description)):
			descriptions.append(lista_description[i])#lista que contém as várias descrições

	else:
		descriptions = [description]#lista que contém a única descrição submetida

	dic_relatorio = {}


	dic_relatorio["tipo"] = 1
	dic_relatorio["title"]=title
	dic_relatorio["subtitle"] = subtitle
	dic_relatorio["iimage"] = iimage
	dic_relatorio["authors"] = authors
	dic_relatorio["masters"] = masters
	dic_relatorio["introduction"] = introduction
	dic_relatorio["questions"] = questions
	dic_relatorio["references"] = references
	dic_relatorio["link"] = link
	dic_relatorio["description"] = descriptions

	s["relatorio"+contador] = dic_relatorio#adicionar uma nova chave e um novo dicionário como valor que contém toda a informação do relatorio adicionado

	string = "Relatório adicionado!"
	
	s.close()
	return render_template("updatecomsucesso.html", string = string)


#route chamada quando se efetua o submit com todas as informações de um relatório que se quer adicionar do tipo 2
@app.route('/relatorio/novo2', methods=['POST'])
def relatorio_novo2():
	s = shelve.open("relatorios.db")
	ps = list(s.keys())
	maior = 0
	for relatorio in ps:
		numero = relatorio[-1]
		if int(numero) > maior:
			maior = int(numero)#buscar o maior número do relatório que se encontra na "base de dados"
	maior1=maior +1#o novo relatorio será o numero a seguir do numero calculado anteriormente
	contador = str(maior1)
	title = request.form.get('title')
	subtitle = request.form.get('subtitle')
	iimage = request.form.get('iimage')

	name = request.form.get('name')
	number = request.form.get('number')
	email = request.form.get('email')
	telephone = request.form.get('telephone')


	#se o utilizador submeteu vários nomes de autores ocorre este processamento
	if "&" in name:
		lista_name = name.split("&")

		lista_number = number.split("&")

		lista_email = email.split("&")

		lista_telephone = telephone.split("&")

		if len(lista_name) != len(lista_number) or len(lista_name) != len(lista_email) or len(lista_name)!=len(lista_telephone):
			string = " Coloque o mesmo número de argumentos nos nomes dos autores, seus números, emails e telefone!"
			s.close()
			return render_template("erros.html", string = string)
		authors = []
		for i in range(len(lista_name)):
			author = []
			author.append(lista_name[i])
			author.append(lista_number[i])
			author.append(lista_email[i])
			author.append(lista_telephone[i])
			authors.append(author)#lista que contém sublistas, em que cada uma tem a informação de um autor
	
	#caso tenha apenas submetido um autor
	else:
		authors = []
		author=[]
		author.append(name)
		author.append(number)
		author.append(email)
		author.append(telephone)
		authors.append(author)#lista que contém a informação de um único autor


	masters = request.form.get('masters')
	

	content = request.form.get('content')
	
	#se o utilizador submeteu vários parágrafos ocorre este processamento
	if "&" in content:
		lista_content = content.split("&")
		contents = []
		for i in range(len(lista_content)):
			contents.append(lista_content[i])#lista cujos elementos são todos os parágrafos

	else:
		contents = [content]#lista que contám apenas o um parágrafo submetido




	image = request.form.get('image')

	conclusion = request.form.get('conclusion')



	reference = request.form.get('references')

	#se o utilizador submeteu várias referências ocorre este processamento
	if "&" in reference:
		lista_reference = reference.split("&")
		references = []
		for i in range(len(lista_reference)):
			references.append(lista_reference[i])#lista que contém as várias referências

	else:
		references = [reference]#lista que contém a única referência submetida




	link = request.form.get('link')



	description = request.form.get('description')

	#se o utilizador submeteu várias descrições ocorre este processamento
	if "&" in description:
		lista_description = description.split("&")
		descriptions = []
		for i in range(len(lista_description)):
			descriptions.append(lista_description[i])#lista que contém as várias descrições

	else:
		descriptions = [description]#lista que contém a única descrição submetida

	dic_relatorio = {}


	dic_relatorio["tipo"] = 2
	dic_relatorio["title"]=title
	dic_relatorio["subtitle"] = subtitle
	dic_relatorio["iimage"] = iimage
	dic_relatorio["authors"] = authors
	dic_relatorio["masters"] = masters
	dic_relatorio["content"] = content
	dic_relatorio["image"] = image
	dic_relatorio["conclusion"] = conclusion
	dic_relatorio["references"] = references
	dic_relatorio["link"] = link
	dic_relatorio["description"] = descriptions

	s["relatorio"+contador] = dic_relatorio#adicionar uma nova chave e um novo dicionário como valor que contém toda a informação do relatorio adicionado

	
	string = "Relatório adicionado!"
	
	s.close()
	return render_template("updatecomsucesso.html", string = string)


#route chamada quando se carrega no Remover Relatorios na página index, a qual vai renderizar o template "remover.html", onde vai aparecer
#uma caixa de texto para inserir qual ou quais os relatórios que se pretende eliminar
@app.route('/delete')
def delete():
	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função da route "api/relatorios"
	lista = json.loads(res.content)#passar o objeto para lista
	if len(lista) == 0:
		string = "Não existem relatórios para eliminar!"
		return render_template("erros.html", string = string)

	return render_template("remover.html",title = "Qual o número do relatório a eliminar?")


#route chamada quando se carrega no submit que se encontra na página obtida a partir da route anterior
@app.route('/relatorio/delete',methods=['POST'])
def relatorio_delete():
	
	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função da route "api/relatorios"
	lista = json.loads(res.content)#passar o objeto para lista
	
	s = shelve.open("relatorios.db")
	response = request.form.get('response')
	
	#se o utilizador colocar mais que um relatorio a eliminar ocorre este processamento
	if "," in response:
		lista_response = response.split(",")
		resposta = ""
		for elemento in lista_response:
			for i in range(len(lista)):
				if elemento == str(i+1):#verificar se os relatorios que colocou se encontra na lista dos relatorios
					resposta += elemento
					for chave in s:
						if lista[i][2]==s[chave]["subtitle"]:
							del(s[chave])#eliminar a chave bem como o contéudo de todos os relatorios que o utilizador pediu para eliminar
		s.close()

		string = "Relatorio(s) " + " e ".join(resposta) + " eliminados!"
		return render_template("updatecomsucesso.html", string = string)

	#caso o utlizador apenas coloque um relatorio a eliminar	
	else:
		resposta = "relatorio "+response
		for i in range(len(lista)):
			if response == str(i+1):#verificar se o relatorio que colocou se encontra na lista dos relatorios
				for chave in s:
					if lista[i][2]==s[chave]["subtitle"]:
						del(s[chave])#eliminar a chave bem como o conteúdo do relatorio que o utilizador pretende eliminar

						string = resposta + " eliminado!"
						
						s.close()
						return render_template("updatecomsucesso.html", string = string)

	s.close()
	#caso o utilizador coloque um relatório que não se encontra na "base de dados"
	string = "O relatório que quer eliminar não existe!"
	return render_template("erros.html", string = string)



#route chamada quando se carrega em Update Relatorios na página index
@app.route('/update')
def update():
	res = requests.get('http://localhost:5000/api/relatorios')
	lista = json.loads(res.content)
	if len(lista) == 0:
		string = "Não existem relatórios para modificar!"
		return render_template("erros.html", string = string)
	else:
		dic_subt ={}#dicionário que contém como chave o numero de relatorio e como valores os subtítulos do respetivo relatório
		for i in range(len(lista)):
			j = i+1
			j = str(j)
			relatorio = j
			dic_subt[relatorio] = lista[i][2]

		#renderizar um template onde irá aparecer todos os relatórios que existem para o utilizador escolher qual o relatorio que pretende fazer alterações
		return render_template("update.html", dic_subt = dic_subt)



#route chamada quando se carrega num relatorio da página obtida a partir da route anterior
@app.route('/update/relatorio/<id_>')
def updates(id_):#função que recebe um id correspondente ao numero do relatorio que se carrega na página obtida a partir da route anterior
	res = requests.get('http://localhost:5000/api/relatorios')
	s = shelve.open("relatorios.db")
	lista_tuplos = list(s.items())

	lista = json.loads(res.content)
	string = id_.replace("<","")
	string1 = string.replace(">","")
	num0 = int(string1)
	num = num0-1
	relatorio = lista[num]
	autor = []
	numero = []
	emaile = []
	telefone = []

	enunciated = []
	answer = []
	resolution = []

	for elemento in lista_tuplos:
		if elemento[1]["subtitle"] == relatorio[2]:
			identificador = elemento[0]
	
	#se a lista de autores do relatório escolhido tiver apenas uma sublista, logo apenas contém informação de um único autor e ocorre este processamento
	if len(relatorio[4]) == 1:
		author = relatorio[4][0]["name"]
		number = relatorio[4][0]["number"]
		email = relatorio[4][0]["email"]
		telephone = relatorio[4][0]["telephone"]

	#caso contrário significa que contém mais do que um autor
	else:	
		for elemento in relatorio[4]:
			autor.append(elemento["name"])
			numero.append(str(elemento["number"]))
			emaile.append(elemento["email"])
			telefone.append(elemento["telephone"])

		author = "&".join(autor)
		number = "&".join(numero)
		email = "&".join(emaile)
		telephone = "&".join(telefone)
	

	#se a lista de questões do relatório escolhido tiver apenas uma sublista, logo apenas contém informação de uma única questão e ocorre este processamento
	if len(relatorio[8]) == 1:
		enunciated = relatorio[8][0]["enunciated"]
		answer = relatorio[4][0]["asnwer"]
		resolution = relatorio[4][0]["resolution"]
		
	#caso contrário significa que contém mais do que uma questão
	else:
		for elemento in relatorio[8]:
			enunciated.append(elemento["enunciated"])
			answer.append(str(elemento["answer"]))
			resolution.append(elemento["resolution"])

		enunciated = "&".join(enunciated)
		answer = "&".join(answer)
		resolution = "&".join(resolution)
		

	#se a lista de contéudo do relatório escolhido tiver apenas um elemento, logo apenas contém um único parágrafo e ocorre este processamento
	if len(relatorio[7]) == 1:
		content = "".join(relatorio[7])

	#caso contrário significa que contém mais do que um parágrafo
	else:
		content="&".join(relatorio[7])


	#se a lista de referências do relatório escolhido tiver apenas um elemento, logo apenas contém uma única referência e ocorre este processamento
	if len(relatorio[11]) == 1:
		references = "".join(relatorio[11])

	#caso contrário significa que contém mais do que uma referência
	else:
		references="&".join(relatorio[11])


	#se a lista de descrições do relatório escolhido tiver apenas um elemento, logo apenas contém uma única descrição e ocorre este processamento
	if len(relatorio[13]) == 1:
		description = "".join(relatorio[13])

	#caso contrário significa que contém mais do que uma descrição
	else:
		description ="&".join(relatorio[13])




	#ver qual é o tipo do relatorio escolhido e renderizar o template com as suas informações
	if relatorio[0] == 1:
		return render_template("update_tipo1.html", id = identificador,tit = relatorio[1], subt = relatorio[2], iimage = relatorio[3], authors = author, number = number, email = email, telephone = telephone, Masters = relatorio[5], Introduction = relatorio[6],
			enunciated = enunciated, answer = answer, resolution = resolution, references = references, link = relatorio[12], description= description, title = "Altere o pretendido neste relatório e submeta no final:")


	else:
		return render_template("update_tipo2.html",id = identificador,tit = relatorio[1], subt = relatorio[2], iimage = relatorio[3], authors = author, number = number, email = email, telephone = telephone, Masters = relatorio[5], content = content,
			image = relatorio[9], Conclusion = relatorio[10], references = references, link = relatorio[12], description= description, title = "Altere o pretendido neste relatório e submeta no final:")



#route chamada quando se efetua alterações de um relatorio do tipo 1 e se carrega no submit
@app.route('/update/relatorio/update/novo1/<id_>', methods=['POST'])
def update_novo1(id_):
	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função da route "api/relatorios"
	s = shelve.open("relatorios.db")
	string = id_.replace("<","")
	string1 = string.replace(">","")
	

	title = request.form.get('title')
	subtitle = request.form.get('subtitle')
	iimage = request.form.get('iimage')

	name = request.form.get('name')
	number = request.form.get('number')
	email = request.form.get('email')
	telephone = request.form.get('telephone')

	#se o utilizador submeteu vários nomes de autores ocorre este processamento
	if "&" in name:
		lista_name = name.split("&")

		lista_number = number.split("&")

		lista_email = email.split("&")

		lista_telephone = telephone.split("&")

		if len(lista_name) != len(lista_number) or len(lista_name) != len(lista_email) or len(lista_name)!=len(lista_telephone):
			string = " Coloque o mesmo número de argumentos nos nomes dos autores, seus números, emails e telefone!"
			s.close()
			return render_template("erros.html", string = string)

		authors = []
		for i in range(len(lista_name)):
			author = []
			author.append(lista_name[i])
			author.append(lista_number[i])
			author.append(lista_email[i])
			author.append(lista_telephone[i])
			authors.append(author)#lista que contém sublistas, em que cada uma tem a informação de um autor
	
	#caso tenha apenas submetido um autor
	else:
		authors = []
		author=[]
		author.append(name)
		author.append(number)
		author.append(email)
		author.append(telephone)
		authors.append(author)#lista que contém a informação de um único autor


	masters = request.form.get('masters')
	introduction = request.form.get('introduction')

	enunciated = request.form.get('enunciated')
	answer = request.form.get('answer')
	resolution = request.form.get('resolution')

	#se o utilizador submeteu várias questões ocorre este processamento
	if "&" in enunciated:

		lista_enunciated = enunciated.split("&")
		
		lista_answer = answer.split("&")

		lista_resolution = resolution.split("&")

		if len(lista_enunciated) != len(lista_answer) or len(lista_enunciated) != len(lista_resolution):
			string = " Coloque o mesmo número de argumentos nos enunciados, suas respostas e resoluções!"
			s.close()
			return render_template("erros.html", string = string)

		questions = []
		for i in range(len(lista_enunciated)):
			question = []
			question.append(lista_enunciated[i])
			question.append(lista_answer[i])
			question.append(lista_resolution[i])
			questions.append(question)#lista que contém sublistas, em que cada uma contém informação de cada questão(enunciado, resposta e resolução)
	
	#caso tenha apenas submetido uma questão
	else:
		questions = []
		question = []
		question.append(enunciated)
		question.append(answer)
		question.append(resolution)
		questions.append(question)#lista que contém apenas uma sublista com as informações da única questão



	reference = request.form.get('references')

	#se o utilizador submeteu várias referências ocorre este processamento
	if "&" in reference:
		lista_reference = reference.split("&")
		references = []
		for i in range(len(lista_reference)):
			references.append(lista_reference[i])#lista que contém as várias referências

	else:
		references = [reference]#lista que contém a única referência submetida




	link = request.form.get('link')



	description = request.form.get('description')

	#se o utilizador submeteu várias descrições ocorre este processamento
	if "&" in description:
		lista_description = description.split("&")
		descriptions = []
		for i in range(len(lista_description)):
			descriptions.append(lista_description[i])#lista que contém as várias descrições

	else:
		descriptions = [description]#lista que contém a única descrição submetida
	

	dic_relatorio = {}


	dic_relatorio["tipo"] = 1
	dic_relatorio["title"]=title
	dic_relatorio["subtitle"] = subtitle
	dic_relatorio["iimage"] = iimage
	dic_relatorio["authors"] = authors
	dic_relatorio["masters"] = masters
	dic_relatorio["introduction"] = introduction
	dic_relatorio["questions"] = questions
	dic_relatorio["references"] = references
	dic_relatorio["link"] = link
	dic_relatorio["description"] = descriptions

	

	for chave in s:
		if chave == string1:
			s[chave] = dic_relatorio#colocar como novo valor na chave do respetivo relatorio um novo dicionário que contém toda a informação do relatorio modificado

	string = "Feito update!"
	s.close()
	return render_template("updatecomsucesso.html", string = string)


#route chamada quando se efetua alterações de um relatorio do tipo 2 e se carrega no submit
@app.route('/update/relatorio/update/novo2/<id_>', methods=['POST'])
def update_novo2(id_):
	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função da route "api/relatorios"
	s = shelve.open("relatorios.db")
	string = id_.replace("<","")
	string1 = string.replace(">","")
	

	title = request.form.get('title')
	subtitle = request.form.get('subtitle')
	iimage = request.form.get('iimage')

	name = request.form.get('name')
	number = request.form.get('number')
	email = request.form.get('email')
	telephone = request.form.get('telephone')

	#se o utilizador submeteu vários nomes de autores ocorre este processamento
	if "&" in name:
		lista_name = name.split("&")

		lista_number = number.split("&")

		lista_email = email.split("&")

		lista_telephone = telephone.split("&")

		if len(lista_name) != len(lista_number) or len(lista_name) != len(lista_email) or len(lista_name)!=len(lista_telephone):
			string = " Coloque o mesmo número de argumentos nos nomes dos autores, seus números, emails e telefone!"
			s.close()
			return render_template("erros.html", string = string)

		authors = []
		for i in range(len(lista_name)):
			author = []
			author.append(lista_name[i])
			author.append(lista_number[i])
			author.append(lista_email[i])
			author.append(lista_telephone[i])
			authors.append(author)#lista que contém sublistas, em que cada uma tem a informação de um autor
	
	#caso tenha apenas submetido um autor
	else:
		authors = []
		author=[]
		author.append(name)
		author.append(number)
		author.append(email)
		author.append(telephone)
		authors.append(author)#lista que contém a informação de um único autor


	masters = request.form.get('masters')
	

	content = request.form.get('content')
	
	#se o utilizador submeteu vários parágrafos ocorre este processamento
	if "&" in content:
		lista_content = content.split("&")
		contents = []
		for i in range(len(lista_content)):
			contents.append(lista_content[i])#lista cujos elementos são todos os parágrafos

	else:
		contents = [content]#lista que contém apenas o parágrafo submetido




	image = request.form.get('image')

	conclusion = request.form.get('conclusion')



	reference = request.form.get('references')

	#se o utilizador submeteu várias referências ocorre este processamento
	if "&" in reference:
		lista_reference = reference.split("&")
		references = []
		for i in range(len(lista_reference)):
			references.append(lista_reference[i])#lista que contém as várias referências

	else:
		references = [reference]#lista que contém a única referência submetida




	link = request.form.get('link')



	description = request.form.get('description')

	#se o utilizador submeteu várias descrições ocorre este processamento
	if "&" in description:
		lista_description = description.split("&")
		descriptions = []
		for i in range(len(lista_description)):
			descriptions.append(lista_description[i])#lista que contém as várias descrições

	else:
		descriptions = [description]#lista que contém a única descrição submetida
	

	dic_relatorio = {}


	dic_relatorio["tipo"] = 2
	dic_relatorio["title"]=title
	dic_relatorio["subtitle"] = subtitle
	dic_relatorio["iimage"] = iimage
	dic_relatorio["authors"] = authors
	dic_relatorio["masters"] = masters
	dic_relatorio["content"] = contents
	dic_relatorio["image"] = image
	dic_relatorio["conclusion"] = conclusion
	dic_relatorio["references"] = references
	dic_relatorio["link"] = link
	dic_relatorio["description"] = descriptions

	
	

	for chave in s:
		if chave == string1:
			s[chave] = dic_relatorio#colocar como novo valor na chave do respetivo relatorio um novo dicionário que contém toda a informação do relatorio modificado

	
	string = "Feito update!"
	s.close()
	return render_template("updatecomsucesso.html", string = string)


#route chamada quando se carrega em Autores Relatorios na pagina index
@app.route('/autores_relatorios')
def autores_relatorios():
	res = requests.get('http://localhost:5000/api/relatorios')
	lista = json.loads(res.content)
	if len(lista) == 0:
		string = "Não existem relatórios! É necessário adicionar relatórios!"
		return render_template("erros.html", string = string)
	dic_autores = {}#dicionario que contém como chave o número do relatório e como valor uma lista com sublistas, em que cada uma da sublistas contém informação de um autor do respetivo relatório

	for i in range(len(lista)):
		
		lista_autores = lista[i][4]
		for k in lista_autores:
			if str(k["number"]) not in dic_autores:
				dic = {}
				dic["name"] = k["name"]
				dic["number"] = k["number"]
				dic["email"] = k["email"]
				dic["telephone"] = k["telephone"]
				dic_autores[str(k["number"])]= dic

	
		

	#renderizar um template de uma página onde aparecem os vários autores e ao carregar no nome de cada um irá ocorrer uma hiperligação para o relatorio desse mesmo autor
	return render_template('autores_relatorios.html', dic_autores = dic_autores)

@app.route('/relatorios/relatorio/autor/<el>')
def relatorios_autor(el):
	res = requests.get('http://localhost:5000/api/relatorios')#buscar o objeto retornado da função anterior
	lista = json.loads(res.content)#passar o objeto para lista
	string = el.replace("<","")
	string1 = string.replace(">","")
	

	
	dic_subt ={}#dicionário que contém como chave o numero de relatorio e como valores os subtítulos do respetivo relatório
	for i in range(len(lista)):
		for autor in lista[i][4]:
			
			if str(autor["number"]) == string1:
				j = i+1
				j = str(j)
				relatorio = j
				dic_subt[relatorio] = lista[i][2]
	

	#renderizar um template onde irá aparecer todos os relatórios do autor dado 
	return render_template("relatorios_autor.html", dic_subt = dic_subt)


#route chamada quando se carrega na Description na página index
@app.route('/description')
def description():
	res = requests.get('http://localhost:5000/api/relatorios')
	lista = json.loads(res.content)
	if len(lista) == 0:
		string = "Não existem relatórios! É necessário adicionar relatórios!"
		return render_template("erros.html", string = string)
	dic_descript={}#dicionário que contém como chaves as descrições com o valor corrrespondente a um tuplo que contém no primeiro elemento o número do relatório que contém essa descrição e o segundo elemento é o seu subtítulo
	for i in range(len(lista)):
		j = i+1
		j = str(j)
		relatorio = j
		description = lista[i][13]
		subtitle = lista[i][2]
		for element in description:
			if element not in dic_descript:
				dic_descript[element] = [(relatorio,subtitle)]

			else:
				dic_descript[element].append((relatorio,subtitle))

	#renderizar um template de uma página onde aparecem as descrições e por baixo os relatórios que apresentam essa descrição e ao
	#carregar num deles ocorre uma hiperligação para o respetivo conteúdo do relatório
	return render_template('description.html', dic_descript = dic_descript)


#route chamada quando se submete uma palavra ou conjunto de palavras na caixa que aparece na página onde se encontram os relatórios e seus subtítulos
@app.route('/pesquisa',methods=['POST'])
def pesquisa():
	pesquisa = request.form.get('search')
	res = requests.get('http://localhost:5000/api/relatorios')
	lista = json.loads(res.content)
	lista_rel = []

	
	dic_rel={}
	
	#ciclo que pretende verificar se a palavra ou palavras submetidas se encontram em algum relatório e se sim então construir um dicionário onde a chave é o número do relatório jutamente com o subtitulo e o valor é uma lista com o contéudo onde a ou as palavras se encontram
	#Os elementos da lista obtida a partir da route "api/relatórios" são sublistas correspondentes a cada relatório e dentro de cada
	#sublista poderemos ter dados do tipo inteiros ou do tipo string ou do tipo lista que por sua vez pode conter elementos que poderão
	#ser dicionários ou strings. E dentro desses dicionários podemos inteiros ou strings como chaves. Daí ser este o processamento que ocorre neste ciclo
	for i in range(len(lista)):
		j = i+1
		j = str(j)
		relatorio = j+lista[i][2]
		
		for k in lista[i]:
			
			if type(k) is int:
				k = str(k)
				
				if pesquisa in k or pesquisa in k.lower():

					if str(relatorio) not in dic_rel.keys():
						x = k.split(" ")
						d = []
						for palavra in x:
							if pesquisa in palavra.lower() or pesquisa in palavra.upper():
								palavra1 = "\u0332".join(palavra)
								d.append(palavra1)
							else:
								d.append(palavra)
						d1 = " ".join(d)
						dic_rel[relatorio] = [d1]
					else:
						x = lista[i][k].split(" ")
						d = []
						for palavra in x:
							if pesquisa in palavra.lower() or pesquisa in palavra.upper():
								palavra1 = "\u0332".join(palavra)
								d.append(palavra1)
							else:
								d.append(palavra)
						d1 = " ".join(d)
						dic_rel[relatorio].append(d1)
						

			elif type(k) is str:
				print(k.lower())
				if pesquisa in k or pesquisa in k.lower():
			
					if str(relatorio) not in dic_rel.keys():
						x = k.split(" ")
						d = []
						for palavra in x:
							if pesquisa in palavra.lower() or pesquisa in palavra.upper():
								palavra1 ="\u0332".join(palavra)
								d.append(palavra1)
							else:
								d.append(palavra)
						d1 = " ".join(d)
						dic_rel[relatorio] = [d1]
					else:
						x = k.split(" ")
						d = []
						for palavra in x:
							if pesquisa in palavra.lower() or pesquisa in palavra.upper():
								palavra1 = "\u0332".join(palavra)
								d.append(palavra1)
							else:
								d.append(palavra)
						d1 = " ".join(d)
						dic_rel[relatorio].append(d1)

			elif type(k) is list:
				for l in k:
					if type (l) is dict:
						for chave in l:
							if type(l[chave]) is int:
								l[chave] = str(l[chave])
								if pesquisa in l[chave] or pesquisa in l[chave].lower():
									
									if str(relatorio) not in dic_rel.keys():
										x = l[chave].split(" ")
										
										d = []
										for palavra in x:
											if pesquisa in palavra.lower() or pesquisa in palavra.upper():
												palavra1 = "\u0332".join(palavra)
												d.append(palavra1)
											else:
												d.append(palavra)
										d1 = " ".join(d)
										dic_rel[relatorio] = [d1]
									else:
										x = l[chave].split(" ")
										
										d = []
										for palavra in x:
											if pesquisa in palavra.lower() or pesquisa in palavra.upper():
												palavra1 = "\u0332".join(palavra)
												d.append(palavra1)
											else:
												d.append(palavra)
										d1 = " ".join(d)
										dic_rel[relatorio].append(d1)
						
							else:
								if pesquisa in l[chave] or pesquisa in l[chave].lower():
									
									if str(relatorio) not in dic_rel.keys():
										x = l[chave].split(" ")
										
										d = []
										for palavra in x:
											if pesquisa in palavra.lower() or pesquisa in palavra.upper():
												palavra1 = "\u0332".join(palavra)
												d.append(palavra1)
											else:
												d.append(palavra)
										d1 = " ".join(d)
										dic_rel[relatorio] = [d1]
									else:
										x = l[chave].split(" ")
										print(x)
										d = []
										for palavra in x:
											if pesquisa in palavra.lower() or pesquisa in palavra.upper():
												palavra1 ="\u0332".join(palavra)
												d.append(palavra1)
											else:
												d.append(palavra)
										d1 = " ".join(d)
										dic_rel[relatorio].append(d1)

					else:
						if pesquisa in l or pesquisa in l.lower():
						
							if str(relatorio) not in dic_rel.keys():
								
								x = l.split(" ")
								
								d = []
								for palavra in x:
									if pesquisa in palavra.lower() or pesquisa in palavra.upper():
										palavra1 ="\u0332".join(palavra)
										d.append(palavra1)
									else:
										d.append(palavra)
								d1 = " ".join(d)
								dic_rel[relatorio] = [d1]
							else:
								x = l.split(" ")
								d = []
								for palavra in x:
									if pesquisa in palavra.lower() or pesquisa in palavra.upper():
										palavra1 ="\u0332".join(palavra)
										d.append(palavra1)
									else:
										d.append(palavra)
								d1 = " ".join(d)
								dic_rel[relatorio].append(d1)

	
	#se houver relatórios que contêm essas palavras ou palavra então aparece uma página com esses relatórios e ao carregar em cada
	#um deles irá ocorrer uma hiperligação para o contéudo do respetivo relatório
	if len(dic_rel) != 0:
		return render_template("pesquisa.html", pesquisa = pesquisa, dic_rel = dic_rel)
	
	#caso não houver relatórios com a palavra ou palavras submetidas então aparece uma página a dizer que não existem relatórios com essa(s) palavra(s)
	else:
		string = "Não existem relatórios associados a esta pesquisa!"
		return render_template("erros.html", string = string)


#route chamada quando se carrega em Autores do Projeto na página index que irá renderizar um template de uma página onde aparece
# a informação dos autores deste projeto
@app.route('/autores_portfolio')
def autores_portfolio():
	return render_template("dadospessoais.html")