from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm


class RegistarutenteModelForm(ModelForm):
    class Meta:
        model = Utente
        fields = ['nome', 'morada', 'nif', 'cc', 'datanasc', 'numutente', 'telefone', 'telefone_emergencia', 'email']

class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        db_table = 'auth_user'
        fields = ("username","email","password1","password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserForm(AuthenticationForm):
     #email = forms.EmailField(required=True)

     class Meta:
         model = User
         db_table = 'auth_user'
         fields = ("username", "password")
     def save(self, commit=True, *args, **kwargs):
         user = super(UserForm, self).save(commit=False, *args, **kwargs)
         #user.email = self.cleaned_data['email']
         if commit:
             user.save()
         return user


class MarcarConsultaForm(forms.Form):

    especialidade = forms.CharField(label = "Especialidade")
    data = forms.DateField(label="Data")
    hora = forms.TimeField(label = "Hora")

class HistoricoConsultasForm(forms.Form):
    numutente = forms.CharField(label = "Número de utente")

class AgendaMedicoForm(forms.Form):
    data = forms.DateField(label = "Data")


class FichasmedicasForm(forms.Form):
    cedula = forms.CharField(label = "Cédula do médico")


class RealizarConsultaForm(forms.Form):
    numutente = forms.CharField(label = "Número de utente")
    data = forms.DateField(label="Data")
    hora = forms.TimeField(label = "Hora")
    cedula = forms.CharField(label="Cédula do médico")


class MarcarExameForm(forms.Form):
    tipo = forms.CharField(label = "Tipo")
    local = forms.CharField(label="Local")
    data_hora = forms.DateTimeField(label = "Data e Hora")
    duracao = forms.TimeField(label="Duração")
    preco = forms.DecimalField(label="Preço")
    estado = forms.BooleanField(label="Estado")
    observacoes = forms.CharField(label="Observações")

class MedicoesForm(forms.Form):

    data = forms.DateField(label = "Data")
    peso = forms.DecimalField(label = "Peso")
    glicemia = forms.DecimalField(label = "Glicemia")
    altura = forms.IntegerField(label = "Altura")
    tensaoarterial = forms.IntegerField(label = "Tensão arterial")
    colesterol = forms.IntegerField(label = "Colesterol")
    trigliceridios = forms.IntegerField(label = "Trigliceridios")
    saturacao = forms.IntegerField(label = "Saturação")
    inr = forms.IntegerField(label = "INR")


class PrescricoesForm(forms.Form):

    data = forms.DateField(label = "Data")
    medicamento = forms.CharField(label="Medicamento")
    dosagem = forms.CharField(label="Dosagem")
    toma = forms.CharField(label = "Toma")


class ObservacoesForm(forms.Form):

    observacoes = forms.CharField(label = "Observações")


class HistoricoForm(forms.Form):

    historico = forms.CharField(label = "Historico")



class UtenteForm(forms.Form):
    nome = forms.CharField(label="Nome")
    morada = forms.CharField(label="Morada")
    nif = forms.CharField(label="NIF")
    cc = forms.CharField(label="CC")
    datanasc = forms.DateField(label="Data de nascimento")
    numutente = forms.CharField(label="Numero de utente")
    telefone = forms.CharField(label="Telefone")
    telefone_emergencia = forms.CharField(label="Telefone de emergência")
    email = forms.CharField(label="Email")

class MedicamentoNomeForm(forms.Form):
    nome = forms.CharField(label="Nome")


class FuncionarioForm(forms.Form):
    nome = forms.CharField(label="Nome do funcionário")
    morada = forms.CharField(label="Morada")
    nif = forms.CharField(label="NIF")
    cc = forms.CharField(label="CC")
    datanasc = forms.DateField(label="Data de nascimento")
    numfunc = forms.IntegerField(label="Número do funcionário")


class MedicoForm(forms.Form):
    nome = forms.CharField(label="Nome do médico")
    morada = forms.CharField(label="Morada")
    nif = forms.CharField(label="NIF")
    cc = forms.CharField(label="CC")
    datanasc = forms.DateField(label="Data de nascimento")
    cedula = forms.CharField(label="Cédula")
    especialidade = forms.CharField(label="Especialidade")


class MedicamentoForm(forms.Form):
    dci = forms.CharField(label="DCI")
    nome = forms.CharField(label="Nome")
    formafarmaceutica = forms.CharField(label="Forma farmacêutica")
    dosagem = forms.CharField(label="Dosagem")
    estadoautorizacao = forms.CharField(label="Estado de autorização")
    generico = forms.BooleanField(label="Genérico")
    titular_aim = forms.CharField(label="Titular AIM")


class UtenteIdadeForm(forms.Form):
    ano = forms.CharField(label="Ano de Nascimento")


class ConsultaForm(forms.Form):
    id_con = forms.CharField(label="ID da Consulta")

class PrescricaoForm(forms.Form):
    id_presc = forms.CharField(label="ID da Prescricao")

class FicheiroForm(forms.Form):
    ficheiro = forms.CharField(label="Path do Ficheiro")