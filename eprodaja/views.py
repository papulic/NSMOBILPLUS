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
from .forms import UserLoginForm, UserRegisterForm, DetaljiForm
from . models import Poruke, Detalji_korisnika, Korpa, Artikal, Kategorija, Marka, Model, Entry
from .filters import ArtikalFilter
from django.http import JsonResponse
import json


def index(request):
    user = None
    artikli = Artikal.objects.filter(na_stanju=True).order_by('kategorija').order_by('marka')
    artikli_na_akciji = Artikal.objects.filter(na_akciji=True)
    artikli_filter = ArtikalFilter(request.GET, queryset=artikli)
    if request.method == 'GET':
        if 'marka' in request.GET:
            izabrana_marka_id = request.GET['marka']
            if izabrana_marka_id != "":
                marka = Marka.objects.get(pk=izabrana_marka_id)
            else:
                marka = 'SVE MARKE'
        else:
            marka = 'SVE MARKE'
        if 'kategorija' in request.GET:
            izabrana_kategorija_id = request.GET['kategorija']
            if izabrana_kategorija_id != "":
                kategorija = Kategorija.objects.get(pk=izabrana_kategorija_id)
            else:
                kategorija = 'SVI PROIZVODI'
        else:
            kategorija = 'SVI PROIZVODI'
        if 'model' in request.GET:
            izabrani_model_id = request.GET['model']
            if izabrani_model_id != "":
                model = Model.objects.get(pk=izabrani_model_id)
                model = model.model
            else:
                model = 'SVI MODELI'
        else:
            model = 'SVI MODELI'
    else:
        marka = 'SVE MARKE'
        kategorija = 'SVI PROIZVODI'
        model = 'SVI MODELI'

    if request.user.is_authenticated():
        user = request.user

    else:
        if request.method == 'POST':
            if 'artikal' in request.POST:
                messages.success(request, 'Morate biti ulogovani!')
                return HttpResponseRedirect('/logovanje')
    proizvoda_u_korpi = 0
    try:
        korpa = user.korpe.get(potvrdjena=False)
        proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
    except:
        pass
    return render(request, 'eprodaja/index.html', {
            'user': user,
            'artikli': artikli,
            'artikli_filter': artikli_filter,
            'marka': marka,
            'kategorija': kategorija,
            'model': model,
            'artikli_na_akciji': artikli_na_akciji,
            'proizvoda_u_korpi': proizvoda_u_korpi
        })


def add_artikal(request):
    user = request.user

    artikal_id = request.GET.get('artikal_id', None)
    artikal = Artikal.objects.get(pk=artikal_id)
    try:
        korpa = user.korpe.get(potvrdjena=False)
    except Korpa.MultipleObjectsReturned:
        korpa = user.korpe.filter(potvrdjena=False)[0]  # ne sme da se desi
    except Korpa.DoesNotExist:
        korpa = Korpa()
        korpa.user = user
        korpa.save()
    unos = Entry(korpa=korpa, artikal=artikal)
    unos.ukupno = artikal.cena
    unos.save()
    korpa.ukupno += artikal.cena
    korpa.ukupno_proizvoda_u_korpi += 1
    korpa.save()
    data = {'proizvoda_u_korpi': korpa.ukupno_proizvoda_u_korpi}
    return JsonResponse(data)
    # return HttpResponse(
    #     json.dumps(response_data),
    #     content_type="application/json")


mail_registracija = """
Poštovani {username},

Vaš nalog na sajtu www.nsmobilplus.com je kreiran,
možete krenuti u sigurnu kupovinu.


Srdačno,

vaš NSMOBILPLUS

Jevrejska 19, 21000 Novi Sad
"""


def login_user(request):
    loginForm = UserLoginForm(request.POST or None)
    registerForm = UserRegisterForm(request.POST or None)
    detaljiForm = DetaljiForm(request.POST or None)
    if request.method == "POST":
        if "logovanje_korisnika" in request.POST and loginForm.is_valid():
            registerForm = UserRegisterForm() # prevent auto populate
            detaljiForm = DetaljiForm()
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
            adresa = request.POST['adresa']
            postanski_broj = request.POST['postanski_broj']
            grad = request.POST['grad']
            kontakt_telefon = request.POST['kontakt_telefon']
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
                detalji = Detalji_korisnika()
                detalji.korisnik = user
                detalji.adresa = adresa
                detalji.postanski_broj = postanski_broj
                detalji.grad = grad
                detalji.kontakt_telefon = kontakt_telefon
                detalji.save()
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
            'registerForm': registerForm,
            'detaljiForm': detaljiForm
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


def nalog(request, user_id):
    user = User.objects.get(pk=user_id)
    detalji_korisnika = Detalji_korisnika.objects.get(korisnik=user)
    korpe = Korpa.objects.filter(user=user, potvrdjena=True).order_by('datum')
    if request.method == "POST":
        adresa = request.POST['adresa']
        postanski_broj = request.POST['postanski_broj']
        grad = request.POST['grad']
        kontakt_telefon = request.POST['kontakt_telefon']
        detalji_korisnika.adresa = adresa
        detalji_korisnika.postanski_broj = postanski_broj
        detalji_korisnika.grad = grad
        detalji_korisnika.kontakt_telefon = kontakt_telefon
        detalji_korisnika.save()
        messages.success(request, 'Podaci su ažurirani!')
        return HttpResponseRedirect('/nalog/{user_id}'.format(user_id=user_id))
    return render(request, 'eprodaja/account.html', {'user': user, 'korpe': korpe})


def korpa(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        izmena_na_unosu = False
        if 'unos' in request.POST:
            unos_id = request.POST['unos']
            unos = Entry.objects.get(pk=unos_id)
            if 'quantity_up' in request.POST:
                unos.quantity += 1
                unos.ukupno += unos.artikal.cena
                unos.save()
                izmena_na_unosu = True
            elif 'quantity_down' in request.POST:
                if unos.quantity <= 1:
                    pass
                else:
                    unos.quantity -= 1
                    unos.ukupno -= unos.artikal.cena
                    unos.save()
                    izmena_na_unosu = True
        if izmena_na_unosu:
            korpa = Korpa.objects.get(user=user, potvrdjena=False)
            unosi = korpa.entry_set.all()
            proizvoda_u_korpi = 0
            korpa_ukupno = 0
            x_exp = (x for x in unosi)
            for i in x_exp:
                proizvoda_u_korpi += i.quantity
                korpa_ukupno += i.ukupno
            korpa.ukupno_proizvoda_u_korpi = proizvoda_u_korpi
            korpa.ukupno = korpa_ukupno
            korpa.save()
        return HttpResponseRedirect('/korpa/{user_id}'.format(user_id=user_id))
    try:
        korpa = Korpa.objects.get(user=user, potvrdjena=False)
        unosi = korpa.entry_set.all()
        proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
    except Korpa.DoesNotExist:
        korpa = None
        unosi = None
        proizvoda_u_korpi = 0

    return render(request, 'eprodaja/cart.html', {'user': user,
                                                  'korpa': korpa,
                                                  'unosi': unosi,
                                                  'proizvoda_u_korpi': proizvoda_u_korpi})


def korpa_detalji(request, korpa_id):
    korpa = Korpa.objects.get(pk=korpa_id)
    unosi = korpa.entry_set.all()
    return render(request, 'eprodaja/korpa_detalji.html', {'korpa': korpa, 'unosi': unosi})

