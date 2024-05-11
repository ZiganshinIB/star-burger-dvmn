import django.db.utils
from django.templatetags.static import static


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


from .models import Product
from .models import Order
from .models import OrderDetails
from .serializers import OrderSerializer

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
        order = OrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        order.save()
        return Response(order.data, status=status.HTTP_201_CREATED)
    except django.db.utils.IntegrityError as e:
        return Response({'error': 'ValueError'}, status=status.HTTP_406_NOT_ACCEPTABLE)


