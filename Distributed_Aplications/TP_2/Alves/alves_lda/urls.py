"""Alves URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from . import views

app_name = "alves_lda"

urlpatterns = [
#-------------------------------------------INICIO---------------------------------------------#

    path('admin/', admin.site.urls),
    path('', views.homepage_view, name="inicial"),
    path('sair/', views.sair),

#-------------------------------------------UTENTE---------------------------------------------#

    path('loginutente/', views.login_utente),
    path('registar_utente/',views.registar_utente),
    path('utente/<str:username>/', views.utente),
    path('utente/<str:username>/marcar_consulta/', views.marcar_consulta),
    path('utente/<str:username>/marcar_consulta/marcar/', views.marcar),
    path('utente/<str:username>/marcar_consulta/horariofuncionamento/', views.horario),
    path('utente/<str:username>/marcar_consulta/especialidades', views.especialidades),
    path('utente/<str:username>/historico_consultas/', views.historico_consultas),
    path('utente/<str:username>/historico_exames/', views.historico_exames),
    path('utente/<str:username>/veragenda/', views.veragenda),
    path('utente/<str:username>/cancelar_consulta/', views.cancelar_consulta),
    path('utente/<str:username>/cancelar_consulta/cancelar/', views.cancelar),


#-------------------------------------------MEDICO---------------------------------------------#

    path('loginmedico/', views.login_medico),
    path('registar_medico/',views.registar_medico),
    path('medico/<str:username>/', views.medico),
    path('medico/<str:username>/hist_consultas/', views.historico_consultas_medico),
    path('medico/<str:username>/realizar_consulta/', views.realizar_consulta),
    path('medico/<str:username>/realizar_consulta/entradagenda_medico/', views.entrada_agenda_medico),
    path('medico/<str:username>/realizar_consulta/entradagenda_medico/ver', views.ver_entrada_agenda_medico),
    path('medico/<str:username>/realizar_consulta/adicionar/', views.realizar_consulta_adicionar),
    path('medico/<str:username>/realizar_consulta/adicionar/marcar_exame/<int:id>/<str:idu>', views.marcar_exame),
    path('medico/<str:username>/realizar_consulta/adicionar/marcar_exame/submeter/<int:id>/<str:idu>', views.submeter_exame),
    path('medico/<str:username>/realizar_consulta/adicionar/medicoes/<int:id>/<str:idu>', views.adicionar_medicoes),
    path('medico/<str:username>/realizar_consulta/adicionar/medicoes/submeter/<int:id>/<str:idu>', views.submeter_medicoes),
    path('medico/<str:username>/realizar_consulta/adicionar/prescricoes/<int:id>/<str:idu>', views.adicionar_prescricoes),
    path('medico/<str:username>/realizar_consulta/adicionar/prescricoes/submeter/<int:id>/<str:idu>', views.submeter_prescricoes),
    path('medico/<str:username>/realizar_consulta/adicionar/observacoes/<int:id>/<str:idu>', views.adicionar_observacoes),
    path('medico/<str:username>/realizar_consulta/adicionar/observacoes/submeter/<int:id>/<str:idu>', views.submeter_observacoes),
    path('medico/<str:username>/realizar_consulta/adicionar/historico/<int:id>/<str:idu>', views.adicionar_historico),
    path('medico/<str:username>/realizar_consulta/adicionar/historico/submeter/<int:id>/<str:idu>', views.submeter_historico),
    path('medico/<str:username>/realizar_consulta/adicionar/medicamento/<int:id>/<str:idu>', views.infomedicamento),
    path('medico/<str:username>/realizar_consulta/adicionar/medicamento/ver/<int:id>/<str:idu>', views.verinfomedicamento),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_ficha_u/<int:id>/<str:idu>',views.ver_ficha_u),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_exames_u/<int:id>/<str:idu>', views.ver_exame_u),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_consultas_u/<int:id>/<str:idu>', views.ver_consulta_u),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_prescricoes_c/<int:id>/<str:idu>', views.ver_prescricoes),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_prescricoes_c/prescricoes/<int:id>/<str:idu>', views.prescricoes),
    path('medico/<str:username>/realizar_consulta/adicionar/ver_prescricoes_c/prescricoes/<str:lista_id>/medicamento/<int:id>/<str:idu>', views.medicamentos),

#-------------------------------------------FUNCIONÁRIO---------------------------------------------#

    path('loginfuncionario/', views.login_funcionario),
    path('registar_funcionario/',views.registar_funcionario),
    path('funcionario/<str:username>/', views.funcionario),
    path('funcionario/<str:username>/adicionar_utente/', views.adicionar_u),
    path('funcionario/<str:username>/adicionar_utente/submeter', views.submeter_u),
    path('funcionario/<str:username>/entrada_agenda/', views.entrada_agenda),
    path('funcionario/<str:username>/entrada_agenda/ver', views.ver_entrada_agenda),
    path('funcionario/<str:username>/medicamento/', views.medicamento),
    path('funcionario/<str:username>/medicamento/submeter', views.submeter_medicamento),
    path('funcionario/<str:username>/ver_lista_u/', views.ver_utente),
    path('funcionario/<str:username>/ver_lista_u/submeter', views.ver_info_utente),

#-------------------------------------------GESTOR---------------------------------------------#

    path('logingestor/', views.login_gestor),
    path('registar_gestor/',views.registar_gestor),
    path('gestor/<str:username>/', views.gestor),
    path('gestor/<str:username>/adicionar_funcionario/', views.adicionar_f),
    path('gestor/<str:username>/adicionar_funcionario/submeter', views.submeter_f),
    path('gestor/<str:username>/adicionar_medico/', views.adicionar_m),
    path('gestor/<str:username>/adicionar_medico/submeter', views.submeter_m),
    path('gestor/<str:username>/adicionar_medicamento/', views.adicionar_medc),
    path('gestor/<str:username>/adicionar_medicamento/submeter', views.submeter_medc),
    path('gestor/<str:username>/ver_listaU/', views.ver_utente_gestor),
    path('gestor/<str:username>/ver_listaM/', views.ver_medico),
    path('gestor/<str:username>/ver_listaF/', views.ver_funcionario),
    path('gestor/<str:username>/ver_listaMedicamentos/',views.ver_medicamento),
    path('gestor/<str:username>/ver_idade/',views.ver_idade),
    path('gestor/<str:username>/ver_idade/submeter', views.ver_idade_submeter),
    path('gestor/<str:username>/povoar/',views.povoar),
    path('gestor/<str:username>/povoar/populate_utentes/',views.popular_utentes),
    path('gestor/<str:username>/povoar/populate_utentes/popular', views.populate_utentes),
    path('gestor/<str:username>/povoar/populate_medicos/',views.popular_medicos),
    path('gestor/<str:username>/povoar/populate_medicos/popular',views.populate_medicos),
    path('gestor/<str:username>/povoar/populate_funcionarios/',views.popular_funcionarios),
    path('gestor/<str:username>/povoar/populate_funcionarios/popular',views.populate_funcionarios),
    path('gestor/<str:username>/povoar/populate_medicamentos/', views.popular_medicamentos),
    path('gestor/<str:username>/povoar/populate_medicamentos/popular',views.populate_medicamentos),
    path('gestor/<str:username>/povoar/populate_fichasmedicas/',views.populate_fichasmedicas),
    path('gestor/<str:username>/povoar/add_historico/',views.popular_historico),
    path('gestor/<str:username>/povoar/add_historico/popular',views.add_historico),
    path('gestor/<str:username>/povoar/populate_consultas/',views.popular_consultas),
    path('gestor/<str:username>/povoar/populate_consultas/popular', views.populate_consultas),

]
#-------------------------------------------FIM---------------------------------------------#

