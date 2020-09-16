import config
import logs
import data
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


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

    markup = ReplyKeyboardMarkup(config.main_keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ok', reply_markup=markup)
    return ConversationHandler.END