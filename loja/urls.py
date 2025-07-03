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
    path('logout/', views.logout_view, name='logout'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('adicionar_ao_carrinho/<str:vinho_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('meu_carrinho/', views.meu_carrinho, name='meu_carrinho'), 
    path('remover_do_carrinho/<str:vinho_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('efetuar_pagamento/', views.efetuar_pagamento, name='efetuar_pagamento'),
    path('historico/', views.historico, name='historico'),     
]
