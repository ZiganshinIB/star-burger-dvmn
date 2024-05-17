from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ValidationError

from .models import Order, OrderDetails





class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderDetailsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id','firstname', 'lastname', 'phonenumber', 'address', 'products', 'total_price']

    def create(self, validated_data):
        products = validated_data.pop('products')

        total_price = sum([product['product'].price * product['quantity'] for product in products])
        validated_data['total_price'] = total_price
        order = Order.objects.create(**validated_data)
        for product in products:
            OrderDetails.objects.create(order=order, **product)
        return order


