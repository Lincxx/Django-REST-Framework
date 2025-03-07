import django_filters

from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
            }

    # url will use a __ instead of a a _ 
    
