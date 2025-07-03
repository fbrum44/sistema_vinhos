from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from loja.mongodb import usuarios_collection, vinhos_collection
from datetime import datetime
from bson.objectid  import ObjectId



# MongoDB imports
from .mongodb import db

# Coleção de usuários no Mongo
usuarios_collection = db['usuarios']
historico_collection = db['historico']


def index(request):
    return render(request, 'loja/index.html')

def sobre(request):
    return render(request, 'loja/sobre.html')

def cadastro_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')
        email = request.POST.get('username')
        senha1 = request.POST.get('password1')
        senha2 = request.POST.get('password2')

        if senha1 != senha2:
            messages.error(request, "As senhas não coincidem. Tente novamente.")
            # Reexibir o formulário com os dados já preenchidos (menos as senhas)
            context = {
                'nome_completo': nome,
                'data_nascimento': nascimento,
                'cpf': cpf,
                'username': email,
            }
            return render(request, 'loja/index.html', context)
        
        # Verifica se já existe usuário com esse email ou CPF no MongoDB
        if usuarios_collection.find_one({"$or": [{"email": email}, {"cpf": cpf}]}):
            messages.error(request, "Já existe um usuário com esse e-mail ou CPF.")
            context = {
                'nome_completo': nome,
                'data_nascimento': nascimento,
                'cpf': cpf,
                'username': email,
            }
            return render(request, 'loja/index.html', context)

        novo_usuario = {
            'nome_completo': nome,
            'data_nascimento': nascimento,
            'cpf': cpf,
            'email': email,
            'senha': make_password(senha1)
        }

        usuarios_collection.insert_one(novo_usuario)
        messages.success(request, "Cadastro realizado com sucesso!")
        return render(request, 'loja/index.html')

    return render(request, 'loja/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        senha = request.POST.get('password')
        
        usuario = usuarios_collection.find_one({'email': email})

        if usuario and check_password(senha, usuario['senha']):
            request.session['usuario_nome'] = usuario['nome_completo']
            request.session['usuario_email'] = usuario['email']
            request.session['is_admin'] = usuario.get('is_admin', False)

            if usuario.get('is_admin', False):
                return redirect('cadastrar_vinho')  
            else:
                return redirect('dashboard')

        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            request.session['login_erro'] = True
            return redirect('index')
            
        
    return render(request, 'loja/index.html')

def dashboard(request):
    usuario_email = request.session.get('usuario_email')

    if not usuario_email:
        return redirect('login')

    usuario = usuarios_collection.find_one({'email': usuario_email})

    if not usuario:
        return redirect('login')
    
    data_nascimento = usuario.get('data_nascimento')
    if data_nascimento:
        try:
            data_formatada = datetime.strptime(data_nascimento, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            data_formatada = data_nascimento 
    else:
        data_formatada = ""

    # Preparar dados para enviar ao template
    context = {
        'nome_completo': usuario.get('nome_completo', ''),
        'data_nascimento': data_formatada,
        'cpf': usuario.get('cpf', ''),
        'email': usuario.get('email', ''),
    }

    return render(request, 'loja/dashboard.html', context)

def listar_usuarios(request):
    usuarios = list(usuarios_collection.find())
    return render(request, 'loja/listar_usuarios.html', {'usuarios': usuarios})

def verifica_modal(request):
    modal = 'register'  
    if request.session.get('login_erro'):
        modal = 'login'
        del request.session['login_erro']
    return JsonResponse({'modal': modal})

def cadastrar_vinho(request):
    if not request.session.get('is_admin', False):
        messages.error(request, "Acesso negado: você precisa ser administrador.")
        return redirect('index')
    
    if request.method == 'POST':
        tipo_vinho = request.POST.get('tipo_vinho')
        tipo_uva = request.POST.get('tipo_uva')
        pais = request.POST.get('pais_origem')
        safra = request.POST.get('safra')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco')
        imagem_url = request.POST.get('imagem')

        if not (tipo_vinho and tipo_uva and pais and safra and preco):
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, 'loja/cadastrar_vinho.html')

        novo_vinho = {
            "tipo_do_vinho": tipo_vinho.title(),
            "tipo_da_uva": tipo_uva.title(),
            "pais_origem": pais.title(),
            "safra": int(safra),
            "quantidade": int(quantidade),
            "preco": float(preco),
            "imagem_url": imagem_url
        }

        vinhos_collection.insert_one(novo_vinho)
        messages.success(request, "Vinho cadastrado com sucesso!")
        return redirect('cadastrar_vinho')  

    return render(request, 'loja/cadastrar_vinho.html')

def listar_vinhos(request):
    vinhos = list(vinhos_collection.find())
    return render(request, 'loja/listar_vinhos.html', {'vinhos': vinhos})

def editar_perfil(request):
    if 'usuario_email' not in request.session:
        messages.error(request, "Você precisa estar logado para editar seu perfil.")
        return redirect('index')

    usuario = usuarios_collection.find_one({"email": request.session['usuario_email']})

    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha and senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return redirect('dashboard')

        novos_dados = {
            "nome_completo": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "email": email
        }

        if senha:
            novos_dados["senha"] = make_password(senha)

        usuarios_collection.update_one(
            {"email": request.session['usuario_email']},
            {"$set": novos_dados}
        )

        request.session['usuario_email'] = email 
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('dashboard')

    return render(request, 'loja/perfil.html', {
        "nome_completo": usuario.get("nome_completo", ""),
        "data_nascimento": usuario.get("data_nascimento", ""),
        "cpf": usuario.get("cpf", ""),
        "email": usuario.get("email", "")
    })

def logout_view(request):
    request.session.flush()  # limpa toda a sessão do usuário
    messages.success(request, "Logout realizado com sucesso.")
    return redirect('index')  

def excluir_conta(request):
    if 'usuario_email' not in request.session:
        messages.error(request, "Você precisa estar logado para excluir a conta.")
        return redirect('index')

    usuarios_collection.delete_one({'email': request.session['usuario_email']})
    request.session.flush()  
    messages.success(request, "Conta excluída com sucesso.")
    return redirect('index')

def catalogo(request):
    
    tipos = request.GET.getlist('tipo')
    uvas = request.GET.getlist('uva')
    paises = request.GET.getlist('pais')

    query = {}

    if tipos:
        query['tipo_do_vinho'] = {"$in": tipos}
    if uvas:
        query['tipo_da_uva'] = {"$in": uvas}
    if paises:
        query['pais_origem'] = {"$in": paises}

    vinhos = list(vinhos_collection.find(query))

    for vinho in vinhos:
        vinho['id'] = str(vinho['_id'])

    return render(request, 'loja/catalogo.html', {
    'vinhos': vinhos,
    'filtros': {
        'tipo': tipos,
        'uva': uvas,
        'pais': paises
    }
})

def adicionar_ao_carrinho(request, vinho_id):
    if 'usuario_email' not in request.session:
        messages.error(request, "Você precisa estar logado para adicionar itens ao carrinho.")
        return redirect('index') 
    
    vinho = vinhos_collection.find_one({"_id": ObjectId(vinho_id)})
    if not vinho:
        messages.error(request, "Vinho não encontrado.")
        return redirect('catalogo')

    carrinho = request.session.get('carrinho', [])

    # Adiciona o vinho ao carrinho
    carrinho.append({
        "id": str(vinho['_id']),
        "nome": vinho.get("tipo_do_vinho", "Vinho"),
        "uva": vinho.get("tipo_da_uva", ""),
        "preco": vinho.get("preco", 0.0),
        "imagem": vinho.get("imagem_url", ""),
        "quantidade": 1 
    })

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return redirect('meu_carrinho')

def meu_carrinho(request):
    if 'usuario_email' not in request.session:
        messages.error(request, "Você precisa estar logado para acessar o carrinho.")
        return redirect('index')
    
    carrinho = request.session.get('carrinho', [])
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)

    return render(request, 'loja/meu_carrinho.html', {
        'carrinho': carrinho,
        'total': total
    })

def remover_do_carrinho(request, vinho_id):
    carrinho = request.session.get('carrinho', [])
    novo_carrinho = [item for item in carrinho if item['id'] != vinho_id]

    request.session['carrinho'] = novo_carrinho
    request.session.modified = True

    return redirect('meu_carrinho')

def efetuar_pagamento(request):
    if not request.session.get('usuario_email'):
        messages.error(request, "Você precisa estar logado para finalizar a compra.")
        return redirect('index')

    carrinho = request.session.get('carrinho', [])
    if not carrinho:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('meu_carrinho')

    total = sum(item['preco'] * item['quantidade'] for item in carrinho)

    historico_collection.insert_one({
        "usuario_email": request.session['usuario_email'],
        "data_compra": datetime.now(),
        "itens": carrinho,
        "total": total
    })

    # Limpa o carrinho
    request.session['carrinho'] = []
    request.session.modified = True

    messages.success(request, "Compra finalizada com sucesso!")
    return redirect('dashboard')

def historico(request):
    if not request.session.get('usuario_email'):
        messages.error(request, "Você precisa estar logado para ver o histórico.")
        return redirect('index')

    compras = list(historico_collection.find({
        "usuario_email": request.session['usuario_email']
    }).sort("data_compra", -1))

    return render(request, 'loja/historico.html', {'compras': compras})

