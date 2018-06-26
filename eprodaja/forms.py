from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Adresa ili korisnicko ime', 'title': ' '}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Lozinka', 'title': ' '}), label='')

class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Korisnicko ime', 'title': ' '}), label='')
    ime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ime', 'title': ' '}), label='')
    prezime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Prezime', 'title': ' '}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email Adresa', 'title': ' '}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Lozinka', 'title': ' '}), label='')
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ponovite lozinku', 'title': ' '}), label='')