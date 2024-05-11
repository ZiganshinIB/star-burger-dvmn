from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count


from geopy import distance
from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from mapper.models import Address
import requests
from star_burger.settings import YANDEX_API_KEY


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = []
    for order_instance in Order.objects.all():
        try:
            order_products = order_instance.products.values_list('product', flat=True)
            restaurants_preparing_all_dishes = (RestaurantMenuItem.objects.select_related('restaurant')
                                                .values('restaurant__name', 'restaurant__address')
                                                .filter(product__in=order_products)
                                                .annotate(restaurants_count=Count('restaurant_id'))
                                                .filter(restaurants_count=len(order_products)))

            for restaurant in restaurants_preparing_all_dishes:
                coordinates_restaurants = fetch_coordinates(restaurant['restaurant__address'])
                coordinates_order = fetch_coordinates(order_instance.address)
                restaurant["distances"] = round(distance.distance(coordinates_restaurants, coordinates_order).km, 3)
            order_items.append((order_instance, sorted(restaurants_preparing_all_dishes, key=lambda x: x["distances"])))
        except ValueError as e:
            print(e)
            order_items.append((order_instance, None))
    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
        # TODO заглушка для нереализованного функционала
    })


def fetch_coordinates(address):
    db_address = Address.objects.filter(address=address).first()
    if not db_address:
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": YANDEX_API_KEY,
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            raise ValueError({f"{address}": "No place found"},)

        most_relevant = found_places[0]
        lng, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        Address.objects.create(address=address, lat=lat, lng=lng)
        return lat, lng
    return db_address.lat, db_address.lng
