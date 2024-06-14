import telebot
import time

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Сообщения и медиа для рассылки
messages = [
    ("Привет! Вот первое видео.", "video1.mp4"),
    ("А теперь картинка с текстом.", "image1.jpg", "Это картинка с текстом."),
    # Добавить еще 5 сообщений
]

# Обработка команд
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Купить подписку", "Попробовать бесплатно", "Нужна помощь")
    bot.send_message(message.chat.id, "Привет! Я буду отправлять тебе контент с интервалом в 5 минут. Выбери нужную опцию ниже:", reply_markup=markup)

    # Рассылка сообщений
    for message_text, media_file, caption in messages:
        if media_file.endswith(".mp4"):
            bot.send_video(message.chat.id, open(media_file, "rb"), caption=caption)
        else:
            bot.send_photo(message.chat.id, open(media_file, "rb"), caption=caption)
        time.sleep(300)  # Ожидание 5 минут

# Обработка кнопки "Нужна помощь"
@bot.message_handler(func=lambda message: message.text == "Нужна помощь")
def help(message):
    # Открыть анонимный чат с ботом поддержки
    bot.send_message(message.chat.id, "Соединяю тебя со службой поддержки...")
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(3)
    bot.send_message(message.chat.id, "Теперь ты в анонимном чате. Напиши свое сообщение, и я его передам.")
# Получение запроса на анонимный чат
@bot.message_handler(commands=['anonchat'])
def anonchat(message):
    # Идентификатор анонимного чата
    anon_chat_id = str(message.chat.id)

    # Информация о текущем пользователе
    user_info = str(message.from_user.id) + ":" + str(message.from_user.username)

    # Пересылка сообщения в чат поддержки
    bot.send_message(TELEGRAM_SUPPORT_BOT_ID, f"Анонимный чат от {user_info}:\n{message.text}", disable_notification=True)

    # Отправка сообщения пользователю

    bot.send_message(message.chat.id, "Твое сообщение передано в анонимный чат.")


# Запуск бота
bot.polling()


