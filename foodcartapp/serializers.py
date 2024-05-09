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
        fields = ['id','firstname', 'lastname', 'phonenumber', 'address', 'products']

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        products = self.validated_data.get('products')
        if not isinstance(products, list):
            self._errors['products'] = 'Поле продуктов должно быть списком'
            raise ValidationError(self._errors)
        if not products:
            self._errors['products'] = 'Поле продуктов не может быть пустым'
            raise ValidationError(self._errors)

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            OrderDetails.objects.create(order=order, **product)
        return order


