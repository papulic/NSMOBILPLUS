# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import RegexValidator





# class Kategorija(models.Model):
#     kategorija = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.kategorija
#
#     class Meta:
#         verbose_name_plural = "Kategorije"

class Detalji_korisnika(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    adresa = models.CharField(max_length=50)
    postanski_broj = models.IntegerField(validators=[RegexValidator(regex='^.{5}$', message='Poštanski broj mora imati 5 cifara', code='Poštanski broj mora imati 5 cifara')])
    grad = models.CharField(max_length=25)
    kontakt_telefon = models.CharField(max_length=15)

    def __str__(self):
        return self.korisnik.username

    class Meta:
        verbose_name_plural = "Detalji korisnika"


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
    model = models.CharField(max_length=100)
    marka = models.CharField(max_length=10, choices=Marke)
    kategorija = models.CharField(max_length=10, choices=Kategorije)
    slika = models.ImageField(null=True, blank=True)
    cena = models.DecimalField(decimal_places=2, max_digits=10)
    na_stanju = models.BooleanField(default=True)
    na_akciji = models.BooleanField(default=False)

    def __str__(self):
        return self.kategorija + " - " + self.marka + " - " + self.model

    class Meta:
        verbose_name_plural = "Artikli"


class Korpa(models.Model):
    user = models.ForeignKey(User, related_name='korpe')
    datum = models.DateField(auto_now_add=True)
    artikli = models.ManyToManyField(Artikal, related_name='korpe', blank=True)
    ukupno = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    potvrdjena = models.BooleanField(default=False)
    otpremljena = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " - id: " + str(self.user.id)

    def artikli_u_korpi(self):
        return ", ".join([str(artikal.id) for artikal in self.artikli.all()])


    class Meta:
        verbose_name_plural = "Korpe kupaca"


class Poruke(models.Model):
    user = models.ForeignKey(User, related_name='poruke')
    tema = models.CharField(max_length=250, null=True, blank=True)
    poruka = models.TextField(null=True, blank=True)
    datum = models.DateField(auto_now_add=True)
    procitana = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Poruke"

