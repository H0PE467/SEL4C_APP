from django import forms
from .models import *



class managerForm(forms.ModelForm):
    
    class Meta:
        model = manager
        fields = '__all__'
        labels = {
            'name' : 'Nombre',
            'email' : 'Correo',
            'cellphone' : 'Celular',
            'password' : 'Contraseña',
            'password_confirmation' : 'Confirmar Contraseña',
            'is_superuser' : 'Es Super Administrador?',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password_confirmation': forms.PasswordInput(),
        }

    
    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        
        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, vuelva a ingresarlas.")
        
        return password_confirmation
    
