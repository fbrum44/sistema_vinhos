from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):  
        if not email:
            raise ValueError('O e-mail deve ser informado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['nome_completo', 'cpf', 'data_nascimento']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = self.cpf
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo
    
