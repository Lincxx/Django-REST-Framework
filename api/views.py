from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductSerializer
from api.models import Order, OrderItem, Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

# function based views
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    # many=True for multiple objects
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
    

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
   

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
   