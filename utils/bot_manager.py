import telebot
from data.private_bot_data import BotData


class BotManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = telebot.TeleBot(BotData.token)

    @classmethod
    def get_bot(cls):
        if cls._instance is None:
            BotManager()
        return cls._instance

    @classmethod
    def set_polling(cls):
        cls._instance.polling(none_stop=True, interval=0)
