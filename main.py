# Import local modules ------------------------------------------------------------------------------------------------>
import config           # Get token and other variable
import data             # Get functions for work with database
import logs             # Get functions for create logs
import dialogs.points   # Get dialogs about points
import dialogs.tasks    # Get dialogs about tasks

# Import telegram modules --------------------------------------------------------------------------------------------->
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


# Import other modules ------------------------------------------------------------------------------------------------>
from datetime import datetime
import logging

# Bot initiation  ----------------------------------------------------------------------------------------------------->
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
close_handler = CommandHandler('close_keyboard', close_keyboard)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
# dispatcher.add_handler(echo_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

# Add dialogs  -------------------------------------------------------------------------------------------------------->

# Set points
points_handler = CommandHandler('set_points', dialogs.points.set_points)
dispatcher.add_handler(points_handler)

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Очки'), dialogs.points.set_points)],
    states={
        "username": [MessageHandler(Filters.text, dialogs.points.get_name)],
        "points": [MessageHandler(Filters.text, dialogs.points.get_points)],
        "description": [MessageHandler(Filters.text, dialogs.points.get_description)]
    },
    fallbacks=[]
))


# Set tasks
tasks_handler = CommandHandler('set_tasks', dialogs.tasks.set_tasks)

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Задание'), dialogs.tasks.set_tasks)],
    states={
        "username": [MessageHandler(Filters.text, dialogs.tasks.get_name)],
        "type": [MessageHandler(Filters.text, dialogs.tasks.get_task_type)],
        "description": [MessageHandler(Filters.text, dialogs.tasks.get_description)]
    },
    fallbacks=[]
))

dispatcher.add_handler(status_handler)
dispatcher.add_handler(logs_handler)

dispatcher.add_handler(close_handler)

reply_keyboard = [['/get_status', '/get_logs', 'Задание', 'Очки']]
markup = ReplyKeyboardMarkup(config.main_keyboard, one_time_keyboard=False)

updater.start_polling()
