# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission, User





# class Kategorija(models.Model):
#     kategorija = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.kategorija
#
#     class Meta:
#         verbose_name_plural = "Kategorije"


Marke = (
    ('samsung', 'SAMSUNG'),
    ('huawei', 'HUAWEI'),
    ('sony', 'SONY'),
    ('motorola', 'MOTOROLA'),
    ('asus', 'ASUS'),
)

Kategorije = (
    ('maska', 'MASKA'),
    ('folija', 'FOLIJA'),
    ('staklo 2d', 'STAKLO 2D')
)

class Artikal(models.Model):
    model = models.CharField(max_length=100, blank=True)
    marka = models.CharField(max_length=10, choices=Marke)
    kategorija = models.CharField(max_length=10, choices=Kategorije)
    cena = models.FloatField(max_length=10)

    def __str__(self):
        return self.kategorija + " - " + self.marka + " - " + self.model

    class Meta:
        verbose_name_plural = "Artikli"


class Korpa(models.Model):
    user = models.ForeignKey(User, default=1)
    grad = models.CharField(max_length=25)
    postanski_broj = models.IntegerField()
    adresa = models.CharField(max_length=50)
    kontakt_telefon = models.IntegerField()
    artikli = models.ManyToManyField(Artikal)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Korpe kupaca"