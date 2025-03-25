import pytest
import allure

class TestCreateCourier:
    @allure.title('Проверка возможности создания курьера')
    def test_can_create_courier(self, api_client, courier_data, delete_courier):
        """Курьера можно создать."""
        response = api_client.login_courier(courier_data) #пытаемся залогиниться
        assert response.status_code == 200
        assert isinstance(response.json()["id"],int) # проверяем наличие id (целое число)

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_cannot_create_duplicate_courier(self, api_client, courier_data, delete_courier):
        """Нельзя создать двух одинаковых курьеров."""
        # Повторно пытаемся зарегистрировать курьера с теми же данными
        # Создаём payload с данными существующего курьера
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }
        # Пытаемся зарегистрировать курьера с теми же данными
        response = api_client.create_courier(payload)  # Здесь вызываем create courier, а не register_new_courier
        assert response.status_code == 409  # Ожидаем конфликт
        assert response.json()["message"] == "Этот логин уже используется"

        #параметризация для проверки вывода ошибки при одном из отсутствующих полей
    @pytest.mark.parametrize(
        "random_courier_data_without_field", ["login", "password"], indirect=True,
        ids=["missing_login", "missing_password"],  # Добавляем ids
    )
    @allure.title('Проверка создания курьера при передаче в ручку всех обязательных полей')
    def test_create_courier_missing_field(self, api_client, random_courier_data_without_field, delete_courier):
        """Чтобы создать курьера, нужно передать в ручку все обязательные поля."""
        response = api_client.create_courier(random_courier_data_without_field)
        assert response.status_code == 400  # Ожидаем Bad Request
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

class TestLoginCourier:
    @allure.title('Проверка авторизации курьера')
    def test_can_login_courier(self, api_client, courier_data):
        """Курьер может авторизоваться."""
        response = api_client.login_courier(courier_data)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Проверка авторизации курьера при передаче всех обязательных полей: логин, пароль')
    def test_login_courier_missing_field(self, api_client, courier_data, delete_courier): #
        """Для авторизации нужно передать все обязательные поля."""
        data = courier_data.copy()
        data["password"] = ""
        response = api_client.login_courier(data)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Проверка возврата ошибки, если неправильно указать логин или пароль курьера')
    def test_login_courier_invalid_credentials(self, api_client, courier_data):
        """Система вернёт ошибку, если неправильно указать логин или пароль."""
        invalid_data = courier_data.copy()
        invalid_data["password"] = "++"
        response = api_client.login_courier(invalid_data)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Проверка возврата ошибки, если авторизоваться под несуществующим пользователем')
    def test_login_nonexistent_courier(self, api_client):
        """Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку."""
        nonexistent_data = {"login": "nonexistent_login", "password": "any_password"}
        response = api_client.login_courier(nonexistent_data)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"