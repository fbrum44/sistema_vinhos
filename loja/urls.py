from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro_view, name='cadastrar'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('cadastrar-usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
]
