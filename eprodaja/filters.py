from .models import Artikal
import django_filters

class ArtikalFilter(django_filters.FilterSet):
    class Meta:
        model = Artikal
        fields = ['marka', 'model', 'kategorija']