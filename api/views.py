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
from rest_framework import viewsets
from api.filters import InStockFilterBackend, ProductFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class ProductListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    # filterset_fields = ['name', 'price']
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter, 
        InStockFilterBackend,
        ]
    search_fields = ['name', 'description']
    # if we want an extact match on a field we need to use =
    # search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    # we override the default page size
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'page_num'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 6

    # offset is controlled by the settings, PAGE_SIZE
    pagination_class = LimitOffsetPagination



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

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    # we can override the default pagination class
    pagination_class = None



# class OrderListAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer

# class UserOrderListAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)


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


