import telebot
import language_tool_python
import logging

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)

def correct_text(text):
    try:
        tool = language_tool_python.LanguageTool('ru-RU')
        matches = tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return corrected_text
    except Exception as e:
        logging.error(f"Ошибка при проверке текста: {e}")
        return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне текст, и я исправлю ошибки.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    corrected_text = correct_text(text)
    if corrected_text:
        bot.reply_to(message, f"Исходный текст: {text}\nИсправленный текст: {corrected_text}")
    else:
        bot.reply_to(message, "Произошла ошибка при проверке текста. Попробуйте еще раз.")

if __name__ == "__main__":
    try:
        logging.info("Бот запущен и готов к работе.")
        bot.polling()
    except Exception as e:
        logging.critical(f"Произошла критическая ошибка: {e}")
