from django.shortcuts import render

def index(request):
    return render(request, 'loja/index.html')

def cadastro(request):
    return render(request, 'loja/cadastro.html')

def login(request):
    return render(request, 'loja/login.html')

