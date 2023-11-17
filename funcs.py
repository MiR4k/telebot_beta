import mysql.connector

# Установка соединения с базой данных
db_connection = mysql.connector.connect(
    host="localhost",
    user="Qosimjon",
    password="19739",
    database="hleb"
)

# Функция проверки авторизации по tg_id
def check_authorization_with_tg_id(tg_id, mode='bool'):
    cursor = db_connection.cursor()
    query = "SELECT * FROM personal WHERE tg_id = %s"
    cursor.execute(query, (tg_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        print("Авторизация успешна.")
        # Здесь можно добавить дополнительные действия после успешной авторизации
    else:
        print("Пользователь не найден или доступ запрещен.")


# telegram_id = 906893530
# check_authorization_with_tg_id(telegram_id)

# Закрытие соединения с базой данных

catalog_items = [
    {'photo': 'AgACAgIAAxkBAAMQZVM6siVjGQqCNKI6nAObo1Xz-3wAAmXTMRuLfKFKHNOX1yMbO_YBAAMCAANtAAMzBA', 
    'description': 'Описание товара 1'},
    {'photo': 'AgACAgIAAxkBAAMRZVM6xbOB1s63csQpU_ypHFkC5rIAAmfTMRuLfKFKmGm0kfaO2PwBAAMCAANtAAMzBA',
    'description': 'Описание товара 2'},
    {'photo': 'AgACAgIAAxkBAAMTZVM63IeRLCpM3XSnowceRsiVvoAAAmnTMRuLfKFK-ksIdDCv0BIBAAMCAANtAAMzBA', 
    'description': 'Описание товара 3'},
    # Добавь свои фотографии и описания здесь
]


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



def check_authorization(tg_id):
    cursor = db_connection.cursor()
    query = "SELECT * FROM personal WHERE tg_id = %s"
    cursor.execute(query, (tg_id,))
    user = cursor.fetchone()
    cursor.close()

    return True if user else False

# db_connection.close()
