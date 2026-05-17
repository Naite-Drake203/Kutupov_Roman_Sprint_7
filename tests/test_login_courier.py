import allure
import pytest
import requests
from helps import DataCourier, Courier
from endpoints import Endpoints
from urls import Urls


class TestLoginCourier:

    @allure.title('Проверка авторизации курьера с валидными данными')
    @allure.description('Отправляем запрос на авторизацию в сервисе, проверяем ответ и удаляем курьера')
    def test_courier_login_success(self, courier):
        courier_data = courier
        response = Courier().courier_login_in_the_system_and_get_id_courier(courier_data["data"])
        assert response["status_code"] == 200
        assert response.get("id")

    @allure.title('Проверка ошибки при авторизации курьера без заполнения обязательных полей Login/Password')
    @allure.description('''Отправляем запрос на авторизацию в сервисе без заполнения обязательных полей Login/Password
                         и проверяем ответ''')
    @pytest.mark.parametrize('courier_data', [DataCourier.invalid_data_login_without_login,
                                           DataCourier.invalid_data_login_without_password])
    def test_courier_login_without_parameters_failed(self, courier_data):
        response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.login_courier}', data=courier_data)
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text

    @allure.title('Проверка ошибки при авторизации курьера с несуществующими данными')
    @allure.description('Отправляем запрос на авторизацию в сервисе с несуществующими данными и проверяем ответ')
    def test_courier_login_without_null_login_failed(self):
        response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.login_courier}', data=DataCourier.null_data_login)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text
