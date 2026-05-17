import allure
import pytest
import requests
from helps import DataCourier
from endpoints import Endpoints
from urls import Urls


class TestCreateCourier:

    @allure.title('Проверка создания нового курьера')
    @allure.description('Отправляем запрос на создание курьера, проверяем ответ и удаляем созданного курьера')
    def test_registration_courier_success(self, courier):
        courier_data = courier
        assert courier_data["status_code"] == 201
        assert courier_data["response_text"] == '{"ok":true}'

    @allure.title('Проверка ошибки при создании двух одинаковых курьеров')
    @allure.description('Отправляем повторный запрос на создание курьера, проверяем ответ и удаляем курьера')
    def test_registration_double_courier_failed(self, courier):
        response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier["data"])
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @allure.title('Проверка ошибки при создании курьера без заполнения обязательных полей Login/Password')
    @allure.description('Отправляем запрос на создание курьера без заполнения обязательных полей Login/Password и проверяем ответ')
    @pytest.mark.parametrize('courier_data', [DataCourier.invalid_data_login_without_login,
                                           DataCourier.invalid_data_login_without_password])
    def test_courier_registration_without_parameters_failed(self, courier_data):
        response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text
