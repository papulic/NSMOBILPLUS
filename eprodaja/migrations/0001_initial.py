# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 05:46
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artikal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opis', models.CharField(default='Ovaj artikal nema opis!', max_length=100)),
                ('opis_za_filter', models.CharField(max_length=100)),
                ('cena', models.FloatField()),
                ('slika', models.ImageField(default='default.jpg', upload_to=b'')),
                ('na_stanju', models.BooleanField(default=True)),
                ('na_akciji', models.BooleanField(default=False)),
                ('broj_pregleda', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-kategorija'],
                'verbose_name_plural': 'Artikli',
            },
        ),
        migrations.CreateModel(
            name='Brend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brend', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Brendovi',
            },
        ),
        migrations.CreateModel(
            name='Detalji_korisnika',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresa', models.CharField(max_length=50)),
                ('postanski_broj', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(code='Po\u0161tanski broj mora imati 5 cifara', message='Po\u0161tanski broj mora imati 5 cifara', regex='^.{5}$')])),
                ('grad', models.CharField(max_length=25)),
                ('kontakt_telefon', models.CharField(max_length=15)),
                ('korisnik', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Detalji korisnika',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ukupno', models.FloatField(default=0.0)),
                ('artikal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprodaja.Artikal')),
            ],
            options={
                'verbose_name_plural': 'Unosi u korpe',
            },
        ),
        migrations.CreateModel(
            name='Kategorija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategorija', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Kategorije',
            },
        ),
        migrations.CreateModel(
            name='Korpa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField(auto_now_add=True)),
                ('ukupno', models.FloatField(default=0.0)),
                ('ukupno_proizvoda_u_korpi', models.PositiveIntegerField(default=0)),
                ('potvrdjena', models.BooleanField(default=False)),
                ('otpremljena', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='korpe', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datum'],
                'verbose_name_plural': 'Korpe kupaca',
            },
        ),
        migrations.CreateModel(
            name='Podkategorija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podkategorija', models.CharField(max_length=30)),
                ('kategorija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='podkategorije', to='eprodaja.Kategorija')),
            ],
            options={
                'verbose_name_plural': 'Podkategorije',
            },
        ),
        migrations.CreateModel(
            name='Poruke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(blank=True, max_length=250, null=True)),
                ('poruka', models.TextField(blank=True, null=True)),
                ('datum', models.DateField(auto_now_add=True)),
                ('procitana', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poruke', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datum'],
                'verbose_name_plural': 'Poruke',
            },
        ),
        migrations.CreateModel(
            name='Pretraga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pretraga', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Pretrage',
            },
        ),
        migrations.CreateModel(
            name='Slika',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slika', models.ImageField(upload_to=b'')),
                ('artikal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dodatne_slike', to='eprodaja.Artikal')),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Tipovi',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='korpa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprodaja.Korpa'),
        ),
        migrations.AddField(
            model_name='artikal',
            name='brend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artikli', to='eprodaja.Brend'),
        ),
        migrations.AddField(
            model_name='artikal',
            name='kategorija',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artikli', to='eprodaja.Kategorija'),
        ),
        migrations.AddField(
            model_name='artikal',
            name='podkategorija',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artikli', to='eprodaja.Podkategorija'),
        ),
        migrations.AddField(
            model_name='artikal',
            name='tip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artikli', to='eprodaja.Tip'),
        ),
    ]
