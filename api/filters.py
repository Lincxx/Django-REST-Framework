import django_filters
from rest_framework import filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
            }

    # url will use a __ instead of a a _ 

class InStockFilterBackend(filters.BaseFilterBackend):
     def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
        #return queryset.exclude(stock__gt=0)

    
