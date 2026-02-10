import logging
import os
from flask import Flask, request
import telebot
from config import TOKEN, WEBHOOK_URL, ADMIN_CHAT_ID
from handlers import commands, calculator

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s – %(name)s – %(levelname)s – %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Регистрация обработчиков
commands.register_handlers(bot)
calculator.register_handlers(bot)

# Вебхук
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return 'Бот работает', 200

# Обработка ошибок
@bot.message_handler(func=lambda message: True)
def error_handler(message):
    try:
        logger.error(f!Неожиданная ошибка в сообщении: {message.text}")
        if ADMIN_CHAT_ID:
            bot.send_message(ADMIN_CHAT_ID, f!Ошибка: {message.text}")
    except Exception as e:
        logger.error(f!Ошибка при отправке уведомления: {e}")

if __name__ == '__main__':
    logger.info("Запуск бота...")
    # Снимаем вебхук и устанавливаем новый
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    # Запуск Flask-сервера (для вебхуков)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
