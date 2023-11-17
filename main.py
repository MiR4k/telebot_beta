import telebot
from telebot import types
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Создание экземпляра бота
bot = telebot.TeleBot('6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4')
# Список фотографий товаров с их описаниями (замени на свои данные)
catalog_items = [
    {'photo': 'AgACAgIAAxkBAAMQZVM6siVjGQqCNKI6nAObo1Xz-3wAAmXTMRuLfKFKHNOX1yMbO_YBAAMCAANtAAMzBA', 'description': 'Описание товара 1'},
    {'photo': 'AgACAgIAAxkBAAMRZVM6xbOB1s63csQpU_ypHFkC5rIAAmfTMRuLfKFKmGm0kfaO2PwBAAMCAANtAAMzBA', 'description': 'Описание товара 2'},
    {'photo': 'AgACAgIAAxkBAAMTZVM63IeRLCpM3XSnowceRsiVvoAAAmnTMRuLfKFK-ksIdDCv0BIBAAMCAANtAAMzBA', 'description': 'Описание товара 3'},
    # Добавь свои фотографии и описания здесь
]

current_photo_index = 0
korzina = 0

# Функция для обновления текущей фотографии с описанием
def update_catalog_item(chat_id, item_index, message_id=None):
    item = catalog_items[item_index]
    photo = item['photo']
    description = item['description']

    keyboard = types.InlineKeyboardMarkup()
    button_previous = types.InlineKeyboardButton("<-", callback_data="previous")
    button_plus = types.InlineKeyboardButton("+", callback_data="plus")
    button_next = types.InlineKeyboardButton("->", callback_data="next")
    keyboard.add(button_previous, button_plus, button_next)

    if message_id:  # Если сообщение существует, обновляем его
        bot.edit_message_media(media=types.InputMediaPhoto(photo, caption=description), chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
    else:  # Если сообщения нет, отправляем новое
        bot.send_photo(chat_id, photo, caption=description, reply_markup=keyboard)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Добро пожаловать!')
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


# Обработчик команды /каталог
@bot.message_handler(commands=['katalog'])
def catalog(message):
    update_catalog_item(message.chat.id, current_photo_index)

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
    global korzina


    if call.data == "previous":
        current_photo_index = (current_photo_index - 1) % len(catalog_items)
        update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    elif call.data == "next":
        current_photo_index = (current_photo_index + 1) % len(catalog_items)
        update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    elif call.data == "plus":
        korzina += 1
        print(korzina)
    logger.info(f"Пользователь {call.from_user.id} нажал кнопку {call.data}")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message):
    # Здесь можно добавить логику обработки текстовых сообщений
    # Пример: отправить эхо-ответ на полученное сообщение
    logger.info(f"Пользователь {message.from_user.id} отправил текстовое сообщение: '{message.text}'")


# Вывод сообщения о запуске бота в консоль
logger.info("Бот запущен")

# Запуск бота
bot.polling()




