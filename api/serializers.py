from django.db import transaction
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

class OrderCreateSerializer(serializers.ModelSerializer):
    #nested serializers
    class OrderItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ['product', 'quantity']

    #nested serializers
    items = OrderItemSerializer(many=True, required=False)
    order_id = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        ordered_data = validated_data.pop('items')

        # atomic transaction, just in case something fails
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if ordered_data is not None:
                # clear the existing order items
                instance.items.all().delete()
                # create new order items
                for item_data in ordered_data:
                    OrderItem.objects.create(order=instance, **item_data)

        return instance

    def create(self, validated_data):
        ordered_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item_data in ordered_data:
                OrderItem.objects.create(order=order, **item_data)

        return order

    # the obj parameter is the Order instance 
    def get_total_price(self, obj):
        order_items = obj.items.all()
    class Meta:
        model = Order
        fields = [ 
            'order_id',
            'user', 
            'status', 
            'items',
            ]
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)

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