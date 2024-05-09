import json

import django.db.utils
from django.http import JsonResponse
from django.templatetags.static import static


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .models import Order
from .models import OrderDetails


@api_view(['GET'])
def banners_list_api(request):
    # FIXME move data to db?
    return Response([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ])


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@api_view(['POST'])
def register_order(request):
    try:
        raw_order = request.data
        if not(isinstance( raw_order.get('products'), list)):
            return Response({'error': 'products key not present or not a list'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif len(raw_order['products']) == 0:
            return Response({'error': 'products list is empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if raw_order.get('firstname') is None or len(raw_order['firstname']) == 0:
            return Response({'error': 'firstname key not present or empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if raw_order.get('lastname') is None or len(raw_order['lastname']) == 0:
            return Response({'error': 'lastname key not present or empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if raw_order.get('address') is None or len(raw_order['address']) == 0:
            return Response({'error': 'address key not present or empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if raw_order.get('phonenumber') is None or len(raw_order['phonenumber']) == 0:
            return Response({'error': 'phonenumber key not present or empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        order = Order.objects.create(
            user_firstname=raw_order['firstname'],
            user_lastname=raw_order['lastname'],
            phonenumber=raw_order['phonenumber'],
            address=raw_order['address'],
        )
        for raw_product in raw_order['products']:
            product = Product.objects.get(id=raw_product['product'])
            OrderDetails.objects.create(
                order=order,
                product=product,
                quantity=raw_product['quantity'],
            )
        return Response(raw_order)
    except django.db.utils.IntegrityError as e:
        print(e)
        return Response({'error': 'ValueError'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # TODO это лишь заглушка

