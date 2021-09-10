from data.chanel_text import ChannelText
from utils.bot_manager import BotManager
import telebot
from data.private_chanel_data import ChanelData
from utils import translation


class ActionsChanel:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(ActionsChanel, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.bot = BotManager.get_bot()

    def checking_group_member(self, mes_id):
        """ проверка подписки на канал """
        try:
            result = self.bot.get_chat_member(ChanelData.id, mes_id)
            if result.status in ChanelData.user_status:
                return True
            else:
                return False
        except telebot.apihelper.ApiTelegramException as e:
            if e.result_json['description'] == 'Bad Request: user not found':
                return False

    def channel_subscription_offers(self, message):
        """ сообщение с предложением подписки на канал """
        mes_id = message.from_user.id
        user_name = translation.translate_name(message.from_user.first_name)
        text_out = ChannelText.text_welcome.format(user_name)
        self.bot.send_message(mes_id, text=text_out, parse_mode='html')
