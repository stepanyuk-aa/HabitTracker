import config
import data
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(filename='logs.txt', format='%(asctime)s,%(message)s', level=logging.INFO)

def correct(data):
    st = ""
    for w in data:
        st += w + ":\t" + str(data[w]) + "\n"

    print(st)
    return st

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_markup=markup)

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

    context.bot.send_message(chat_id=update.effective_chat.id, text='Чей статус выхотите просмотреть?', reply_markup = whois)

def get_logs(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='2')
def set_points(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='3')

def button(update, context):
    query = update.callback_query.data
    if ('Статус' in query):
        text = query[6:]
        print(update.__dict__)
        print(context.__dict__)
        context.bot.send_message(chat_id=update.effective_chat.id, text=correct(data.read(text)))

start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('caps', caps)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

status_handler = CommandHandler('get_status', get_status)
logs_handler = CommandHandler('get_logs', get_logs)
points_handler = CommandHandler('set_points', set_points)
close_handler = CommandHandler('close_keyboard', close_keyboard)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

dispatcher.add_handler(status_handler)
dispatcher.add_handler(logs_handler)
dispatcher.add_handler(points_handler)
dispatcher.add_handler(close_handler)

reply_keyboard = [['/get_status','/get_logs','/set_points']]
markup = ReplyKeyboardMarkup (reply_keyboard, one_time_keyboard=False)


updater.start_polling()