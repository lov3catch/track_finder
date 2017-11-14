# -*- coding: utf-8 -*-
from core.chanel.models import Chanel
from core.download.models import Download


def save_chanel_decorator(fn):
    def wrapper(bot, update, *args, **kwargs):
        print('SAVE CHANEL')

        try:
            area = bot.area
            if (update.callback_query):
                chat_id = update.callback_query.message.chat.id
                first_name = update.callback_query.message.chat.first_name
                last_name = update.callback_query.message.chat.last_name
            else:
                chat_id = update.message.chat.id
                first_name = update.message.chat.first_name
                last_name = update.message.chat.last_name

            defaults = {'chanel_id': chat_id, 'first_name': first_name, 'last_name': last_name, 'area': area}
            chanel, is_new = Chanel.get_or_create(area=area, chanel_id=chat_id, defaults=defaults)
            print(chanel)
            chanel.update_me()
        except Exception as ex:
            print(ex)

        return fn(bot, update, *args, **kwargs)

    return wrapper


def save_download_decorator(fn):
    def wrapper(bot, update, *args, **kwargs):
        print('SAVE DOWNLOAD')

        try:
            chat_id = update.callback_query.message.chat.id
            chanel_obj = Chanel.get(Chanel.chanel_id == chat_id, Chanel.area == bot.area)
            Download.create(chanel=chanel_obj)
        except Exception as ex:
            print(ex)

        return fn(bot, update, *args, **kwargs)

    return wrapper
