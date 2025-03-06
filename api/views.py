from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductSerializer, ProductInfoSerializer
from api.models import Order, OrderItem, Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_url_kwarg = 'product_id'
    
class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
