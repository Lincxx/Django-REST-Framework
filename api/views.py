from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductSerializer, ProductInfoSerializer
from api.models import Order, OrderItem, Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import(
    IsAuthenticated, 
    IsAdminUser, 
    AllowAny)
from rest_framework.views import APIView


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()



class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# this is being handled in the ProductListCreateAPIView
# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer  

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs) 

class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


# this is good for collecting data or retruning that data
# refer to here - https://www.youtube.com/watch?v=TVFCU0w65Ak&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t&index=9
class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)


