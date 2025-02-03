from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Dirección de correo electrónico'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), label='', required=False)
    second_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Segundo nombre'}), label='', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}), label='')
    second_last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno'}), label='', required=False)
    rut = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'RUT'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña'}), label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'second_name', 'last_name', 'second_last_name', 'rut', 'password1', 'password2']



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, help_text="El email no puede estar vacío.")
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ['username', 'email', 'password']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'imagen', 'precio', 'stock', 'categoria']