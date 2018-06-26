from django.conf.urls import url
from . import views


app_name = 'eprodaja'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logovanje/$', views.login_user, name='login_user'),
    url(r'^korisnik_izlogovan/$', views.logout_user, name='logout_user'),
    url(r'^kontakt/$', views.kontakt, name='kontakt'),
]
