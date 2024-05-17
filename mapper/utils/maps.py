import requests
from star_burger.settings import YANDEX_API_KEY
from ..models import Address


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
