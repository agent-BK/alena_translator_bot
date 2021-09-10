from data.private_chanel_data import ChanelData


class ChannelText:
    title_url_href = 'подписаться на канал Алена бот переводчик'
    text_welcome = 'Здраствуйте {0}!\nПереводчик заработает сразу после ' + u'\U0001F449' \
        f'<a href="{ChanelData.url}" title="{title_url_href}">подписки</a> на наш канал {ChanelData.id} '\
        + u'\U0001F44D\n\nКанал не будет вас беспокоить, он нужен чтобы переводчик находили новые ' \
        u'пользователи.\n\n\U0001F514' + f'<a href="{ChanelData.url}" title="{title_url_href}">Подпишитесь</a> и ' \
        f'вы можете отправлять мне сообщения для перевода'
