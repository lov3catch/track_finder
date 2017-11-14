# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters, BaseFilter

from core.adv.controller import send_adv
from core.area.models import Area
from core.handlers.decorators import save_chanel_decorator, save_download_decorator
from core.handlers.finder import parse_result, normalize_song_name, normalize_download_url
from core.handlers.messages import Messages

messages = Messages()

BOTONARIOUM = '::Ботонариум::'


# def _build_botonarioum_keyboard(bot, update):
#     area = Area.get(Area.token == bot.area.token)
#     if (area.language in ('RU')):
#         buttons = [[BOTONARIOUM]]
#         keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#         bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)


def build_download_keyboard(songs_data):
    download_buttons = []
    for title, url in songs_data:
        inline_download_button = InlineKeyboardButton(title, callback_data=url)
        download_buttons.append([inline_download_button])
    return download_buttons


@save_chanel_decorator
def send_botonarioum_info(bot, update):
    print('ok1')
    message = 'Ботонариум - вселенная, где обитают боты.'
    print('ok2')
    button = [[InlineKeyboardButton('Присоединиться', url='https://t.me/botonarioum')]]
    print('ok3')
    return bot.send_message(update.message.chat.id, message, reply_markup=InlineKeyboardMarkup(button))


class BotonarioumFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text == BOTONARIOUM)


@save_chanel_decorator
def search_audio(bot, update):
    messages.set_language(bot.area.language)
    try:
        bot.send_message(update.message.chat.id, messages.get_massage('searching'))
        songs_data = parse_result(normalize_song_name(update.message.text))
        songs_data = list(filter(None, songs_data))

        buttons = build_download_keyboard(songs_data)
        keyboard = InlineKeyboardMarkup(buttons)

        if buttons:
            bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
        else:
            bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    except Exception as ex:
        print(ex)


@save_chanel_decorator
def send_info(bot, update):
    messages.set_language(bot.area.language)
    message = messages.get_massage('intro')
    # area = Area.get(Area.token == bot.area.token)
    # if (area.language in ('RU')):
    #     buttons = [[BOTONARIOUM]]
    #     keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    #     return bot.send_message(update.message.chat.id, message, reply_markup=keyboard)
    return bot.send_message(update.message.chat.id, message)


@save_chanel_decorator
@save_download_decorator
def download_song(bot, update, *args, **kwargs):
    messages.set_language(bot.area.language)
    query = update.callback_query
    download_url = normalize_download_url(query.data)
    bot.send_audio(query.message.chat_id, download_url)
    send_adv(bot, query.message.chat_id, messages)


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(BotonarioumFilter(), send_botonarioum_info))
    dispatcher.add_handler(MessageHandler(Filters.text, search_audio))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    return dispatcher
