import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать!", reply_markup=config.main_menu(user_id))

# Обработка кнопок главного меню
@bot.message_handler(func=lambda message: True)
def handle_main_menu(message):
    user_id = message.from_user.id
    user_type = config.get_user_type(user_id)

    if user_type == 'ordinary':
        if message.text == 'Заказать продукцию':
            # Обработка заказа продукции
            pass
        elif message.text == 'Посмотреть историю заказов':
            # Обработка просмотра истории заказов
            pass
        elif message.text == 'Посмотреть статус текущего заказа':
            # Обработка просмотра статуса текущего заказа
            pass
    elif user_type == 'company_rep':
        if message.text == 'Заказать продукцию':
            # Обработка заказа продукции
            pass
        elif message.text == 'Посмотреть статус заказа':
            # Обработка просмотра статуса заказа
            pass
        elif message.text == 'Подтвердить получение заказа':
            # Обработка подтверждения получения заказа
            pass
        elif message.text == 'Пополнить баланс':
            # Обработка пополнения баланса
            pass
        elif message.text == 'Управление шаблонами заказов':
            # Обработка управления шаблонами заказов
            pass
    elif user_type == 'courier':
        status = config.get_user_status(user_id)
        if status == 'free':
            if message.text == 'Стать на заказ':
                # Обработка старта выполнения заказа
                pass
        elif status == 'on_delivery':
            if message.text == 'Подтвердить факт доставки':
                # Обработка подтверждения факта доставки
                pass
            elif message.text == 'Отправить счет-фактуру':
                # Обработка отправки счет-фактуры
                pass
        elif status == 'inactive':
            if message.text == 'Активировать профиль':
                # Обработка активации профиля
                pass

if __name__ == '__main__':
    bot.polling(none_stop=True)
