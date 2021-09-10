from data.bot_data import BotData
from data.private_data import ChanelData
from utils import function


class BotText:
    welcome = f'Здраствуйте {0}!\nЯ Бот переводчик Алёна версии {BotData.version}.\n\nЯ могу переводить  ' \
        f'текстовые и голосовые сообщения.\n' + function.get_help_text()
    language_input = 'Укажите язык c которого вы хотите получать переводы.\n'
    language_select = 'Выбран язык {0}\nУкажите язык на который вы хотите получать перевод.\n'
    language_not_changed = f'Языки перевода остались прежние\n{0}\u21E8{1}\nЯ Вас внимательно слушаю.'
    not_understand_change_lang = 'Я не понимаю Вас. Пожалуйста выберите язык перевода.'
    languages_selected = 'Отлично. Выбраны языки {0}\u21E8{1}\nДля последущей смены языков просто введите команду ' \
        '/lang и следуйте инструкциям.\nДавайте начнем переводить, я Вас внимательно слушаю.'
    not_understand = 'Я не понимаю Вас. Попробуйте повторить еще раз.'


class ChannelText:
    title_url_href = 'подписаться на канал Алена бот переводчик'
    text_welcome = 'Здраствуйте {0}!\nПереводчик заработает сразу после ' + u'\U0001F449' \
        f'<a href="{ChanelData.url}" title="{title_url_href}">подписки</a> на наш канал {ChanelData.id} '\
        + u'\U0001F44D\n\nКанал не будет вас беспокоить, он нужен чтобы переводчик находили новые ' \
        u'пользователи.\n\n\U0001F514' + f'<a href="{ChanelData.url}" title="{title_url_href}">Подпишитесь</a> и ' \
        f'вы можете отправлять мне сообщения для перевода'
