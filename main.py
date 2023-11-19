import telebot
import mysql.connector
from trio import current_time
import funcs
import datetime  # Для работы с датой и временем

# Открываем файл для записи логов
log_file = open("bot_logs.txt", "a")  # "a" - режим добавления новой информации в файл


# Установка соединения с базой данных
db_connection = mysql.connector.connect(
    host='localhost',
    user='Qosimjon',
    password='19739',
    database='Qosimjon'
)
cursor = db_connection.cursor()

# Инициализация бота
bot = telebot.TeleBot("6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4")

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, зарегистрирован ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        funcs.log(f"Пользователь {user_id} существует и вошёл в систему.")
        bot.send_message(user_id, f"Привет, {username}! Вы уже зарегистрированы.")
        # Отправка главного меню в зависимости от роли пользователя
        if user[3] == 'physical':
            funcs.send_physical_menu(user_id)
        elif user[3] == 'legal':
            funcs.send_legal_menu(user_id)
        elif user[3] == 'admin':
            funcs.send_admin_menu(user_id)
    else:
        funcs.log(f"Новый пользователь {user_id} зарегистрировался.")
        funcs.authorization(message)


# Функция для обработки команды Авторизироваться для простой регистрации
@bot.message_handler(func=lambda message: message.text == 'Авторизироваться')
def register(message):
    user_id = message.from_user.id
    username = message.from_user.username
    password = message.text.split()

    # Проверка, зарегистрирован ли пользователь уже в базе данных
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        bot.send_message(user_id, "Вы уже зарегистрированы.")
    else:
        # Добавление нового пользователя в базу данных
        cursor.execute("INSERT INTO users (telegram_id, username, role, password) VALUES (%s, %s, %s, %s)",
                       (user_id, username, 'physical'))  # 'physical' - роль для обычных пользователей
        db_connection.commit()
        bot.send_message(user_id, "Вы успешно зарегистрированы.")
        funcs.send_physical_menu(user_id)

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
        bot.register_next_step_handler(message, funcs.process_admin_registration)

    else:
        funcs.log(f"Пользователь {user_id} Отправил команду admin_register.")
        bot.send_message(user_id, "У вас нет прав для выполнения этой операции.")


funcs.log(f'Бот Запущен ')

# Запуск бота
bot.polling()
