import allure
import pytest
import requests
from helps import DataCourier
from endpoints import Endpoints
from urls import Urls


class TestCreateCourier:

    @allure.title('Проверка создания нового курьера')
    @allure.description('Отправляем запрос на создание курьера, проверяем ответ и удаляем созданного курьера')
    def test_registration_courier_success(self):
        # Генерируем уникальные данные курьера (логин, пароль, имя)
        courier_data = DataCourier.generate_courier_data()  # предполагаем, что есть такой метод

        # Шаг 1: создание курьера
        with allure.step(f"Отправить POST-запрос на создание курьера с данными {courier_data}"):
            create_response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)

        # Шаг 2: проверка ответа
        with allure.step("Проверить, что курьер создан успешно"):
            assert create_response.status_code == 201
            assert create_response.json() == {"ok": True}

        # Шаг 3: удаление курьера (для чистоты данных)
        with allure.step("Удалить созданного курьера"):
            login_pass = {"login": courier_data["login"], "password": courier_data["password"]}
            login_response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.login_courier}', data=login_pass)
            courier_id = login_response.json().get("id")
            if courier_id:
                requests.delete(f'{Urls.QA_SCOOTER_URL}{Endpoints.delete_courier}/{courier_id}')

    @allure.title('Проверка ошибки при создании двух одинаковых курьеров')
    @allure.description('Отправляем повторный запрос на создание курьера, проверяем ответ и удаляем курьера')
    def test_registration_double_courier_failed(self):
        # Создаём уникального курьера в теле теста
        courier_data = DataCourier.generate_courier_data()

        with allure.step("Создать первого курьера"):
            response_first = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)
            assert response_first.status_code == 201

        with allure.step("Попытаться создать второго курьера с теми же данными"):
            response_second = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)

        with allure.step("Проверить, что сервер вернул ошибку 409 с соответствующим сообщением"):
            assert response_second.status_code == 409
            assert DataCourier.DUPLICATE_LOGIN_ERROR in response_second.text

        # Очистка: удаляем созданного курьера
        with allure.step("Удалить созданного курьера"):
            login_pass = {"login": courier_data["login"], "password": courier_data["password"]}
            login_response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.login_courier}', data=login_pass)
            courier_id = login_response.json().get("id")
            if courier_id:
                requests.delete(f'{Urls.QA_SCOOTER_URL}{Endpoints.delete_courier}/{courier_id}')

    @allure.title('Проверка ошибки при создании курьера без заполнения обязательных полей (Login/Password)')
    @allure.description('Отправляем запрос на создание курьера без заполнения обязательных полей и проверяем ответ')
    @pytest.mark.parametrize('courier_data', [
        DataCourier.INVALID_DATA_WITHOUT_LOGIN,
        DataCourier.INVALID_DATA_WITHOUT_PASSWORD
    ])
    def test_courier_registration_without_parameters_failed(self, courier_data):
        with allure.step(f"Отправить POST-запрос на создание курьера с неполными данными: {courier_data}"):
            response = requests.post(f'{Urls.QA_SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)

        with allure.step("Проверить, что сервер вернул ошибку 400 с соответствующим сообщением"):
            assert response.status_code == 400
            assert DataCourier.INSUFFICIENT_DATA_ERROR in response.text
