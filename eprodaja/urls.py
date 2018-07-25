from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


app_name = 'eprodaja'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logovanje/$', views.login_user, name='login_user'),
    url(r'^korisnik_izlogovan/$', views.logout_user, name='logout_user'),
    url(r'^kontakt/$', views.kontakt, name='kontakt'),
    url(r'^nalog/(?P<user_id>[0-9]+)/$', views.nalog, name='nalog'),
    url(r'^korpa/(?P<user_id>[0-9]+)/$', views.korpa, name='korpa'),
    url(r'^detalji_korpe/(?P<korpa_id>[0-9]+)/$', views.korpa_detalji, name='korpa_detalji'),
    url(r'^potvrdi_korpu/(?P<korpa_id>[0-9]+)/$', views.potvrdi_korpu, name='potvrdi_korpu'),
    url(r'^dodaj_artikal/$', views.add_artikal, name='add_artikal'),
    url(r'^filter/$', views.filter, name='filter'),
    url(r'^pretraga/$', views.pretraga, name='pretraga'),
    url(r'^onama/$', views.onama, name='onama'),
    url(r'^create_modal/$', views.create_modal, name='create_modal'),
    # url(r'^artikal/(?P<artikal_id>[0-9]+)/$', views.artikal_detalji, name='artikal_detalji'), # treba ako nema jquery
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
