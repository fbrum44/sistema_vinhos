from django.shortcuts import render

def index(request):
    return render(request, 'loja/index.html')

def sobre(request):
    return render(request, 'loja/sobre.html')


