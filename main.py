import telebot
from telebot import types
import logging
import funcs

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Создание экземпляра бота
bot = telebot.TeleBot('6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4')
# Список фотографий товаров с их описаниями (замени на свои данные)


current_photo_index = 0



# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_authorized = funcs.check_authorization(message.from_user.id)

    if user_authorized:
        # Пользователь авторизован - выводим обычные кнопки
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = types.KeyboardButton('Добавить')
        button2 = types.KeyboardButton('Список Заказов')
        button3 = types.KeyboardButton('Корзина')
        keyboard.add(button1, button2, button3)
        bot.send_message(chat_id, 'Выберите действие:', reply_markup=keyboard)
    else:
        # Пользователь не авторизован - выводим кнопку для авторизации
        auth_button = types.KeyboardButton('Авторизоваться')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(auth_button)
        bot.send_message(chat_id, 'Для начала работы необходимо авторизоваться.', reply_markup=keyboard)





# Обработчик команды /каталог
@bot.message_handler(commands=['katalog'])
def catalog(message):
    funcs.update_catalog_item(message.chat.id, current_photo_index)

# # Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def show_menu(message):
    bot.send_message(message.chat.id, 'меню')
    logger.info(f"Пользователь {message.from_user.id} вызвал меню")

#     keyboard = types.InlineKeyboardMarkup()
#     button_previous = types.InlineKeyboardButton("< Предыдущий", callback_data="previous")
#     button_plus = types.InlineKeyboardButton("+", callback_data="plus")
#     button_next = types.InlineKeyboardButton("Следующий >", callback_data="next")
#     keyboard.add(button_previous, button_plus, button_next)
#     bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# Обработчик нажатий на инлайн кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global current_photo_index

    if call.data == "previous":
        current_photo_index = (current_photo_index - 1) % len(funcs.catalog_items)
        funcs.update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    elif call.data == "next":
        current_photo_index = (current_photo_index + 1) % len(funcs.catalog_items)
        funcs.update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    logger.info(f"Пользователь {call.from_user.id} нажал кнопку {call.data}")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message):
    # Здесь можно добавить логику обработки текстовых сообщений
    # Пример: отправить эхо-ответ на полученное сообщение
    logger.info(f"Пользователь {message.from_user.id} отправил текстовое сообщение: '{message.text}'")


# закрытие подключения к бд

# Вывод сообщения о запуске бота в консоль
logger.info("Бот запущен")

# Запуск бота
bot.polling()




