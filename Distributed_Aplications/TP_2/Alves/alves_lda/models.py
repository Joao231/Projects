from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import *


class Pessoa(models.Model):
    nome = models.CharField(max_length=200, null=False)
    morada = models.CharField(max_length=500, null=False)
    nif = models.CharField(unique=True, max_length=9, null=False)
    cc = models.CharField(max_length=12, null=False)
    datanasc = models.DateField(null=False)

    class Meta:
        abstract = True


class Utente(Pessoa):
    id_utente = models.AutoField(primary_key=True, null=False)
    numutente = models.CharField(unique=True, max_length=200, null=False)
    telefone = models.CharField(max_length=14, null=False)
    telefone_emergencia = models.CharField(max_length=14, null=False)
    email = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.nome


class Medico(Pessoa):
    id_medico = models.AutoField(primary_key=True, null=False)
    cedula = models.CharField(unique=True, max_length=200, null=False)
    especialidade = models.CharField(max_length=200, null=False)

    def __str__(self):
        return str(self.nome) + ":" + str(self.morada)  + ":" + str(self.nif)  + ":" + str(self.cc)  + ":" + str(self.datanasc)  + ":" + str(self.cedula)  + ":" + str(self.especialidade)


class Funcionario(Pessoa):
    id_funcionario = models.AutoField(primary_key=True, null=False)
    numfunc = models.IntegerField(unique=True, null=False)

    def __str__(self):
        return str(self.nome) + ":" + str(self.morada)  + ":" + str(self.nif)  + ":" + str(self.cc)  + ":" + str(self.datanasc) + ":" + str(self.numfunc)


class Gestor(Pessoa):
    id_gestor = models.AutoField(primary_key=True, null=False)
    telefone = models.CharField(max_length=14, null=False)
    telefone_emergencia = models.CharField(max_length=14, null=False)
    email = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True, null=False)
    dci = models.CharField(max_length=200, null=False)
    nome = models.CharField(max_length=200, null=False)
    formafarmaceutica = models.CharField(max_length=200, null=False)
    dosagem = models.CharField(max_length=200, null=True)
    estadoautorizacao = models.CharField(max_length=200, null=False)
    generico = models.BooleanField(default=True)
    titular_aim = models.CharField(max_length=200, null=False)

    def __str__(self):
        return str(self.id_medicamento) + ":" +str(self.dci) + ":" + str(self.nome) + ":" + str(self.formafarmaceutica) + ":" + str(self.dosagem) + ":" + str(self.estadoautorizacao) + ":" + str(self.generico) + ":" + str(self.titular_aim)


class Medicao(models.Model):
    id_medicao = models.AutoField(primary_key=True, null=False)
    data = models.DateField(null=False)
    peso = models.DecimalField(max_digits=200, decimal_places=5, null=False)
    glicemia = models.DecimalField(max_digits=200, decimal_places=5, null=False)
    altura = models.IntegerField(null=False)
    tensaoarterial = models.IntegerField(null=False)
    colesterol = models.IntegerField(null=False)
    trigliceridios = models.IntegerField(null=False)
    saturacao = models.IntegerField(null=False)
    inr = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id_medicao) + ":" + str(self.data) + ":" + str(self.peso) + ":" + str(self.glicemia) + ":" + str(self.altura) + ":" + str(self.tensaoarterial) + ":" + str(self.colesterol) + ":" + str(self.trigliceridios) + ":" + str(self.saturacao) + ":" + str(self.inr)

class Ficha_medica(models.Model):
    id_ficha = models.AutoField(primary_key=True, null=False)
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE)
    medicoes = models.ManyToManyField(Medicao)
    historico = models.CharField(max_length=2000, blank = True)

    def __str__(self):
        return str(self.id_ficha) + ":" + str(self.utente) + ":" + str(self.historico)

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True, null=False)
    data = models.DateField(null=True)
    observacoes = models.CharField(max_length=2000, blank = True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null = True)
    fichamedica = models.ForeignKey(Ficha_medica, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id_consulta) + ":" + str(self.data) + ":" + str(self.medico) + ":" + str(self.observacoes)

class Prescricao(models.Model):
    id_prescricao = models.AutoField(primary_key=True, null=False)
    data = models.DateField(null=False)
    med = models.ManyToManyField(Medicamento)
    toma = models.CharField(max_length=200, null=False)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id_prescricao) + ":" + str(self.med) + ":" + str(self.data) + ":" + str(self.toma) + ":" + str(self.consulta)



class Exame(models.Model):
    id_exame = models.AutoField(primary_key=True, null=False)
    tipo = models.CharField(max_length=200, null=False)
    local = models.CharField(max_length=200, null=False)
    data_hora = models.DateTimeField(null=False)
    duracao = models.TimeField()
    preco = models.DecimalField(max_digits=200, decimal_places=5, null=False)
    estado = models.BooleanField(max_length=200, null=False)
    observacoes = models.CharField(max_length=200, null=False)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id_exame) + ":" + str(self.tipo) + ":" + str(self.data_hora) + ":" + str(self.observacoes)

class Entrada_Agenda(models.Model):
    id_entradagenda = models.AutoField(primary_key=True, null=False)
    data_hora = models.DateTimeField(null=False)
    estado = models.CharField(max_length=20)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.utente) + ":" + str(self.medico)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
