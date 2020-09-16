import config
import logs
import data
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


def correct(data):
    st = ""
    for w in data:
        st += w + ":\t" + str(data[w]) + "\n"

    return st


def get_status(update, context):
    reply_keyboard = [['Андрей', 'Ирина']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Кому?', reply_markup=markup)
    return "username"

def return_status(update, context):
    context.user_data['username'] = update.message.text

    markup = ReplyKeyboardMarkup(config.main_keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text=correct(data.read(context.user_data['username'])), reply_markup=markup)

    return ConversationHandler.END

