from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro_view, name='cadastrar'),
    path('login/', views.login_view, name='login'),
    path('verifica-modal/', views.verifica_modal, name='verifica_modal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('cadastrar-vinho/', views.cadastrar_vinho, name='cadastrar_vinho'),
    path('vinhos/', views.listar_vinhos, name='listar_vinhos'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
