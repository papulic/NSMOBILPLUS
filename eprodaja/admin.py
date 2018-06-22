# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Artikal, Korpa, Detalji_korisnika




class ArtikalModelAdmin(admin.ModelAdmin):
    list_display = ["id", "kategorija", "marka", "model", "cena", "na_stanju", "na_akciji"]
    list_filter = ["kategorija", "marka", "cena"]
    list_editable = ["na_stanju", "na_akciji", "cena"]

# class KategorijaModelAdmin(admin.ModelAdmin):
#     list_display = ["kategorija"]
#     list_filter = ["kategorija"]
#
# class MarkaModelAdmin(admin.ModelAdmin):
#     list_display = ["marka"]
#     list_filter = ["marka"]

class KorpaModelAdmin(admin.ModelAdmin):
    list_display = ["user", "user_id", "ukupno", "potvrdjena", "otpremljena", "artikli_u_korpi"]
    list_filter = ["user__username", "potvrdjena", "otpremljena"]


class Detalji_korisnikaModelAdmin(admin.ModelAdmin):
    list_display = ["korisnik"]
    list_filter = ["korisnik__username"]


admin.site.register(Detalji_korisnika, Detalji_korisnikaModelAdmin)
admin.site.register(Artikal, ArtikalModelAdmin)
admin.site.register(Korpa, KorpaModelAdmin)
# admin.site.register(Kategorija, KategorijaModelAdmin)
# admin.site.register(Marka, MarkaModelAdmin)
