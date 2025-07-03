from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class CadastroForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['nome_completo', 'data_nascimento', 'cpf', 'email', 'password1', 'password2']
       
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if cpf:
            cpf = cpf.replace(".", "").replace("-", "")
            
            if not cpf.isdigit() or len(cpf) != 11:
                raise forms.ValidationError("Digite um CPF válido com 11 números.")
        
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  
        if commit:
            user.save()
        return user  