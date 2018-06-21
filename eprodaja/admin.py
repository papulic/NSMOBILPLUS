# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Artikal, Korpa


class ArtikalModelAdmin(admin.ModelAdmin):
    list_display = ["kategorija", "marka", "model", "cena"]
    list_filter = ["kategorija", "marka"]

# class KategorijaModelAdmin(admin.ModelAdmin):
#     list_display = ["kategorija"]
#     list_filter = ["kategorija"]
#
# class MarkaModelAdmin(admin.ModelAdmin):
#     list_display = ["marka"]
#     list_filter = ["marka"]

class KorpaModelAdmin(admin.ModelAdmin):
    list_display = ["user", "adresa"]
    list_filter = ["user"]


admin.site.register(Artikal, ArtikalModelAdmin)
admin.site.register(Korpa, KorpaModelAdmin)
# admin.site.register(Kategorija, KategorijaModelAdmin)
# admin.site.register(Marka, MarkaModelAdmin)
