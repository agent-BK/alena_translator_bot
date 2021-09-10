import requests
import modules.analytic.analytic as analytic
from data.private_analytics_data import AnalyticData
from data.bot_text import BotText
from data.languages import Languages
from data.private_bot_data import BotData
from utils import function, translation, conversion, config_keyboard
from utils.actions_chanel import ActionsChanel
from utils.bot_manager import BotManager

bot = BotManager.get_bot()


@bot.message_handler(commands=['start', 'старт', 'Start'])
def start_start(message):
    message_id = message.from_user.id
    if ActionsChanel().checking_group_member(message_id):
        bot.send_message(message_id, text=BotText.welcome.format(
            translation.translate_name(message.from_user.first_name)))
        analytic.statistics(message_id, message.text)
    else:
        ActionsChanel().channel_subscription_offers(message)


@bot.message_handler(commands=['help', 'помощь', 'Help'])
def start_help(message):
    message_id = message.from_user.id
    if ActionsChanel().checking_group_member(message_id):
        bot.send_message(message_id, text=function.get_help_text())
        analytic.statistics(message_id, message.text)
    else:
        ActionsChanel().channel_subscription_offers(message)


@bot.message_handler(commands=['lang', 'язык', 'Lang'])
def start_lang(message):
    """ смена языка на который переводим и вызов клавиатуры выбора варианта языков """
    message_id = message.from_user.id
    if ActionsChanel().checking_group_member(message_id):
        analytic.statistics(message_id, message.text)
        bot.send_message(message_id, text=BotText.language_input, reply_markup=config_keyboard.get_keyboard_lang())
        bot.register_next_step_handler(message, change_lang_in)
    else:
        ActionsChanel().channel_subscription_offers(message)


def change_lang_in(message):
    text = message.text
    message_id = message.from_user.id

    if text in Languages.dict_languages_translation.values():
        lang_in_temp = function.get_key(Languages.dict_languages_translation, text)
        text_out = BotText.language_select.format(Languages.dict_languages_translation[lang_in_temp])
        bot.send_message(message_id, text=text_out)
        bot.register_next_step_handler(message, change_lang_out, lang_in_temp)

    elif text.lower() == 'отмена':
        b_lang = translation.base_lang(message, read=True)
        text_out = BotText.language_not_changed.format(
            Languages.dict_languages_translation[b_lang[0]], Languages.dict_languages_translation[b_lang[1]])
        bot.send_message(message_id, text=text_out, reply_markup=config_keyboard.keyboard_remove())

    else:
        bot.send_message(message_id, text=BotText.not_understand_change_lang)
        bot.register_next_step_handler(message, change_lang_in)


def change_lang_out(message, lang_in_temp):
    text = message.text
    message_id = message.from_user.id

    if text in Languages.dict_languages_translation.values():
        lang_in = lang_in_temp
        lang_out = function.get_key(Languages.dict_languages_translation, text)

        translation.base_lang(message, lic=lang_in, loc=lang_out)
        text_out = BotText.languages_selected.format(
            Languages.dict_languages_translation[lang_in], Languages.dict_languages_translation[lang_out])
        bot.send_message(message_id, text=text_out, reply_markup=config_keyboard.keyboard_remove())

    elif text.lower() == 'отмена':
        b_lang = translation.base_lang(message, read=True)
        text_out = BotText.language_not_changed.format(
            Languages.dict_languages_translation[b_lang[0]], Languages.dict_languages_translation[b_lang[1]])
        bot.send_message(message_id, text=text_out, reply_markup=config_keyboard.keyboard_remove())
    else:
        bot.send_message(message_id, text=BotText.not_understand_change_lang)
        bot.register_next_step_handler(message, change_lang_out, lang_in_temp)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def text_processing(message):
    """ обработка текстовых сообщений """
    message_id = message.from_user.id

    if ActionsChanel().checking_group_member(message_id):
        message_user = message.text

        if (message_user in AnalyticData.words_login) and (message_id == AnalyticData.admin_id):
            analytic.get_statistics(message, bot, config_keyboard.keyboard_remove(), AnalyticData.password)
        else:
            text_translate = translation.translate(message_user, transcription=True, message=message)
            bot.send_message(message_id, text=text_translate[0])

            translation.pronounce(text_translate, message_id)
            voice = conversion.text_in_audio(message, text_translate[0])

            if voice:
                bot.send_voice(message.from_user.id, voice)

            analytic.statistics(message_id, 'текст')
    else:
        ActionsChanel().channel_subscription_offers(message)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    """ обработка голосовых сообщей """
    message_id = message.from_user.id

    if ActionsChanel().checking_group_member(message_id):
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{BotData.token}/{file_info.file_path}')
        audio_bytes = conversion.convert(in_bytes=file.content, ogg=True)
        text = conversion.audio_text(audio_bytes, translation.base_lang(message, read=True)[0])

        if text:
            text_translate = translation.translate(text, transcription=True, message=message)
            bot.send_message(message_id, text=text)
            bot.send_message(message_id, text=text_translate[0])
            analytic.statistics(message_id, 'голос')
            translation.pronounce(text_translate, message_id)
            voice = conversion.text_in_audio(message, text_translate[0])
            if voice:
                bot.send_voice(message.from_user.id, voice)
        else:
            bot.send_message(message_id, text=BotText.not_understand)
    else:
        ActionsChanel().channel_subscription_offers(message)


BotManager.set_polling()
