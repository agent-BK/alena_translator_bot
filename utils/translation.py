import re
from data.languages import Languages
from modules.google_tn.google_tn import google_translator
import csv
import pandas as pd
from utils.bot_manager import BotManager


def translate_name(user_name):
    """ перевод имени пользователя"""
    if not re.search(r'[а-я,А-я]', user_name):
        user_name = translate(user_name, ('en-GB', 'ru-RU'))
    return user_name


def translate(text, lang=None, transcription=False, message=None):
    """ перевод текста """
    lang_in, lang_to = base_lang(message, read=True) if not lang and message else lang
    return google_translator().translate(text, lang_src=lang_in, lang_tgt=lang_to, pronounce=transcription)


def base_lang(message, read=False, lic=None, loc=None):
    """поключение к файлу csv базы данных языка"""
    base_lang_name = './base/lang_base.csv'
    df = pd.read_csv(base_lang_name, delimiter=';', encoding='cp1251', index_col="id")
    message_id = message.from_user.id

    if message_id not in df.index:
        with open(base_lang_name, 'a', newline="", encoding='cp1251') as file:
            wr = csv.writer(file, delimiter=';')
            if lic and loc:
                wr.writerow([message_id, lic, loc])
                if read:
                    df.loc[message_id, 'lang_in'] = lic
                    df.loc[message_id, 'lang_out'] = loc
            else:
                wr.writerow([message_id, Languages.lang_in, Languages.lang_out])
                if read:
                    df.loc[message_id, 'lang_in'] = Languages.lang_in
                    df.loc[message_id, 'lang_out'] = Languages.lang_out

    elif lic and loc:
        df.loc[message_id, 'lang_in'] = lic
        df.loc[message_id, 'lang_out'] = loc
        df.to_csv(base_lang_name, sep=';', encoding='cp1251', index='id')

    if message_id in df.index:
        result = (df.loc[message_id, 'lang_in'], df.loc[message_id, 'lang_out'])
    else:
        result = (Languages.lang_in, Languages.lang_out)
    return result


def pronounce(text, message_id):
    """ транслитерация текста """
    transliteration_text = text[2]
    if transliteration_text:
        BotManager.get_bot().send_message(message_id, text=f'Произношение:\n{transliteration_text}')
