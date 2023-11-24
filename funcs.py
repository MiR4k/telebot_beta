import telebot
import mysql.connector
import datetime
# Открываем файл для записи логов
log_file = open("bot_logs.txt", "a")  # "a" - режим добавления новой информации в файл

# Функция для записи логов в файл
def log(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущая дата и время
    log_file.write(f"[{current_time}] {message}\n")
    log_file.flush()  # Сбрасываем буфер, чтобы гарантировать запись в файл

db_connection = mysql.connector.connect(
    host='localhost',
    user='Qosimjon',
    password='19739',
    database='hleb'
)
cursor = db_connection.cursor()


bot = telebot.TeleBot("6668392385:AAEv2_ROZSkJFQjaVp29uEhfFPrG6xN_Bp4")

def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, зарегистрирован ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        log(f"Пользователь {user_id} существует и вошёл в систему.")
        bot.send_message(user_id, f"Привет, {username}! Вы уже зарегистрированы.")
        # Отправка главного меню в зависимости от роли пользователя
        if user[3] == 'physical':
            send_physical_menu(user_id)
        elif user[3] == 'legal':
            send_legal_menu(user_id)
        elif user[3] == 'admin':
            send_admin_menu(user_id)
    else:
        register(message)

def register(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, зарегистрирован ли пользователь уже в базе данных
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        send_physical_menu(user_id)
    else:
        # Добавление нового пользователя в базу данных
        cursor.execute("INSERT INTO users (telegram_id, username, role) VALUES (%s, %s, %s)",
                       (user_id, username, 'physical'))  # 'physical' - роль для обычных пользователей
        db_connection.commit()
        bot.send_message(user_id, "Вы успешно зарегистрированы.")
        send_physical_menu(user_id)
        log(f"Новый пользователь {user_id} зарегистрирован.")



def process_admin_registration(message):
    admin_id = message.from_user.id
    registration_data = message.text.split()

    if len(registration_data) != 5:
        bot.send_message(admin_id, "Неправильный формат данных. Используйте: /register username role password user_id")

        return

    username_to_register = registration_data[1]
    role = registration_data[2]
    password = registration_data[3]
    telegram_id = registration_data[4]

    # Проверка, зарегистрирован ли уже этот пользователь
    cursor.execute("SELECT * FROM users WHERE username = %s", (username_to_register,)) # type: ignore
    registered_user = cursor.fetchone()

    if registered_user:
        bot.send_message(admin_id, f"Пользователь {username_to_register} уже зарегистрирован.")
    else:
        # Регистрация нового пользователя администратором
        cursor.execute("INSERT INTO users (username, role, password, telegram_id) VALUES (%s, %s, %s, %s)",
                       (username_to_register, role, password, telegram_id))
        db_connection.commit()
        bot.send_message(admin_id, f"Пользователь {username_to_register} успешно зарегистрирован.")
        log(f"Пользователь {admin_id} зарегистрировал нового пользователя {username_to_register}.")


# Функции для отправки различных меню в зависимости от роли пользователя
def send_physical_menu(user_id):
    # Отправка меню для физических лиц
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🍞 Каталог продуктов', '🛒 Моя корзина')
    markup.row('📊 Мои заказы', '⚙️ Настройки аккаунта')
    bot.send_message(user_id, "Выберите опцию:", reply_markup=markup)

def send_legal_menu(user_id):
    # Отправка меню для юридических лиц
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🍞 Каталог продуктов', '🛒 Моя корзина')
    markup.row('📊 Мои заказы', '⚙️ Настройки аккаунта', '💼 Мои счета-фактуры')
    bot.send_message(user_id, "Выберите опцию:", reply_markup=markup)

def send_admin_menu(user_id):
    # Отправка меню для администраторов
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📩 Новые заказы', '🚚 Управление доставкой')
    markup.row('📊 Статистика продаж', '⚙️ Настройки')
    bot.send_message(user_id, "Выберите опцию:", reply_markup=markup)