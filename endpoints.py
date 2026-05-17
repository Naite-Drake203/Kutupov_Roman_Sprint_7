# ручки API
class Endpoints:
    create_courier = "/api/v1/courier"  # Создание курьера
    login_courier = "/api/v1/courier/login"  # Логин курьера в системе
    create_order = "/api/v1/orders"  # Создание заказа
    delete_courier = '/api/v1/courier/'  # Удаление курьера
    get__number_courier_orders = '/api/v1/courier/:id/ordersCount'  # Получить количество заказов курьера
    finish_order = '/api/v1/orders/finish/'  # Завершить заказ
    cancel_order = '/api/v1/orders/cancel'  # Отменить заказ
    get_orders_list = '/api/v1/orders'  # Получение списка заказов
    accept_order_by_number = '/api/v1/orders/track'  # Получить заказ по его номеру
    accept_order = '/api/v1/orders/accept/:id'  # Принять заказ
