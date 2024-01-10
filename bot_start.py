# main_bot.py
import telebot
from extensions import CurrencyConverter, APIException
from config import TELEGRAM_BOT_TOKEN

class BotHandler:
    @staticmethod
    def start(message):
        instructions = "Привет! Я бот для конвертации валют. Чтобы узнать цену, отправьте сообщение в формате:\n" \
                        "<имя валюты> <валюта, в которую хотите перевести> <количество>\n" \
                        "Например: USD RUB 100\n\n" \
                        "Доступные команды:\n" \
                        "/start - Начать работу с ботом\n" \
                        "/help - Получить инструкции по использованию\n" \
                        "/values - Посмотреть список доступных валют"
        return instructions

    @staticmethod
    def help(message):
        return BotHandler.start(message)

    @staticmethod
    def values(message):
        currencies = "Доступные валюты:\n" \
                     "- USD (Доллар США)\n" \
                     "- EUR (Евро)\n" \
                     "- RUB (Российский рубль)"
        return currencies

    @staticmethod
    def get_currency_price(message):
        try:
            text = message.text.split()
            if len(text) != 3:
                raise APIException("Неверный формат запроса. Введите три параметра: <валюта> <валюта> <количество>")

            base_currency = text[0].upper()
            quote_currency = text[1].upper()
            amount = float(text[2])

            result = CurrencyConverter.get_price(base_currency, quote_currency, amount)
            return f"{amount} {base_currency} = {result} {quote_currency}"

        except ValueError:
            raise APIException("Некорректное количество валюты")

        except APIException as e:
            raise e

def main():
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.send_message(message.chat.id, BotHandler.start(message))

    @bot.message_handler(commands=['values'])
    def handle_values(message):
        bot.send_message(message.chat.id, BotHandler.values(message))

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        try:
            result = BotHandler.get_currency_price(message)
            bot.send_message(message.chat.id, result)
        except APIException as e:
            bot.send_message(message.chat.id, f"Ошибка: {e.message}")

    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
