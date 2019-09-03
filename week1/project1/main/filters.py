from django_filters import rest_framework as filters
from main.models import *


class AdvertisementFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    description = filters.CharFilter(lookup_expr='contains')
    class Meta:
        model = Advertisement
        fields = ('name','description',)
class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    description = filters.CharFilter(lookup_expr='contains')
    class Meta:
        model = Advertisement
        fields = ('name','description',)