import config
import data
import logging
import logs
from datetime import datetime

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(filename='logs.txt', format='%(asctime)s,%(message)s', level=logging.INFO)


def correct(data):
    st = ""
    for w in data:
        st += w + ":\t" + str(data[w]) + "\n"

    return st


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!",
                             reply_markup=markup)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    logging.info(text_caps)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def close_keyboard(update, context):
    update.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())


def get_status(update, context):
    whois = [[
        InlineKeyboardButton("Андрей", callback_data="СтатусАндрей"),
        InlineKeyboardButton("Ирина", callback_data="СтатусИрина")
    ]]
    whois = InlineKeyboardMarkup(whois)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Кого?', reply_markup=whois)


def get_logs(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='2')


def set_points(update, context):
    reply_keyboard = [['Андрей', 'Ирина']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Кому?', reply_markup=markup)
    return "username"

def get_name(update, context):
    context.user_data['username'] = update.message.text

    reply_keyboard = [['-3', '-2','-1'],['1','2','3']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Сколько?', reply_markup=markup)
    return "points"

def get_points(update, context):
    context.user_data['points'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text='За что?')
    return "description"

def get_description(update, context):
    context.user_data['description'] = update.message.text
    text = "Points " + str(context.user_data['points']) + " for " + str(context.user_data['description'])

    logs.create_log(datetime.now(), update._effective_user.username, context.user_data['username'], text)

    data.scope(context.user_data['username'],context.user_data['points'])

    reply_keyboard = [['/get_status', '/get_logs', 'Установить очки']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ok', reply_markup=markup)
    return ConversationHandler.END

def button(update, context):
    query = update.callback_query.data
    if ('Статус' in query):
        user = query[6:]
        context.bot.send_message(chat_id=update.effective_chat.id, text=correct(data.read(user)))


start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('caps', caps)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

status_handler = CommandHandler('get_status', get_status)
logs_handler = CommandHandler('get_logs', get_logs)
points_handler = CommandHandler('set_points', set_points)
close_handler = CommandHandler('close_keyboard', close_keyboard)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
# dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Установить очки'), set_points)],
    states={
        "username": [MessageHandler(Filters.text, get_name)],
        "points": [MessageHandler(Filters.text, get_points)],
        "description": [MessageHandler(Filters.text, get_description)]
    },
    fallbacks=[]
))

dispatcher.add_handler(status_handler)
dispatcher.add_handler(logs_handler)
dispatcher.add_handler(points_handler)
dispatcher.add_handler(close_handler)

reply_keyboard = [['/get_status', '/get_logs', 'Установить очки']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

updater.start_polling()
