import pytest
import time
from api_client import ApiClient
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"  # Замени на адрес твоего API

@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания клиента API."""
    return ApiClient(BASE_URL)

@pytest.fixture()
def courier_data(api_client):
    """Фикстура для создания тестовых данных курьера."""
    courier_data = api_client.register_new_courier()
    assert courier_data is not None, "Failed to register new courier" # Check registration success
    return courier_data

@pytest.fixture()
def create_courier(api_client, courier_data):
    """Фикстура для создания курьера."""
    yield courier_data  # Передаем данные курьера в тест

@pytest.fixture()
def delete_courier(api_client, courier_data):
    """Фикстура для удаления курьера после теста."""
    yield
    api_client.delete_courier(courier_data["login"]) #Удаляем курьера после теста

def generate_random_string(length):
    """Генерирует случайную строку заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

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
    metro_stations = ["Сокольники", "Комсомольская", "Красные ворота", "Чистые пруды", "Лубянка"] # станции
    colors = ["BLACK", "GREY", ""]

    return {
        "firstName": generate_random_string(10),
        "lastName": generate_random_string(10),
        "address": generate_random_string(20),
        "metroStation": random.choice(metro_stations),
        "phone": "+7" + ''.join(random.choice(string.digits) for i in range(10, 12)), #Случайный номер телефона
        "rentTime": random.randint(1, 7),  # Случайное количество дней аренды (от 1 до 7)
        "deliveryDate": "2025-01-" + str(random.randint(10, 31)), #Пример даты
        "comment": generate_random_string(30),
        "color": random.choice(colors) #Случайный выбор цветов (может быть пустой список)
    }


