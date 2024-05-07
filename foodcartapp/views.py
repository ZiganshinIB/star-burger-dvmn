import json

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
    except ValueError:
        print('error')
        return Response({'error': 'ValueError'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # TODO это лишь заглушка

