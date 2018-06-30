# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Artikal, Korpa, Detalji_korisnika, Poruke, Marka, Kategorija, Model




class ArtikalModelAdmin(admin.ModelAdmin):
    list_display = ["id", "kategorija", "marka", "model", "cena", "na_stanju", "na_akciji"]
    list_filter = ["kategorija__kategorija", "marka__marka", "na_stanju", "na_akciji"]
    list_editable = ["na_stanju", "na_akciji", "cena"]

class KategorijaModelAdmin(admin.ModelAdmin):
    list_display = ["kategorija"]
    list_filter = ["kategorija"]

class MarkaModelAdmin(admin.ModelAdmin):
    list_display = ["marka"]
    list_filter = ["marka"]

class ModelModelAdmin(admin.ModelAdmin):
    list_display = ["marka", "model"]
    list_filter = ["marka__marka"]

class KorpaModelAdmin(admin.ModelAdmin):
    list_display = ["user", "user_id", "ukupno", "potvrdjena", "otpremljena", "datum"]
    list_filter = ["user__username", "potvrdjena", "otpremljena"]


class Detalji_korisnikaModelAdmin(admin.ModelAdmin):
    list_display = ["korisnik"]
    list_filter = ["korisnik__username"]


class PorukeModelAdmin(admin.ModelAdmin):
    list_display = ["user", "procitana"]
    list_filter = ["user__username", "datum"]


admin.site.register(Detalji_korisnika, Detalji_korisnikaModelAdmin)
admin.site.register(Artikal, ArtikalModelAdmin)
admin.site.register(Korpa, KorpaModelAdmin)
admin.site.register(Poruke, PorukeModelAdmin)
admin.site.register(Kategorija, KategorijaModelAdmin)
admin.site.register(Marka, MarkaModelAdmin)
admin.site.register(Model, ModelModelAdmin)