from django.conf.urls import url
from . import views


app_name = 'eprodaja'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]