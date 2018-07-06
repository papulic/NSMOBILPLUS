from django import forms
from django.contrib.auth.models import User



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Adresa ili korisnicko ime', 'title': ' ', 'id': 'username_login'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Lozinka', 'title': ' ', 'id': 'password_login', 'autocomplete': 'off'}), label='')

class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Korisnicko ime', 'title': ' '}), label='')
    ime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ime', 'title': ' '}), label='')
    prezime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Prezime', 'title': ' '}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email Adresa', 'title': ' '}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Lozinka', 'title': ' ', 'autocomplete': 'off'}), label='')
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ponovite lozinku', 'title': ' ', 'autocomplete': 'off'}), label='')

class DetaljiForm(forms.Form):
    adresa = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ulica i broj', 'title': ' '}), label='', required=False)
    postanski_broj = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Postanski broj', 'title': ' ', 'pattern': '[0-9]{5}'}), label='', required=False)
    grad = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Grad', 'title': ' '}), label='', required=False)
    kontakt_telefon = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kontakt telefon', 'title': ' '}), label='', required=False)
