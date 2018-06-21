# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Artikal


class ArtikalModelAdmin(admin.ModelAdmin):
    list_display = ["model"]
    list_filter = ["model"]

# class KategorijaModelAdmin(admin.ModelAdmin):
#     list_display = ["kategorija"]
#     list_filter = ["kategorija"]
#
# class MarkaModelAdmin(admin.ModelAdmin):
#     list_display = ["marka"]
#     list_filter = ["marka"]



admin.site.register(Artikal, ArtikalModelAdmin)
# admin.site.register(Kategorija, KategorijaModelAdmin)
# admin.site.register(Marka, MarkaModelAdmin)
