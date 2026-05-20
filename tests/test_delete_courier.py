import allure
from helps import Courier


class TestDeleteCourier:

    @allure.title('Проверка удаления курьера')
    @allure.description('Отправляем запрос на удаление курьера и проверяем ответ')
    def test_delete_courier_success(self, courier_delete):
        courier_id = courier_delete
        with allure.step(f"Отправить запрос на удаление курьера с id {courier_id['id']}"):
            response = Courier().courier_subsequent_deletion(courier_id["id"])
        with allure.step("Проверить, что курьер успешно удалён (статус 200, ответ {'ok':true})"):
            assert response["status_code"] == 200
            assert response["response_text"] == '{"ok":true}'

    @allure.title('Проверка удаления курьера с несуществующим ID')
    @allure.description('Отправляем запрос на удаление курьера с несуществующим ID и проверяем ответ')
    def test_delete_courier_invalid_id_failed(self):
        courier_id = '123456'
        with allure.step(f"Отправить запрос на удаление курьера с несуществующим id {courier_id}"):
            response = Courier().courier_subsequent_deletion(courier_id)
        with allure.step("Проверить, что сервер вернул ошибку 404 с сообщением 'Курьера с таким id нет'"):
            assert response["status_code"] == 404
            assert "Курьера с таким id нет" in response["response_text"]

    @allure.title('Проверка удаления курьера без ID')
    @allure.description('Отправляем запрос на удаление курьера без ID и проверяем ответ')
    def test_delete_courier_none_id_failed(self):
        courier_id = None
        with allure.step(f"Отправить запрос на удаление курьера с id = {courier_id}"):
            response = Courier().courier_subsequent_deletion(courier_id)
        with allure.step("Проверить, что сервер вернул ошибку 500 с сообщением 'invalid input syntax'"):
            assert response["status_code"] == 500
            assert "invalid input syntax" in response["response_text"]
