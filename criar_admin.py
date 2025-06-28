import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_vinhos.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from loja.mongodb import usuarios_collection

admin = {
    "nome_completo": "Admin Master",
    "data_nascimento": "1990-01-01",
    "cpf": "00000000000",
    "email": "admin@admin",
    "senha": make_password("admin"),
    "is_admin": True
}

if not usuarios_collection.find_one({"email": admin['email']}):
    usuarios_collection.insert_one(admin)
    print("Admin criado com sucesso!")
else:
    print("Admin já existe.")