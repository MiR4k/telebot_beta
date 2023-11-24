import telebot
from funcs import *

# Инициализация бота
bot = telebot.TeleBot("6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4")



# Обработка команды /start
@bot.message_handler(commands=['start'])
def _(message):
    start(message)
   


# Функция для регистрации пользователей администратором
@bot.message_handler(commands=['admin_register'])
def admin_register(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, имеет ли пользователь права администратора
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s AND role = 'admin'", (user_id))
    admin_user = cursor.fetchone()

    if admin_user:
        # Получение информации о пользователе, которого нужно зарегистрировать (в данном случае, по его username)
        bot.send_message(user_id, "Используйте: /register username role password user_id")
        bot.register_next_step_handler(message, process_admin_registration)

    else:
        log(f"Пользователь {user_id} Отправил команду admin_register.")
        bot.send_message(user_id, "У вас нет прав для выполнения этой операции.")

@bot.message_handler(content_types=['text'])
def process_text_message(message):
    user_id = message.from_user.id
    if message.text == "🍞 Каталог продуктов":
        update_catalog_item(message.chat.id, current_photo_index)    
    else:
        bot.send_message(user_id,  "Извини, не понял твоего сообщения. Можешь повторить?")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global current_photo_index

    if call.data == "previous":
        current_photo_index = (current_photo_index - 1) % len(catalog_items)
        update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    elif call.data == "next":
        current_photo_index = (current_photo_index + 1) % len(catalog_items)
        update_catalog_item(call.message.chat.id, current_photo_index, message_id=call.message.message_id)

    log(f"Пользователь {call.from_user.id} нажал кнопку {call.data}")


log("Бот Запущен")
print("Bot Enabled")

# Запуск бота
bot.polling()

