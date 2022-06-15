from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Gestor)
admin.site.register(Medico)
admin.site.register(Funcionario)
admin.site.register(Utente)
admin.site.register(Medicamento)
admin.site.register(Prescricao)
admin.site.register(Medicao)
admin.site.register(Consulta)
admin.site.register(Ficha_medica)
admin.site.register(Entrada_Agenda)