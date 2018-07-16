# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import RegexValidator


class Detalji_korisnika(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    adresa = models.CharField(max_length=50, blank=True)
    postanski_broj = models.CharField(max_length=5, validators=[RegexValidator(regex='^.{5}$', message='Poštanski broj mora imati 5 cifara', code='Poštanski broj mora imati 5 cifara')], blank=True)
    grad = models.CharField(max_length=25, blank=True)
    kontakt_telefon = models.CharField(max_length=15, blank=True)

    def __unicode__(self):
        return self.korisnik.username

    class Meta:
        verbose_name_plural = "Detalji korisnika"


class Brend(models.Model):
    brend = models.CharField(max_length=30)

    def __unicode__(self):
        return self.brend

    class Meta:
        verbose_name_plural = "Brendovi"

class Tip(models.Model):
    tip = models.CharField(max_length=30)

    def __unicode__(self):
        return self.tip

    class Meta:
        verbose_name_plural = "Tipovi"


class Kategorija(models.Model):
    kategorija = models.CharField(max_length=30)
    tipovi = models.BooleanField(default=False)
    brendovi = models.BooleanField(default=False)

    def __unicode__(self):
        return self.kategorija

    class Meta:
        verbose_name_plural = "Kategorije"


class Podkategorija(models.Model):
    kategorija = models.ForeignKey(Kategorija, on_delete=models.CASCADE, related_name="podkategorije")
    podkategorija = models.CharField(max_length=30)

    def __unicode__(self):
        return self.kategorija.kategorija + " - " + self.podkategorija

    class Meta:
        verbose_name_plural = "Podkategorije"


class Artikal(models.Model):
    kategorija = models.ForeignKey(Kategorija, on_delete=models.CASCADE, related_name='artikli')
    podkategorija = models.ForeignKey(Podkategorija, on_delete=models.CASCADE, null=True, blank=True, related_name='artikli')
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, null=True, blank=True, related_name='artikli')
    brend = models.ForeignKey(Brend, on_delete=models.CASCADE, null=True, blank=True, related_name='artikli')
    opis = models.CharField(max_length=100, default="Ovaj artikal nema opis!")
    opis_za_filter = models.CharField(max_length=100)
    cena = models.FloatField()
    slika = models.ImageField(default='default.jpg')
    na_stanju = models.BooleanField(default=True)
    na_akciji = models.BooleanField(default=False)
    broj_pregleda = models.IntegerField(default=0)

    def __unicode__(self):
        return "id: {id} - kat: {kategorija} - pod.kat: {podkategorija} - tip: {tip} - brend: {brend} - opis: {opis}".format(id=str(self.id), kategorija=self.kategorija, podkategorija=self.podkategorija, tip=self.tip, brend=self.brend, opis=self.opis)

    class Meta:
        verbose_name_plural = "Artikli"
        ordering = ['-kategorija', ]


class Slika(models.Model):
    artikal = models.ForeignKey(Artikal, related_name='dodatne_slike')
    slika = models.ImageField()


class Korpa(models.Model):
    user = models.ForeignKey(User, related_name='korpe')
    datum = models.DateField(auto_now_add=True)
    ukupno = models.FloatField(default=0.0)
    ukupno_proizvoda_u_korpi = models.PositiveIntegerField(default=0)
    potvrdjena = models.BooleanField(default=False)
    otpremljena = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username + " - id: " + str(self.user.id)

    def ime(self):
        return self.user.first_name + " " + self.user.last_name

    def mail(self):
        return self.user.email

    def tel(self):
        return self.user.detalji_korisnika.kontakt_telefon

    def adresa(self):
        return self.user.detalji_korisnika.adresa + "\n" + self.user.detalji_korisnika.postanski_broj + "\n" + self.user.detalji_korisnika.grad

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


class Pretraga(models.Model):
    pretraga = models.CharField(max_length=50)

    def __unicode__(self):
        return self.pretraga

    class Meta:
        verbose_name_plural = "Pretrage"
