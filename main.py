import telebot
from funcs import *

# Инициализация бота
bot = telebot.TeleBot("6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4")

# Обработка команды /start
@bot.message_handler(commands=['start'])
def _(message):
    start(message)
   

# Функция для регистрации пользователей для администраторов
@bot.message_handler(commands=['admin_register'])
def admin_register(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, имеет ли пользователь права администратора
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s AND role = 'admin'", (user_id,))
    admin_user = cursor.fetchone()

    if admin_user:
        # Получение информации о пользователе, которого нужно зарегистрировать (в данном случае, по его username)
        bot.send_message(user_id, "Используйте: /register username role password user_id")
        bot.register_next_step_handler(message, process_admin_registration)

    else:
        log(f"Пользователь {user_id} Отправил команду admin_register.")
        bot.send_message(user_id, "У вас нет прав для выполнения этой операции.")



log("Бот Запущен")
print("Bot Enabled")
# Запуск бота
bot.polling()

