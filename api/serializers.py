from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product #the model
        fields = [
            'description',
            'name', 
            'price', 
            'stock'
            ]

    
    #Field-level validation
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    

class OrderItemSerializer(serializers.ModelSerializer):
    # fields
    # product = ProductSerializer()
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price', 
        max_digits=10, 
        decimal_places=2
        )
    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'quantity', 'item_subtotal']
        # item_subtotal comes from the OrderItem model


class OrderSerializer(serializers.ModelSerializer):
    
    #nested serializers
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    # the obj parameter is the Order instance 
    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = [
            'order_id', 
            'created_at', 
            'user', 
            'status', 
            'items',
            'total_price'
            ]
        
class ProductInfoSerializer(serializers.Serializer):
    #get all products, count of products, max price of product

    # nested serializers
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)