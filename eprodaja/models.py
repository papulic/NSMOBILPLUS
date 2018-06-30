# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import RegexValidator


class Detalji_korisnika(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    adresa = models.CharField(max_length=50)
    postanski_broj = models.CharField(max_length=5, validators=[RegexValidator(regex='^.{5}$', message='Poštanski broj mora imati 5 cifara', code='Poštanski broj mora imati 5 cifara')])
    grad = models.CharField(max_length=25)
    kontakt_telefon = models.CharField(max_length=15)

    def __unicode__(self):
        return self.korisnik.username

    class Meta:
        verbose_name_plural = "Detalji korisnika"


class Marka(models.Model):
    marka = models.CharField(max_length=30)

    def __unicode__(self):
        return self.marka

    class Meta:
        verbose_name_plural = "Marke"


class Kategorija(models.Model):
    kategorija = models.CharField(max_length=30)

    def __unicode__(self):
        return self.kategorija

    class Meta:
        verbose_name_plural = "Kategorije"


class Model(models.Model):
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    model = models.CharField(max_length=30)

    def __unicode__(self):
        return self.marka.marka + " - " + self.model

    class Meta:
        verbose_name_plural = "Modeli"


class Artikal(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    opis = models.CharField(max_length=100, default="Ovaj artikal nema opis!")
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    kategorija = models.ForeignKey(Kategorija, on_delete=models.CASCADE)
    slika = models.ImageField(null=True, blank=True)
    cena = models.FloatField()
    na_stanju = models.BooleanField(default=True)
    na_akciji = models.BooleanField(default=False)

    def __unicode__(self):
        return self.kategorija.kategorija + " - " + self.marka.marka + " - " + self.model.model

    class Meta:
        verbose_name_plural = "Artikli"
        ordering = ['-kategorija', ]


class Korpa(models.Model):
    user = models.ForeignKey(User, related_name='korpe')
    datum = models.DateField(auto_now_add=True)
    ukupno = models.FloatField(default=0.0)
    ukupno_proizvoda_u_korpi = models.PositiveIntegerField(default=0)
    potvrdjena = models.BooleanField(default=False)
    otpremljena = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username + " - id: " + str(self.user.id)


    class Meta:
        verbose_name_plural = "Korpe kupaca"
        ordering = ['-datum', ]


class Entry(models.Model):
    artikal = models.ForeignKey(Artikal, on_delete=models.CASCADE)
    korpa = models.ForeignKey(Korpa, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ukupno = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.artikal.opis + str(self.quantity)


    class Meta:
        verbose_name_plural = "Unosi u korpe"


class Poruke(models.Model):
    user = models.ForeignKey(User, related_name='poruke')
    tema = models.CharField(max_length=250, null=True, blank=True)
    poruka = models.TextField(null=True, blank=True)
    datum = models.DateField(auto_now_add=True)
    procitana = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Poruke"
        ordering = ['-datum', ]

