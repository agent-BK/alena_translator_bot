import telebot
from data.languages import Languages


def get_keyboard_lang():
    keyboard_lang = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard_lang_tmp = [item for item in Languages.dict_languages_translation.values()]
    keyboard_lang_tmp.append('Отмена')
    keyboard_lang.add(*keyboard_lang_tmp)
    return keyboard_lang


def keyboard_remove():
    return telebot.types.ReplyKeyboardRemove()
