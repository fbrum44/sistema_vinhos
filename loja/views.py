from django.shortcuts import render, redirect
from .forms import CadastroForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# MongoDB imports
from .mongodb import db

# Coleção de usuários no Mongo
usuarios_collection = db['usuarios']


def index(request):
    return render(request, 'loja/index.html')

def sobre(request):
    return render(request, 'loja/sobre.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        print("Dados recebidos:", request.POST)
        if form.is_valid():
            print("Formulário válido. Salvando...")
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro em {field}: {error}")
            return redirect('index')
    else:
        return redirect('index')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        senha = request.POST.get('password')
        print(f"Tentando login com email: {email} e senha: {senha}")
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos. Tente novamente.")
            return redirect('index')
    return redirect('index')

@login_required
def dashboard(request):
    user = request.user
    return render(request, 'loja/dashboard.html', {'user': user})

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        nascimento = request.POST.get('nascimento')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        novo_usuario = {
            'nome': nome,
            'nascimento': nascimento,
            'cpf': cpf,
            'email': email,
            'senha': senha
        }

        usuarios_collection.insert_one(novo_usuario)
        return redirect('listar_usuarios')

    return render(request, 'loja/cadastrar_usuario.html')

def listar_usuarios(request):
    usuarios = list(usuarios_collection.find())
    return render(request, 'loja/listar_usuarios.html', {'usuarios': usuarios})
