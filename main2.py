import telebot
from telebot import types

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Создание инлайн-клавиатуры с кнопкой "Ответить"
    keyboard = types.InlineKeyboardMarkup()
    reply_button = types.InlineKeyboardButton("Ответить", callback_data="reply")
    keyboard.add(reply_button)

    # Получение и пересылка сообщения боту-рассыльщику
    bot.send_message(TELEGRAM_BOT_ID, message.text, disable_notification=True)

    # Ответ пользователю с инлайн-клавиатурой
    bot.send_message(message.chat.id, "Твое сообщение передано.", reply_markup=keyboard)

# Обработка нажатия на кнопку "Ответить"
@bot.callback_query_handler(func=lambda call: call.data == "reply")
def reply_to_message(call):
    # Создание клавиатуры с полем для ввода сообщения
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    message_input = types.KeyboardButton("Введите сообщение")
    keyboard.add(message_input)

    # Отправка сообщения с клавиатурой
    bot.send_message(call.message.chat.id, "Введите сообщение для ответа:", reply_markup=keyboard)

    # Переход в режим ожидания ответа
    bot.register_next_step_handler(call.message, send_reply)

def send_reply(message):
    # Отправка ответа боту-рассыльщику
    bot.send_message(TELEGRAM_BOT_ID, message.text, disable_notification=True)

    # Отправка сообщения пользователю об успешной отправке
    bot.send_message(message.chat.id, "Ответ отправлен.")

# Обработка добавления постов
@bot.message_handler(commands=['addpost'])
def add_post(message):
    # Создание инлайн-клавиатуры с кнопкой "Добавить пост"
    keyboard = types.InlineKeyboardMarkup()
    add_post_button = types.InlineKeyboardButton("Добавить пост", callback_data="add_post")
    keyboard.add(add_post_button)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы добавить пост.", reply_markup=keyboard)

# Обработка нажатия на кнопку "Добавить пост"
@bot.callback_query_handler(func=lambda call: call.data == "add_post")
def handle_add_post(call):
    # Получение текста и медиа
    text = call.message.text[8:]
    media = call.message.photo or call.message.video

    # Если есть медиа, то сохранить его и извлечь содержимое
    if media:
        file_info = bot.get_file(media.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"{media.file_id}.{media.file_name}", "wb") as f:
            f.write(downloaded_file)

        # Определение типа медиа
        if media.file_name.endswith(".mp4"):
            media_type = "video"
            media_file = f"{media.file_id}.{media.file_name}"
        else:
            media_type = "image"
            media_file = f"{media.file_id}.{media.file_name}"
    else:
        media_type = None
        media_file = None

    # Добавление поста в список рассылки бота-рассыльщика
    messages.append((text, media_file, media_type))

    # Отправка сообщения пользователю
    bot.send_message(call.message.chat.id, "Пост добавлен в рассылку.")

# Запуск бота
bot.polling()

