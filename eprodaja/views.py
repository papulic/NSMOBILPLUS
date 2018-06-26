# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import UserLoginForm, UserRegisterForm
from . models import Poruke





def index(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    return render(request, 'eprodaja/index.html', {'user': user})


mail_registracija = """
Poštovani {username},

Vaš nalog je kreiran, možete krenuti u sigurnu kupovinu.

NSMOBILPLUS, Jevrejska 19
21000 Novi Sad

"""


def login_user(request):
    loginForm = UserLoginForm(request.POST or None)
    registerForm = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if "logovanje_korisnika" in request.POST and loginForm.is_valid():
            registerForm = UserRegisterForm() # prevent auto populate
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, '{username}, dobrodošli!'.format(username=user.username))
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request, 'Vaš nalog je suspendovan')
                    # return render(request, 'eprodaja/login.html', {'error_message': 'Vaš nalog je suspendovan'})
            else:
                messages.error(request, 'Pogrešno korisničko ime ili lozinka')
                # return render(request, 'eprodaja/login.html', {'error_message': 'Pogrešno korisničko ime ili lozinka'})
        if "registrovanje_korisnika" in request.POST and registerForm.is_valid():
            error = False
            loginForm = UserLoginForm() # prevent auto populate
            username = request.POST['username']
            ime = request.POST['ime']
            prezime = request.POST['prezime']
            email = request.POST['email']
            password = request.POST['password']
            password_2 = request.POST['password_2']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Korisničko ime '{username}' je zauzeto, molim vas izaberite drugo".format(
                    username=username))
                error = True
            if User.objects.filter(email=email).exists():
                messages.error(request,
                               "Korisnik sa email adresom '{email}' postoji, molim vas unesite drugu email adresu".format(
                                   email=email))
                error = True
            if len(password) < 6:
                messages.error(request, 'Lozinka mora imati najmanje 6 karaktera')
                error = True
            if password != password_2:
                messages.error(request, 'Pogrešna lozinka')
                error = True
            if not error:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=ime,
                                                last_name=prezime
                                                )
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # email = EmailMessage('NSMOBILPLUS | Novi nalog', mail_registracija.format(username=user.username), to=[user.email])
                        # email.send()
                        messages.success(request, '{username}, vaš nalog je uspešno kreiran. Hvala!'.format(username=username))
                        return HttpResponseRedirect('/')
    return render(request, 'eprodaja/login.html', {
            'loginForm': loginForm,
            'registerForm': registerForm
        })


def logout_user(request):
    try:
        user = request.user
    except:
        user = "Korisnik"
    logout(request)
    messages.success(request, 'Doviđenja {username}, dođite nam opet!'.format(username=user.username))
    return HttpResponseRedirect(reverse('eprodaja:index'))


def kontakt(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        tema = request.POST['subject']
        poruka = request.POST['message']
        nova_poruka = Poruke()
        nova_poruka.user = user
        nova_poruka.tema = tema
        nova_poruka.poruka = poruka
        nova_poruka.save()
        messages.success(request, '{username}, hvala vam što ste nas kontaktirali!'.format(username=username))
        return HttpResponseRedirect(reverse('eprodaja:kontakt'))
    return render(request, 'eprodaja/contact-us.html', {'user': user})
