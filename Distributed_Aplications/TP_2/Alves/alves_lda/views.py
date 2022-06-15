from django.shortcuts import render

# Create your views here.

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.regex_helper import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import *
from datetime import *
import datetime
from .models import *

# pagina inicial
from django.urls import reverse

# from clinica.forms import SignUpForm
from .models import *

def homepage_view(request):
    return render(request, "inicial.html")

#--------------------------------------------------------------------------------UTENTE------------------------------------------------------------#

def login_utente(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username} ")
                return redirect('/alves_lda/utente/'+username)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'utente/login_utente.html', {'form': form})


def registar_utente(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        username = request.POST['username']
        x = username.replace("U", "")
        if "U" in username and Utente.objects.filter(numutente=x).exists():
            if form.is_valid():
                user = form.save()
                messages.success(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/alves_lda/")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = NewUserForm()
    return render(request, "utente/registar_utente.html", context={"form": form})

@login_required
def utente(request, username):
    return render(request, 'utente/utente.html', {'username':username})

@login_required
def marcar_consulta(request, username):
    form = MarcarConsultaForm()

    return render(request, 'utente/marcar_consulta.html', context={'form': form,'username':username })

@login_required
def marcar(request, username):

    x=username.replace("U","")

    utente = Utente.objects.get(numutente=x)
    especialidade = request.POST['especialidade']

    data = request.POST['data']
    hora = request.POST['hora']
    data1 = data.split("-")
    hora1 = hora.split(":")

    dt1 = date(int(data1[0]), int(data1[1]), int(data1[2]))
    tm1 = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))

    if dt1 >= datetime.now().date():
        if tm1.minute != 0 and tm1.minute != 30:
            string = "Introduza uma hora válida! A Hora deverá ter o formato ##:00:00H ou ##:30:00H, sendo ## a hora pretendida."
            return render(request, "utente/erros2.html", {'string': string})
        else:
            if (tm1.hour < 13 or tm1.hour >= 14) and (tm1.hour >= 9 and tm1.hour < 18 ) and (dt1.weekday() != 6):

                data1 = data.split("-")
                hora1 = hora.split(":")
                dt = datetime(int(data1[0]), int(data1[1]), int(data1[2]))
                tm = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))
                combined = dt.combine(dt, tm)
                if Entrada_Agenda.objects.filter(utente = utente, data_hora = combined).exists():
                    string = "Já possui uma consulta marcada nessa data."
                    return render(request, "utente/erros2.html", {'string': string})
                medicos = Medico.objects.filter(especialidade=especialidade)
                for medico in medicos:
                    agenda = Entrada_Agenda.objects.filter(medico=medico)
                    if agenda == None:
                        data1 = data.split("-")
                        hora1 = hora.split(":")
                        dt = datetime(int(data1[0]), int(data1[1]), int(data1[2]))
                        tm = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))
                        combined = dt.combine(dt, tm)
                        entradaagenda = Entrada_Agenda.objects.create(data_hora=combined,
                                                                      estado="Marcado", utente=utente,
                                                                      medico=medico)
                        entradaagenda.save()
                        string = "Consulta Marcada com: " + medico.nome
                        return render(request, "utente/erro.html", context={'string': string, 'username':username})
                    else:
                        contador = 0
                        contador1 = 0
                        for eag in agenda:
                            contador1+=1
                            if eag.data_hora.date() == dt1:
                                if eag.data_hora.time() == tm1:
                                    break
                                else:
                                    contador+=1
                            else:
                                contador+=1

                        if contador == contador1:
                            data1 = data.split("-")
                            hora1 = hora.split(":")
                            dt = datetime(int(data1[0]), int(data1[1]), int(data1[2]))
                            tm = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))
                            combined = dt.combine(dt, tm)
                            entradaagenda = Entrada_Agenda.objects.create(data_hora=combined,
                                                                          estado="Marcado", utente=utente,
                                                                          medico=medico)
                            entradaagenda.save()
                            string = "Consulta Marcada com: " + medico.nome
                            return render(request, "utente/erro.html", context={'string': string, 'username':username})
            else:
                string = "Não é possível marcar consulta neste horário! Verifique o horário de atendimento e remarque..."
                return render(request, "utente/erros2.html", {'string': string})
        string = "Não é possível marcar consulta! Remarque..."
        return render(request, "utente/erros2.html", {'string': string})
    else:
        string = "Não é possível marcar uma consulta no passado! Remarque..."
        return render(request, "utente/erros2.html", {'string': string})

@login_required
def horario(request, username):
    return render(request, 'utente/horario.html', {'username':username})

@login_required
def especialidades(request, username):
    lista=[]
    medicos = Medico.objects.all()
    for medico in medicos:
        a=medico.especialidade
        if a not in lista:
            lista.append(a)
    return render(request, 'utente/especialidades.html', {'lista':lista,'username':username})


@login_required
def veragenda(request, username):
    x = username.replace("U", "")
    utente = Utente.objects.get(numutente=x)

    if Entrada_Agenda.objects.filter(utente=utente).exists():
        entradas_agenda = Entrada_Agenda.objects.filter(utente=utente)

        return render(request, 'utente/ver_agenda.html', context={'consultas': entradas_agenda, 'username':username})
    else:
        string = "Não tem consultas marcadas!"
        return render(request, "medico/erros2.html", {'string': string})


@login_required
def historico_consultas(request, username):
    x = username.replace("U", "")

    utente = Utente.objects.get(numutente=x)

    fichamedica = Ficha_medica.objects.get(utente = utente)

    if Consulta.objects.filter(fichamedica = fichamedica).exists():
        consultas = Consulta.objects.filter(fichamedica = fichamedica)

        return render(request, "utente/ver_hist_consultas.html", {'consultas':consultas, 'username':username})
    else:
        string = "Utente introduzido não tem consultas realizadas!"
        return render(request, "gestor/erros2.html", {'string': string})


@login_required
def historico_exames(request, username):
    x = username.replace("U", "")

    lista_exames =[]

    utente = Utente.objects.get(numutente=x)

    fichamedica = Ficha_medica.objects.get(utente = utente)

    if Consulta.objects.filter(fichamedica=fichamedica).exists():
        consultas = Consulta.objects.filter(fichamedica = fichamedica)

        for consulta in consultas:
            exames = Exame.objects.filter(consulta = consulta)
            if exames:
                lista_exames.append(exames)

        if len(lista_exames)==0:
            string = "Utente introduzido não tem exames!"
            return render(request, "gestor/erros2.html", {'string': string})
        else:
            return render(request, "utente/ver_hist_exames.html", context={'exames':lista_exames, 'username':username})
    else:
        string = "Utente introduzido não tem consultas realizadas!"
        return render(request, "gestor/erros2.html", {'string': string})


@login_required
def cancelar_consulta(request, username):

    form = MarcarConsultaForm()
    return render(request, 'utente/cancelar_consulta.html', context={'form': form, 'username':username})

@login_required
def cancelar(request, username):
    x = username.replace("U", "")

    utente = Utente.objects.get(numutente=x)

    especialidade = request.POST['especialidade']

    data = request.POST['data']
    hora = request.POST['hora']

    Entradas_Agenda = Entrada_Agenda.objects.all()

    data1 = data.split("-")
    hora1 = hora.split(":")

    dt = date(int(data1[0]), int(data1[1]), int(data1[2]))
    tm = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))

    for eag in Entradas_Agenda:
        if utente == eag.utente and dt == eag.data_hora.date() and tm == eag.data_hora.time() and especialidade == eag.medico.especialidade:
            eag.delete()
            string = "Consulta cancelada com sucesso!"
            return render(request, "utente/erro.html", context={'string' : string, 'username':username})

    string = "Nao marcou essa consulta para a poder cancelar..."
    return render(request, "utente/erro.html", context={'string' : string, 'username':username})


def sair(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("/alves_lda")

#---------------------------------------------------------------------MÉDICO---------------------------------------------------------#

def login_medico(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username} ")
                return redirect('/alves_lda/medico/'+username)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'medico/login_medico.html', {'form': form})


def registar_medico(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        username = request.POST['username']
        x = username.replace("M", "")
        if "M" in username and Medico.objects.filter(cedula=x).exists():
            if form.is_valid():
                user = form.save()
                messages.success(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/alves_lda/")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = NewUserForm()
    return render(request, "medico/registar_medico.html", context={"form": form})

@login_required
def medico(request, username):
    return render(request, 'medico/medico.html', {"username":username})


@login_required
def historico_consultas_medico(request, username):
    x=username.replace("M","")

    medico = Medico.objects.get(cedula=x)

    if Consulta.objects.filter(medico=medico).exists():
        consultas = Consulta.objects.filter(medico=medico)
        listas_utente_consulta=[]
        for consulta in consultas:
            lista_utente_consulta = []
            fichamedica = consulta.fichamedica
            utente = fichamedica.utente
            lista_utente_consulta.append(utente)
            lista_utente_consulta.append(consulta)
            listas_utente_consulta.append(lista_utente_consulta)
        return render(request, 'medico/ver_historico_consultas.html', context={'consultas':listas_utente_consulta, "username":username})
    else:
        string = "Não existem consultas associadas ao médico pretendido!"
        return render(request, "medico/erros2.html", {'string': string})


@login_required
def realizar_consulta(request, username):
    form = RealizarConsultaForm()
    return render(request, 'medico/realizar_consulta.html', context={'form': form, "username":username})

@login_required
def realizar_consulta_adicionar(request, username):
    x = username.replace("M", "")
    if str(x) == request.POST['cedula']:

        utente = Utente.objects.get(numutente=request.POST['numutente'])

        data = request.POST['data']
        hora = request.POST['hora']

        cedula = request.POST['cedula']

        entradas_agenda = Entrada_Agenda.objects.all()

        data1 = data.split("-")
        hora1 = hora.split(":")

        dt = date(int(data1[0]), int(data1[1]), int(data1[2]))
        tm = time(int(hora1[0]), int(hora1[1]), int(hora1[2]))

        for eag in entradas_agenda:
            if utente == eag.utente and dt == eag.data_hora.date() and tm == eag.data_hora.time() and cedula == eag.medico.cedula:
                fichamedica = Ficha_medica.objects.get(utente=utente)
                medico = eag.medico
                consulta = Consulta.objects.create(data= dt, medico = medico, fichamedica = fichamedica)
                consulta.save()
                id = consulta.id_consulta
                eag.delete()
                idu=utente.numutente
                return render(request,'medico/consulta.html', context={'id':id, "username":username, 'idu':idu})

        string= "Não é possivel realizar esta consulta... Retifique!"
        return render(request, "medico/erro.html", context={'string':string, "username":username})
    else:
        string = "O número introduzido não é o seu... Retifique!"
        return render(request, "medico/erros2.html", {'string': string})


@login_required
def entrada_agenda_medico(request,username):
    form = AgendaMedicoForm()
    return render(request, 'medico/ent_agenda.html', context={'form': form, 'username':username})

@login_required
def ver_entrada_agenda_medico(request,username):
    listac=[]
    x = username.replace("M", "")
    data=request.GET['data']

    medico = Medico.objects.get(cedula=x)

    if Entrada_Agenda.objects.filter(medico=medico).exists():
        entradas_agenda = Entrada_Agenda.objects.filter(medico=medico)
        for eag in entradas_agenda:
            if str(eag.data_hora.date()) == data:
                listac.append(eag)
        if len(listac)>0:
            return render(request, 'medico/ver_ent_agenda.html', context={'consultas': listac, 'username':username})
        else:
            string = "Não tem consultas marcadas para essa data!"
            return render(request, "medico/erros2.html", {'string': string})

    else:
        string = "Médico inserido não tem consultas marcadas!"
        return render(request, "medico/erros2.html", {'string': string})


@login_required
def marcar_exame(request, username,id, idu):
    form = MarcarExameForm()
    id = id
    return render(request, 'medico/marcar_exame.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def submeter_exame(request, username, id, idu):
    tipo = request.POST['tipo']
    local = request.POST['local']

    data_hora = request.POST['data_hora']

    duracao = request.POST['duracao']

    preco = request.POST['preco']

    estado = request.POST['estado']

    observacoes = request.POST['observacoes']

    if estado == "on":
        estado = True
    else:
        estado = False

    consulta = Consulta.objects.get(id_consulta= id)

    exame = Exame.objects.create(tipo = tipo, local = local, data_hora = data_hora, duracao = duracao, preco = preco, estado = estado, observacoes = observacoes, consulta = consulta)
    exame.save()
    string = "Exame criado!"
    return render(request,"medico/erros2.html",{'string':string})

@login_required
def adicionar_medicoes(request, username,id, idu):
    form = MedicoesForm()
    return render(request, 'medico/medicoes.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def submeter_medicoes(request, username,id, idu):

    numutente = idu
    data = request.POST["data"]
    peso = request.POST["peso"]
    glicemia = request.POST["glicemia"]
    altura = request.POST["altura"]
    tensaoarterial = request.POST["tensaoarterial"]
    colesterol = request.POST["colesterol"]
    trigliceridios = request.POST["trigliceridios"]
    saturacao = request.POST["saturacao"]
    inr = request.POST["inr"]


    utente = Utente.objects.get(numutente = numutente)

    fichamedica= Ficha_medica.objects.get(utente = utente)

    medicao = Medicao.objects.create(data = data, peso = peso, glicemia= glicemia, altura = altura, tensaoarterial = tensaoarterial,
                             colesterol = colesterol, trigliceridios= trigliceridios, saturacao = saturacao, inr = inr)
    medicao.save()

    fichamedica.medicoes.add(medicao)


    string="Medição adicionada!"
    return render(request,"medico/erros2.html",{'string':string})


@login_required
def infomedicamento(request, username, id, idu):
    form = MedicamentoNomeForm()
    return render(request, 'medico/medicamento_submeter.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def verinfomedicamento(request, username, id, idu):
    nome = request.GET["nome"]

    if Medicamento.objects.filter(nome=nome).exists():

        medicamento = Medicamento.objects.filter(nome=nome)
        return render(request, 'medico/lista_medicamento.html', context={'medicamento': medicamento, 'id':id, "username":username, 'idu':idu})
    else:
        string = "Medicamento introduzido não existe! Adicione de novo..."
        return render(request, "medico/erros2.html", {'string': string})

@login_required
def adicionar_prescricoes(request, username,id, idu):

    form = PrescricoesForm()
    return render(request, 'medico/adicionar_prescricoes.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def submeter_prescricoes(request, username,id, idu):

    data = request.POST["data"]
    medicamento = request.POST["medicamento"]
    dosagem = request.POST["dosagem"]
    toma = request.POST["toma"]

    if "," in medicamento:
        consulta = Consulta.objects.get(id_consulta=id)
        prescricao = Prescricao.objects.create(data=data, toma=toma)
        prescricao.consulta = consulta
        prescricao.save()
        medicamento1 = medicamento.split(",")
        dosagem1 = dosagem.split(",")

        for i in range(len(medicamento1)):
            medc = Medicamento.objects.get(nome=medicamento1[i], dosagem=dosagem1[i])
            prescricao.med.add(medc)
        string = "Prescrição adicionada!"
        return render(request, "medico/erros2.html", {'string': string})

    else:
        medc = Medicamento.objects.get(nome=medicamento, dosagem=dosagem)
        consulta = Consulta.objects.get(id_consulta=id)
        prescricao = Prescricao.objects.create(data=data, toma=toma)
        prescricao.consulta = consulta
        prescricao.save()
        prescricao.med.add(medc)

        string = "Prescrição adicionada!"
        return render(request, "medico/erros2.html", {'string': string})

@login_required
def adicionar_observacoes(request, username,id, idu):
    form = ObservacoesForm()
    return render(request, 'medico/adicionar_observacoes.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def submeter_observacoes(request, username,id, idu):
    observacoes = request.POST["observacoes"]

    consulta = Consulta.objects.get(id_consulta= id)

    consulta.observacoes = observacoes
    consulta.save()

    string = "Observação adicionada!"
    return render(request, "medico/erros2.html", {'string':string})

@login_required
def adicionar_historico(request, username,id, idu):
    form = HistoricoForm()
    id = id
    return render(request, 'medico/adicionar_historico.html', context={'form': form, 'id':id, "username":username, 'idu':idu})

@login_required
def submeter_historico(request, username,id, idu):
    numutente = idu
    historico = request.POST["historico"]

    utente = Utente.objects.get(numutente=numutente)

    fichamedica = Ficha_medica.objects.get(utente=utente)
    fichamedica.historico += historico
    fichamedica.save()
    string = "Histórico adicionado à Ficha Médica!"
    return render(request, "medico/erros2.html", {'string': string})


@login_required
def ver_ficha_u(request, username,id, idu):


        utente = Utente.objects.get(numutente=idu)

        fichamedica = Ficha_medica.objects.get(utente=utente)

        if Medicao.objects.all().exists():
            medicoes = fichamedica.medicoes.all()

            return render(request, "medico/fichautente.html",
                          context={'fichamedica': fichamedica, 'medicoes': medicoes, "username": username, 'id':id,'idu': idu})
        else:
            return render(request, "medico/fichautente.html", context={'fichamedica': fichamedica, "username": username, 'id':id, 'idu': idu})



@login_required
def ver_exame_u(request, username,id, idu):

    lista_exames = []

    utente = Utente.objects.get(numutente=idu)
    fichamedica = Ficha_medica.objects.get(utente=utente)
    consultas = Consulta.objects.filter(fichamedica=fichamedica)
    for consulta in consultas:
        exames = Exame.objects.filter(consulta=consulta)
        if exames:
            lista_exames.append(exames)
    if len(lista_exames) == 0:
        string = "O Utente inserido não tem Exames!"
        return render(request, "medico/erros2.html", {'string': string})
    else:
        return render(request, "medico/exames_utente.html", context={'exames': lista_exames, "username": username, 'id':id, 'idu': idu})


@login_required
def ver_consulta_u(request, username,id, idu):

    utente = Utente.objects.get(numutente=idu)
    fichamedica = Ficha_medica.objects.get(utente=utente)

    if Consulta.objects.filter(fichamedica=fichamedica).exists():
        consultas = Consulta.objects.filter(fichamedica=fichamedica)

        return render(request, 'medico/consultas_utente.html', context={'consultas': consultas, "username": username, 'id':id, 'idu': idu})
    else:
        string = "Utente inserido não tem consultas realizadas!"
        return render(request, "medico/erros2.html", {'string': string})


@login_required
def ver_prescricoes(request, username,id, idu):
    form = ConsultaForm()
    return render(request, 'medico/ver_prescricoes_c.html', context={'form': form, "username": username, 'id':id, 'idu': idu})

@login_required
def prescricoes(request, username,id, idu):
    form = PrescricaoForm()
    id = request.GET["id_con"]
    lista_id = ""
    utente=Utente.objects.get(numutente=idu)
    fichamedica=Ficha_medica.objects.get(utente=utente)
    if Consulta.objects.filter(id_consulta=id, fichamedica=fichamedica).exists():

        consulta = Consulta.objects.get(id_consulta=id, fichamedica=fichamedica)

        if Prescricao.objects.filter(consulta=consulta).exists():
            prescricoes = Prescricao.objects.filter(consulta=consulta)
            for presc in prescricoes:
                lista_id += "_" + str(presc.id_prescricao)
            return render(request, "medico/prescricoes.html", context={'prescricoes': prescricoes, 'form': form, "username": username,'lista_id': lista_id, 'id':id, 'idu': idu})
        else:
            string = "Não há Prescrições associadas à Consulta pretendida!"
            return render(request, "medico/erros2.html", {'string': string})

    else:
        string = "Consulta inserida não existe ou não pertence ao Utente! Verifique as consultas do Utente..."
        return render(request, "medico/erros2.html", {'string': string})

@login_required
def medicamentos(request, username,id, lista_id, idu):
    id = request.GET["id_presc"]
    lista = lista_id.split("_")
    if id in lista_id:
        prescricao = Prescricao.objects.get(id_prescricao=id)
        medc = prescricao.med.all()

        return render(request, "medico/medicamentos.html", context={'medicamentos': medc, "username": username, 'id':id, 'idu': idu})
    else:
        string = "Esta prescrição não pertence à consulta pretendida!"
        return render(request, "medico/erros2.html", {'string': string})


#--------------------------------------------------------------------------------FUNCIONÁRIO--------------------------------------------------------#

def login_funcionario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username} ")
                return redirect('/alves_lda/funcionario/'+username)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'funcionario/login_funcionário.html', {'form': form})


def registar_funcionario(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        username = request.POST['username']
        x = username.replace("F", "")
        if "F" in username and Funcionario.objects.filter(numfunc=int(x)).exists():
            if form.is_valid():
                user = form.save()
                messages.success(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/alves_lda")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = NewUserForm()
    return render(request, "funcionario/registar_funcionario.html", context={"form": form})

@login_required
def funcionario(request, username):
    return render(request, 'funcionario/funcionário.html', {'username':username})

@login_required
def adicionar_u(request, username):
    form = UtenteForm()
    return render(request, 'funcionario/adicionar_utente.html', context={'form': form, 'username':username})

@login_required
def submeter_u(request, username):
    nome = request.POST["nome"]
    morada = request.POST["morada"]
    
    nif = request.POST["nif"]
    cc = request.POST["cc"]
    datanasc = request.POST["datanasc"]
    numutente = request.POST["numutente"]
    telefone = request.POST["telefone"]
    telefone_emergencia = request.POST["telefone_emergencia"]
    email = request.POST["email"]


    utente = Utente.objects.create(nome = nome, morada = morada, nif = nif, cc = cc, datanasc = datanasc, numutente = numutente,
                                   telefone = telefone, telefone_emergencia= telefone_emergencia, email = email)

    utente.save()

    fichamedica = Ficha_medica(utente=utente)
    fichamedica.save()

    string = "Utente adicionado!"
    return render(request, "funcionario/erro.html",{'string':string, 'username':username})

@login_required
def entrada_agenda(request,username):
    form = HistoricoConsultasForm()
    return render(request, 'funcionario/ent_agenda.html', context={'form': form, 'username':username})

@login_required
def ver_entrada_agenda(request,username):

    if Utente.objects.filter(numutente=request.GET['numutente']).exists():
        utente = Utente.objects.get(numutente=request.GET['numutente'])

        if Entrada_Agenda.objects.filter(utente=utente).exists():
            entradas_agenda = Entrada_Agenda.objects.filter(utente=utente)

            return render(request, 'funcionario/ver_ent_agenda.html', context={'consultas': entradas_agenda, 'username':username})
        else:
            string = "Utente inserido não tem consultas marcadas!"
            return render(request, "medico/erros2.html", {'string': string})
    else:
        string = "Utente inserido não existe! Insira de novo..."
        return render(request, "medico/erros2.html", {'string': string})

@login_required
def medicamento(request, username):
    form = MedicamentoNomeForm()
    return render(request, 'funcionario/medicamento.html', context={'form': form, 'username':username})

@login_required
def submeter_medicamento(request, username):

    lista_u = []
    lista_con = []
    nome = request.GET["nome"]
    if Medicamento.objects.filter(nome = nome).exists():
        medicamento = Medicamento.objects.filter(nome = nome)
        for medc in medicamento:
            prescricao = Prescricao.objects.filter(med = medc)
            for el in prescricao:
                consultas = el.consulta
                lista_con.append(consultas)

        for consulta in lista_con:
            fichamedica = consulta.fichamedica
            utente = fichamedica.utente
            numutente = utente.numutente
            utente_nome = utente.nome

            if [numutente,utente_nome] not in lista_u:
                lista_u.append([numutente,utente_nome])

        if len(lista_u)>0:
            return render(request,"funcionario/submeter_medicamento.html", context={'utentes' : lista_u, 'username':username})
        else:
            string = "Ainda nenhum utente tomou esse medicamento..."
            return render(request, "medico/erros2.html", {'string': string})
    else:
        string = "Medicamento inserido não existe! Tente de novo..."
        return render(request, "medico/erros2.html", {'string': string})

@login_required
def ver_utente(request, username):
    form = HistoricoConsultasForm()
    return render(request, "funcionario/numutente.html",  context={'form': form, 'username':username})

@login_required
def ver_info_utente(request, username):
    numutente = request.GET["numutente"]

    if Utente.objects.filter(numutente = numutente).exists():

        utente = Utente.objects.get(numutente = numutente)
        return render(request, "funcionario/lista_utentes.html", context={'utente' : utente, 'username':username})

    else:
        string = "Utente inserido não existe! Insira de novo..."
        return render(request, "medico/erros2.html", {'string': string})


#-------------------------------------------------------------------------------GESTOR----------------------------------------------------#

def login_gestor(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username} ")
                return redirect('/alves_lda/gestor/'+username)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'gestor/login_gestor.html', {'form': form})


def registar_gestor(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        username = request.POST['username']
        if "G" in username:
            if form.is_valid():
                user = form.save()
                messages.success(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/alves_lda")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = NewUserForm()
    return render(request, "gestor/registar_gestor.html", context={"form": form})

@login_required
def gestor(request, username):
    return render(request, 'gestor/gestor.html', {"username":username})

@login_required
def adicionar_f(request, username):
    form = FuncionarioForm()

    return render(request, "gestor/adicionar_funcionario.html", context={'form': form, "username":username})

@login_required
def submeter_f(request, username):
    nome = request.POST["nome"]
    morada = request.POST["morada"]
    nif = request.POST["nif"]
    cc = request.POST["cc"]
    datanasc = request.POST["datanasc"]
    numfunc = request.POST["numfunc"]

    funcionario = Funcionario.objects.create(nome = nome, morada = morada, nif = nif, cc = cc, datanasc = datanasc, numfunc = numfunc)

    funcionario.save()

    string = "Funcionário adicionado!"
    return render (request, "gestor/erro.html", context={'string':string, "username":username})

@login_required
def adicionar_m(request, username):
    form = MedicoForm()

    return render(request, "gestor/adicionar_medico.html", context={'form': form, "username":username})

@login_required
def submeter_m(request, username):
    nome = request.POST["nome"]
    morada = request.POST["morada"]
    nif = request.POST["nif"]
    cc = request.POST["cc"]
    datanasc = request.POST["datanasc"]
    cedula = request.POST["cedula"]
    especialidade = request.POST["especialidade"]

    medico = Medico.objects.create(nome = nome, morada = morada, nif = nif, cc = cc, datanasc = datanasc, cedula = cedula, especialidade = especialidade)

    medico.save()
    string = "Médico adicionado!"
    return render(request, "gestor/erro.html", context={'string':string, "username":username})

@login_required
def adicionar_medc(request, username):
    form = MedicamentoForm()
    return render(request, "gestor/adicionar_medicamento.html", context={'form': form, "username":username})

@login_required
def submeter_medc(request, username):
    dci = request.POST["dci"]
    nome = request.POST["nome"]
    formafarmaceutica = request.POST["formafarmaceutica"]
    dosagem = request.POST["dosagem"]
    estadoautorizacao = request.POST["estadoautorizacao"]
    generico = request.POST["generico"]
    titular_aim = request.POST["titular_aim"]

    if generico == "on":
        generico = True
    else:
        generico = False

    medicamento = Medicamento.objects.create(dci = dci, nome = nome, formafarmaceutica = formafarmaceutica, dosagem = dosagem,
                                             estadoautorizacao = estadoautorizacao, generico = generico, titular_aim = titular_aim)

    medicamento.save()

    string = "Medicamento adicionado!"
    return render(request, "gestor/erro.html", context={'string':string, "username":username})


@login_required
def ver_utente_gestor(request, username):

    utente = Utente.objects.all()

    return render(request, "gestor/lista_utentes.html", context={'utente': utente, "username":username})


@login_required
def ver_medico(request, username):

    medicos =Medico.objects.all()
    return render(request, 'gestor/lista_medicos.html', context={'medicos': medicos, "username":username})

@login_required
def ver_funcionario(request, username):

    funcionarios = Funcionario.objects.all()
    return render(request, 'gestor/lista_funcionarios.html', context={'funcionarios': funcionarios, "username":username})

@login_required
def ver_medicamento(request, username):
    medicamento = Medicamento.objects.all()
    return render(request, 'gestor/lista_medicamentos.html', context={'medicamento': medicamento, "username":username})

@login_required
def ver_idade(request, username):
    form =UtenteIdadeForm()
    return render(request, 'gestor/ver_utentes_idade.html', context={'form': form, "username":username})

@login_required
def ver_idade_submeter(request, username):
    ano = request.GET["ano"]
    utentes = Utente.objects.all()

    lista_u = []
    for utente in utentes:
        if int(utente.datanasc.year) == int(ano):

            lista_u.append(utente)
    if len(lista_u)==0:
        string = "Não há ninguém com a idade pretendida! Adicione de novo..."
        return render(request, "gestor/erros2.html", {'string': string})
    else:
        return render(request, 'gestor/utentes_idade.html', context={'utentes': lista_u, "username":username})

@login_required
def povoar(request, username):
    return render(request, 'gestor/povoargeral.html', context={"username": username})

@login_required
def popular_utentes(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheiroutente.html', context={'form': form, "username": username})

@login_required
def populate_utentes(request, username):

    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8" ) as f:

        while True:
            linha = f.readline()
            if not linha:
                break
            utente = linha.split(";")
            for i in range(len(utente)):
                if utente[i].startswith("\""):
                    utente[i] = utente[i].replace('"',' ').strip()
            lista_dn = utente[4].split("-")
            for i in range(len(lista_dn)):
                if lista_dn[i].startswith("\""):
                    lista_dn[i] = lista_dn[i].replace('"', ' ').strip()
            lista_dn[2] = lista_dn[2].replace('"', ' ').strip()
            utente[8] = utente[8].replace("\n"," ").strip()
            utente[7] = utente[7].replace("(", " ").strip()
            utente[7] = utente[7].replace(")", " ").strip()

            u = Utente.objects.create(nome = str(utente[0]),
                                      morada = str(utente[1]),
                                      nif = str(utente[2]),
                                      cc = str(utente[3]),
                                      datanasc = date(int(lista_dn[0]), int(lista_dn[1]), int(lista_dn[2])),
                                      numutente = str(utente[5]),
                                      telefone = str(utente[6]), telefone_emergencia = str(utente[7]), email = str(utente[8]))
            u.save()

        string = "Utentes Povoados!"
        return render(request, "gestor/erro.html", {'string': string, "username": username })

@login_required
def popular_medicos(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheiromedico.html', context={'form': form, "username": username})

@login_required
def populate_medicos(request, username):
    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8") as f:

        while True:
            linha = f.readline()
            if not linha:
                break
            medico = linha.split(";")
            for i in range(len(medico)):
                if medico[i].startswith("\""):
                    medico[i] = medico[i].replace('"',' ').strip()
            lista_dn = medico[4].split("-")
            m = Medico.objects.create(nome=str(medico[0]),
                                      morada=str(medico[1]),
                                      nif=str(medico[2]),
                                      cc=str(medico[3]),
                                      datanasc=date(int(lista_dn[0]), int(lista_dn[1]), int(lista_dn[2])),
                                      cedula=str(medico[5]),
                                      especialidade=str(medico[6]))
            m.save()
        string = "Medicos Povoados!"
        return render(request, "gestor/erro.html", {'string': string, "username": username })

@login_required
def popular_funcionarios(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheirofunc.html', context={'form': form, "username": username})

@login_required
def populate_funcionarios(request, username):

    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8") as f:
        while True:
            linha = f.readline()
            if not linha:
                break
            funcionario = linha.split(";")
            for i in range(len(funcionario)):
                if funcionario[i].startswith("\""):
                    funcionario[i] = funcionario[i].replace('"',' ').strip()
            lista_dn = funcionario[4].split("-")
            funcionario[5] = funcionario[5].replace("\n", " ").strip()
            func = Funcionario.objects.create(nome=str(funcionario[0]),
                                      morada=str(funcionario[1]),
                                      nif=str(funcionario[2]),
                                      cc=str(funcionario[3]),
                                      datanasc=date(int(lista_dn[0]), int(lista_dn[1]), int(lista_dn[2])),
                                      numfunc=int(funcionario[5]))

            func.save()
        string = "Funcionários Povoados!"
        return render(request, "gestor/erro.html", {'string': string, "username": username})

@login_required
def popular_medicamentos(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheirosmedicamento.html', context={'form': form, "username": username})

@login_required
def populate_medicamentos(request, username):
    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8") as f:

        while True:
            linha = f.readline()
            if not linha:
                break
            medicamento = linha.split(";")
            if str(medicamento[6]) == "N":
                medicamento[6] = False
            else:
                medicamento[6] = True
            medc = Medicamento.objects.create(
                                      dci=str(medicamento[1]),
                                      nome=str(medicamento[2]),
                                      formafarmaceutica=str(medicamento[3]),
                                      dosagem=str(medicamento[4]),
                                      estadoautorizacao=str(medicamento[5]), generico=medicamento[6], titular_aim=str(medicamento[7]))

            medc.save()
        string = "Medicamentos Povoados!"
        return render(request, "gestor/erro.html", {'string': string, "username": username})

@login_required
def populate_fichasmedicas(request, username):
    utentes = Utente.objects.all()
    for utente in utentes:
        fichamedica = Ficha_medica(utente = utente)
        fichamedica.save()
    string = "Fichas Médicas Povoadas!"
    return render(request, "gestor/erro.html", {'string': string, "username": username})

@login_required
def popular_historico(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheirohist.html', context={'form': form, "username": username})

def add_historico(request, username):
    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8") as f:

        while True:
            linha = f.readline()
            if not linha:
                break
            tokens = linha.split(";")
            for i in range(len(tokens)):
                if tokens[i].startswith("\""):
                    tokens[i] = tokens[i].replace('"',' ').strip()
            utente = Utente.objects.get(numutente = tokens[0])
            fichamedica = Ficha_medica.objects.get(utente = utente)
            fichamedica.historico = tokens[1]
            fichamedica.save()
        string = "Histórico Povoado!"
        return render(request, "gestor/erro.html", {'string': string, "username": username})

@login_required
def popular_consultas(request, username):
    form = FicheiroForm()
    return render(request, 'gestor/ficheirocons.html', context={'form': form, "username": username})

@login_required
def populate_consultas(request, username):
    ficheiro = request.POST["ficheiro"]

    with open(ficheiro, encoding="utf8") as f:

        k=0
        while k<10001:
            linha = f.readline()
            if not linha:
                break
            tokens = linha.split(";")
            for i in range(len(tokens)):
                if tokens[i].startswith("\""):
                    tokens[i] = tokens[i].replace('"', ' ').strip()
            data = tokens[2].split("-")

            medico = Medico.objects.get(cedula=tokens[0])


            utente = Utente.objects.get(numutente=tokens[1])
            fichamedica = Ficha_medica.objects.get(utente=utente)

            consulta = Consulta(data=date(int(data[0]), int(data[1]), int(data[2])), medico=medico,
                                observacoes=tokens[3],fichamedica = fichamedica)
            consulta.save()

            for i in range(4,len(tokens)):
                token = tokens[i]
                token = token.replace('[', ' ').replace( ']', ' ').strip()
                rtokens = token.split(",")
                for j in range(len(rtokens)):
                    rtokens[j] = rtokens[j].replace('\'', ' ').strip()

                data1 = rtokens[0].split("-")


                medicamento = Medicamento.objects.get(id_medicamento = rtokens[1])

                prescricao = Prescricao(data=date(int(data1[0]), int(data1[1]), int(data1[2])), toma = rtokens[2])
                prescricao.consulta = consulta
                prescricao.save()

                prescricao.med.add(medicamento)
        k+=1
        string = "Consultas Povoadas!"
        return render(request, "gestor/erro.html", {'string': string, "username": username})

# -------------------------------------------------------FIM------------------------------------------------------------------#