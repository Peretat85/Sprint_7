import pytest
import allure

class TestCreateOrder:
    @pytest.mark.parametrize(
        "colors",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            [],  # Пустой список для случая, когда цвет не указан
        ],
        ids=["black_color", "grey_color", "both_colors", "no_color"]
    )

    @allure.title('Проверка создания заказа с разными вариантами цветов')
    def test_can_create_order_with_colors(self, api_client, order_data, colors):
        """Проверяем создание заказа с разными вариантами цветов."""
        order_data["color"] = colors  # Изменяем цвет в данных заказа
        response = api_client.create_order(order_data)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)  # Проверяем тип track

class TestGetOrderList:
    @allure.title('Проверка возврата списка в тело ответа')
    def test_can_get_order_list(self, api_client):
        """Проверяем, что в тело ответа возвращается список заказов."""
        response = api_client.get_order_list()
        assert response.status_code == 200
        assert isinstance(response.json(), dict)  # Проверяем, что ответ - словарь
        assert "orders" in response.json()  # Проверяем наличие ключа "orders"
        assert isinstance(response.json()["orders"], list)  # Проверяем, что "orders" - список