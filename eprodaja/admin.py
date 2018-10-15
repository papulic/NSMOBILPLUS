# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Artikal, Korpa, Detalji_korisnika, Poruke, Podkategorija, Kategorija, Brend, Tip, Slika, Entry, Pretraga
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User


class ArtikalSlikaInline(admin.TabularInline):
    model = Slika
    extra = 3

class KorisnikKorpaInline(admin.TabularInline):
    model = Korpa
    extra = 0


class EntryKorpaInline(admin.TabularInline):
    model = Entry
    extra = 0
    readonly_fields = ('artikal', 'quantity', 'ukupno')

class PodkategorijaInline(admin.TabularInline):
    model = Podkategorija
    extra = 0

class DetaljiKorisnikInline(admin.StackedInline):
    model = Detalji_korisnika

class UserAdmin(AuthUserAdmin):
 inlines = [DetaljiKorisnikInline, KorisnikKorpaInline]


class ArtikalModelAdmin(admin.ModelAdmin):
    list_display = ["kategorija", "podkategorija", "tip", "brend", "nasa_sifra", "opis", "opis_za_filter", "cena", "na_stanju", "na_akciji"]
    list_filter = ["kategorija__kategorija", "na_stanju", "na_akciji"]
    list_editable = ["na_stanju", "na_akciji", "cena"]
    inlines = [ArtikalSlikaInline, ]

class KategorijaModelAdmin(admin.ModelAdmin):
    list_display = ["kategorija"]
    inlines = [PodkategorijaInline]

class PodkategorijaModelAdmin(admin.ModelAdmin):
    list_display = ["podkategorija", "kategorija"]
    list_filter = ["kategorija__kategorija"]

class BrendModelAdmin(admin.ModelAdmin):
    list_display = ["brend"]

class TipModelAdmin(admin.ModelAdmin):
    list_display = ["tip"]

class KorpaModelAdmin(admin.ModelAdmin):
    list_display = ["user", "user_id", "ukupno", "potvrdjena", "otpremljena", "datum"]
    list_filter = ["user__username", "potvrdjena", "otpremljena"]
    list_editable = ["otpremljena"]
    inlines = [EntryKorpaInline, ]
    readonly_fields = ['potvrdjena', 'datum', 'user', 'ukupno', 'ukupno_proizvoda_u_korpi', 'ime', 'mail', 'adresa', 'tel']


class Detalji_korisnikaModelAdmin(admin.ModelAdmin):
    list_display = ["korisnik"]
    list_filter = ["korisnik__username"]


class PorukeModelAdmin(admin.ModelAdmin):
    list_display = ["user", "procitana"]
    list_filter = ["user__username", "datum"]
    list_editable = ["procitana"]


class PretragaModelAdmin(admin.ModelAdmin):
    list_display = ["pretraga", "id"]



admin.site.register(Detalji_korisnika, Detalji_korisnikaModelAdmin)
admin.site.register(Artikal, ArtikalModelAdmin)
admin.site.register(Korpa, KorpaModelAdmin)
admin.site.register(Poruke, PorukeModelAdmin)
admin.site.register(Kategorija, KategorijaModelAdmin)
admin.site.register(Podkategorija, PodkategorijaModelAdmin)
admin.site.register(Brend, BrendModelAdmin)
admin.site.register(Tip, TipModelAdmin)
admin.site.register(Pretraga, PretragaModelAdmin)
# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
