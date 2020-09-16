import config
import logs
import data
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

def set_tasks(update, context):
    """Хочу установить задачу"""
    reply_keyboard = [['Андрей', 'Ирина']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Кому?', reply_markup=markup)
    return "username"

def get_name(update, context):
    """
        Вход: Для кого задача
        Выход: Тип задачи
    """
    context.user_data['username'] = update.message.text

    reply_keyboard = [['Mounth_task', 'Week_task'],['Day_task', 'Rememeber']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Какое?', reply_markup=markup)
    return "type"

def get_task_type(update, context):
    context.user_data['type'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что?')
    return "description"

def get_description(update, context):
    context.user_data['description'] = update.message.text

    text = str(context.user_data['type']) + " = " + str(context.user_data['description'])

    logs.create_log(datetime.now(), update._effective_user.username, context.user_data['username'], text)

    data.task(context.user_data['username'],context.user_data['type'], context.user_data['description'])

    markup = ReplyKeyboardMarkup(config.main_keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ok', reply_markup=markup)
    return ConversationHandler.END