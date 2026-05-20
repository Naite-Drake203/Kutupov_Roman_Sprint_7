import allure
import requests
from endpoints import Endpoints
from urls import Urls


class TestOrdersList:

    @allure.title('Проверка получения списка заказов')
    @allure.description('Получаем списки заказов и проверяем ответ')
    def test_list_orders_success(self):
        response = requests.get(f'{Urls.QA_SCOOTER_URL}{Endpoints.get_orders_list}')
        assert response.status_code == 200
        assert "track" in response.text
