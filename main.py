# Import local modules ------------------------------------------------------------------------------------------------>
import config           # Get token and other variable
import data             # Get functions for work with database
import logs             # Get functions for create logs
import dialogs.tasks    # Get dialogs about tasks
import dialogs.points   # Get dialogs about points
import dialogs.status   # Get dialogs about status

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


# Functions  ---------------------------------------------------------------------------------------------------------->
# Initiate dialog with bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!",
                             reply_markup=markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Get logs
def get_logs(update, context):
    tmp = logs.read_log(); text = ""
    for w in tmp[0]:
        text += w
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

logs_handler = CommandHandler('get_logs', get_logs)
dispatcher.add_handler(logs_handler)


# Add dialogs  -------------------------------------------------------------------------------------------------------->

# Set points
# points_handler = CommandHandler('set_points', dialogs.points.set_points)
# dispatcher.add_handler(points_handler)

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
# tasks_handler = CommandHandler('set_tasks', dialogs.tasks.set_tasks)

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Задание'), dialogs.tasks.set_tasks)],
    states={
        "username": [MessageHandler(Filters.text, dialogs.tasks.get_name)],
        "type": [MessageHandler(Filters.text, dialogs.tasks.get_task_type)],
        "description": [MessageHandler(Filters.text, dialogs.tasks.get_description)]
    },
    fallbacks=[]
))


# Get status
# tasks_handler = CommandHandler('set_tasks', dialogs.tasks.set_tasks)

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Статус'), dialogs.status.get_status)],
    states={
        "username": [MessageHandler(Filters.text, dialogs.status.return_status)]
    },
    fallbacks=[]
))





markup = ReplyKeyboardMarkup(config.main_keyboard, one_time_keyboard=False)

updater.start_polling()
