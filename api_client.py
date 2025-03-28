import requests
import random
import string
import allure

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step('Регистрация нового курьера и возврат списка данных: логин, пароль, имя')
    def register_new_courier(self):
        """Регистрирует нового курьера и возвращает данные регистрации."""
        def generate_random_string(length):  # Локальная функция
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f"{self.base_url}/courier", json=payload)

        if response.status_code == 201:
            return {"login": login, "password": password, "firstName": first_name}
        else:
            return None

    @allure.step('Создание курьера с переданными данными: логин, пароль, имя')
    def create_courier(self, data):  #
        """Создает курьера с заданными данными."""
        return requests.post(f"{self.base_url}/courier", json=data)

    @allure.step('Авторизация курьера ')
    def login_courier(self, data):
        return requests.post(f"{self.base_url}/courier/login", json=data)

    @allure.step('Удаление курьера')
    def delete_courier(self, login): #метод для удаления курьера
        return requests.delete(f"{self.base_url}/courier/{login}")

    @allure.step('Создание заказа')
    def create_order(self, data):
        return requests.post(f"{self.base_url}/orders", json=data)

    @allure.step('Получение списка заказов')
    def get_order_list(self):
        return requests.get(f"{self.base_url}/orders")
