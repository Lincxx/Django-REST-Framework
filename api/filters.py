import django_filters
from rest_framework import filters
from api.models import Order, Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'gt',  'lt', 'range'],
            }

    # url will use a __ instead of a a _ 

class OrderFilter(django_filters.FilterSet):
    # overrode the default date filter to use the date field and not the datetime
    created_at = django_filters.DateFilter(field_name='created_at__date')  
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['exact', 'gt', 'lt'],
        }

class InStockFilterBackend(filters.BaseFilterBackend):
     def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
        #return queryset.exclude(stock__gt=0)

    
