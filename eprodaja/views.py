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
from . models import Poruke, Detalji_korisnika, Korpa, Artikal, Kategorija, Podkategorija, Brend, Entry, Tip, Slika, Pretraga
from django.http import JsonResponse
# import random
import datetime


def index(request):
    user = None
    artikli = Artikal.objects.filter(na_stanju=True).order_by('kategorija')
    artikli_na_akciji = Artikal.objects.filter(na_akciji=True)
    artikli_na_akciji_ids = artikli_na_akciji.values_list("id", flat=True)
    sve_kategorije = Kategorija.objects.all()
    tipovi = Tip.objects.all()
    brendovi = Brend.objects.all()
    # try:
    #     random_artikli = [artikli[i] for i in random.sample(range(1, len(artikli)), 15)]
    # except ValueError:
    #     random_artikli = [artikli[i] for i in random.sample(range(1, len(artikli)), len(artikli) - 1)]
    random_artikli = Artikal.objects.filter(na_stanju=True).exclude(pk__in=list(artikli_na_akciji_ids)).order_by('-broj_pregleda')[:15]

    if request.user.is_authenticated():
        user = request.user

    proizvoda_u_korpi = 0
    try:
        korpa = user.korpe.get(potvrdjena=False)
        proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
    except:
        pass

    return render(request, 'eprodaja/index.html', {
            'user': user,
            'artikli_na_akciji': artikli_na_akciji,
            'proizvoda_u_korpi': proizvoda_u_korpi,
            'sve_kategorije': sve_kategorije,
            'tipovi': tipovi,
            'brendovi': brendovi,
            'random_artikli': random_artikli
        })


def add_artikal(request):
    user = request.user
    if user.username != "":
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
    else:
        messages.add_message(request, messages.INFO, 'Morate biti ulogovani!')
        data = {'error': True}
    return JsonResponse(data)
    # return HttpResponse(
    #     json.dumps(response_data),
    #     content_type="application/json")


def filter(request):
    artikli = None
    artikli_za_filter = request.GET.get('artikli_za_filter', None)
    artikli_za_filter = artikli_za_filter.split("_")
    kategorija_id = artikli_za_filter[0].split("kategorija")[1]
    artikli = Artikal.objects.filter(kategorija_id=kategorija_id)
    if len(artikli_za_filter) > 1:
        for i in artikli_za_filter:
            if 'podkategorija' in i:
                podkategorija_id = i.split("podkategorija")[1]
                artikli = artikli.filter(podkategorija_id=podkategorija_id)
            elif 'tip' in i:
                tip_id = i.split("tip")[1]
                artikli = artikli.filter(tip_id=tip_id)
            elif 'brend' in i:
                brend_id = i.split("brend")[1]
                artikli = artikli.filter(brend_id=brend_id)
    if artikli:
        data = list(artikli.values())
    else:
        data = {}
    return JsonResponse(data, safe=False)


def pretraga(request):
    pretraga = request.GET.get('pretraga', None)
    splited = pretraga.split()
    if len(pretraga) > 5:
        if Pretraga.objects.filter(pretraga=pretraga).exists():
            pass
        else:
            if Pretraga.objects.all().count() > 500:
                pretrage = Pretraga.objects.all()[200:].values_list("id", flat=True)
                Pretraga.objects.exclude(pk__in=list(pretrage)).delete()
            nova_pretraga = Pretraga()
            nova_pretraga.pretraga = pretraga
            nova_pretraga.save()
    if len(splited) > 0:
        artikli = Artikal.objects.filter(opis_za_filter__icontains=splited[0])
        if len(splited) > 1:
            for pos, i in enumerate(splited):
                if pos > 0:
                    artikli = artikli.filter(opis_za_filter__icontains=i)
    if artikli:
        data = list(artikli.values())
    else:
        data = {}
    return JsonResponse(data, safe=False)

def create_modal(request):
    artikal_id = request.GET.get('artikal_id', None)
    art = Artikal.objects.get(pk=artikal_id)
    art.broj_pregleda += 1
    art.save()
    artikal = Artikal.objects.filter(pk=artikal_id)
    slike = Slika.objects.filter(artikal_id=artikal_id)
    data = [[], []]
    data[0] = list(artikal.values())
    data[1] = list(slike.values())
    return JsonResponse(data, safe=False)


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
                    messages.warning(request, '{username}, dobrodošli!'.format(username=user.username))
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
    messages.warning(request, 'Doviđenja {username}, dođite nam opet!'.format(username=user.username))
    return HttpResponseRedirect(reverse('eprodaja:index'))


def kontakt(request):
    user = None
    proizvoda_u_korpi = 0
    if request.user.is_authenticated():
        user = request.user
        try:
            korpa = user.korpe.get(potvrdjena=False)
            proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
        except:
            pass
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
        messages.warning(request, '{username}, hvala vam što ste nas kontaktirali!'.format(username=username))
        return HttpResponseRedirect(reverse('eprodaja:kontakt'))
    return render(request, 'eprodaja/contact-us.html', {'user': user, 'proizvoda_u_korpi': proizvoda_u_korpi})


def nalog(request, user_id):
    user = User.objects.get(pk=user_id)
    detalji_korisnika = Detalji_korisnika.objects.get(korisnik=user)
    korpe = Korpa.objects.filter(user=user, potvrdjena=True).order_by('-datum')
    proizvoda_u_korpi = 0
    try:
        korpa = user.korpe.get(potvrdjena=False)
        proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
    except:
        pass
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
    return render(request, 'eprodaja/account.html', {'user': user, 'korpe': korpe, 'proizvoda_u_korpi': proizvoda_u_korpi})


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
        if 'brisi_unos' in request.POST:
            unos_id = request.POST['brisi_unos']
            unos = Entry.objects.get(pk=unos_id)
            unos.delete()
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


def potvrdi_korpu(request, korpa_id):
    korpa = Korpa.objects.get(pk=korpa_id)
    error = False
    if korpa.user.detalji_korisnika.adresa == "":
        messages.error(request, 'Molim vas unesite ispravne podatke "Ulica i broj".')
        error = True
    elif korpa.user.detalji_korisnika.postanski_broj == "":
        messages.error(request, 'Molim vas unesite ispravne podatke "Poštanski broj".')
        error = True
    elif korpa.user.detalji_korisnika.grad == "":
        messages.error(request, 'Molim vas unesite ispravne podatke "Grad".')
        error = True
    elif korpa.user.detalji_korisnika.kontakt_telefon == "":
        messages.error(request, 'Molim vas unesite ispravne podatke "Kontakt telefon".')
        error = True
    if error:
        return HttpResponseRedirect('/nalog/{user_id}#adresa'.format(user_id=korpa.user.id))
    korpa.potvrdjena = True
    korpa.datum = datetime.date.today()
    korpa.save()
    messages.success(request, 'Hvala na kupovini! Detalje o vašim porudžbinama možete videti u sekciji Moj nalog.')
    return HttpResponseRedirect("/")


# treba ako nema jquery
# def artikal_detalji(request, artikal_id):
#     artikal = Artikal.objects.get(pk=artikal_id)
#     artikal.broj_pregleda += 1
#     artikal.save()
#     ostale_slike = Slika.objects.filter(artikal=artikal)
#     proizvoda_u_korpi = 0
#     user = request.user
#     try:
#         korpa = user.korpe.get(potvrdjena=False)
#         proizvoda_u_korpi = korpa.ukupno_proizvoda_u_korpi
#     except:
#         pass
#     return render(request, 'eprodaja/product-details.html', {'artikal': artikal, 'ostale_slike': ostale_slike, 'proizvoda_u_korpi': proizvoda_u_korpi})

def error_404(request):
    return render(request, 'eprodaja/404.html')
