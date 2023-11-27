import mysql.connector
from mysql.connector import errorcode
from telebot import types

token = "AgACAgIAAxkBAAMJZVM5HakAAQiydf7Hh6-6t2Csz_VlAAI_1zEbOKuZSp7tqwi7l12wAQADAgADbQADMwQ"
# Подключение к базе данных
try:
    conn = mysql.connector.connect(
        user='pizducky',
        password='1111',
        host='localhost',
        database='hleb'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Неверные логин или пароль")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("База данных не существует")
    else:
        print(err)

cursor = conn.cursor()

# Определение типа пользователя по его id
def get_user_type(user_id):
    query = "SELECT user_type FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

# Определение статуса пользователя
def get_user_status(user_id):
    if get_user_type(user_id) == 'courier':
        query = "SELECT status FROM courier_status WHERE courier_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
    return None

# Главное меню
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_type = get_user_type(user_id)

    if user_type == 'ordinary':
        markup.row(types.KeyboardButton('Заказать продукцию'))
        markup.row(types.KeyboardButton('Посмотреть историю заказов'))
        markup.row(types.KeyboardButton('Посмотреть статус текущего заказа'))
    elif user_type == 'company_rep':
        markup.row(types.KeyboardButton('Заказать продукцию'))
        markup.row(types.KeyboardButton('Посмотреть статус заказа'))
        markup.row(types.KeyboardButton('Подтвердить получение заказа'))
        markup.row(types.KeyboardButton('Пополнить баланс'))
        markup.row(types.KeyboardButton('Управление шаблонами заказов'))
    elif user_type == 'courier':
        status = get_user_status(user_id)
        if status == 'free':
            markup.row(types.KeyboardButton('Стать на заказ'))
        elif status == 'on_delivery':
            markup.row(types.KeyboardButton('Подтвердить факт доставки'))
            markup.row(types.KeyboardButton('Отправить счет-фактуру'))
        elif status == 'inactive':
            markup.row(types.KeyboardButton('Активировать профиль'))

    return markup
