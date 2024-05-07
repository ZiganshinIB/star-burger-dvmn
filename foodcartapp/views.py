import json

from django.http import JsonResponse
from django.templatetags.static import static


from .models import Product
from .models import Order
from .models import OrderDetails


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
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
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


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
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    try:
        raw_order = json.loads(request.body.decode())
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
        return JsonResponse(raw_order)
    except ValueError:
        return JsonResponse({'status': 'error'}, status=400)

    # TODO это лишь заглушка

