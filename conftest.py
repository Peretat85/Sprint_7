import pytest
import time
from api_client import ApiClient
from helpers import (generate_random_string, generate_random_phone_number,
                     generate_random_rent_time, generate_random_date,
                     generate_random_metro_station)

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"  #

@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания клиента API."""
    return ApiClient(BASE_URL)

@pytest.fixture()
def courier_data(api_client):
    """Фикстура для создания тестовых данных курьера."""
    courier_data = api_client.register_new_courier()
    return courier_data


@pytest.fixture()
def delete_courier(api_client, courier_data):
    """Фикстура для удаления курьера после теста."""
    yield
    api_client.delete_courier(courier_data["login"]) #Удаляем курьера после теста


@pytest.fixture()
def random_courier_data_without_field(request):
    """Фикстура для создания случайных данных курьера с пропущенным полем."""
    missing_field = request.param  # Получаем параметр из параметризованного теста
    data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    del data[missing_field]
    return data

@pytest.fixture()
def order_data():
    """Фикстура для создания тестовых данных заказа со случайными значениями."""

    return {
        "firstName": generate_random_string(10),
        "lastName": generate_random_string(10),
        "address": generate_random_string(20),
        "metroStation": generate_random_metro_station(),
        "phone": generate_random_phone_number(), #Случайный номер телефона
        "rentTime": generate_random_rent_time(),  # Случайное количество дней аренды (от 1 до 7)
        "deliveryDate": generate_random_date(), #Пример даты
        "comment": generate_random_string(30),
        "color": "" 
    }


