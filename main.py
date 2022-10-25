from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from random import seed
from random import random
from menus import Menu
from db.engine import session
from db.models import User,Items
from datetime import datetime
import telebot
from steps import Steps
import callbacks
from telebot import types
from setup import bot

class Markup(object):
    def __init__(self,*params):
        self.params = params
    def make_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for param in self.params:
            if param:
                markup.add(param)
        return markup





@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = Markup('Меню').make_markup()
    bot.send_message(message.chat.id, "привет хуйло", parse_mode='html',reply_markup= markup)
@bot.message_handler(content_types=['text'])
def bot_msg(message):
    if message.chat.type == 'private':
        menu(message)

def menu(message):
    keyboard = types.InlineKeyboardMarkup()
    profile = types.InlineKeyboardButton(f'Профиль', callback_data='profile')
    items = types.InlineKeyboardButton(f'Товары', callback_data='items')
    orders = types.InlineKeyboardButton(f'Мои покупки', callback_data='orders')
    keyboard.add(profile)
    keyboard.add(items)
    keyboard.add(orders)

    bot.send_message(message.chat.id, text='Выберите', parse_mode='html', reply_markup=keyboard)


bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапуск бота"),
    telebot.types.BotCommand("/help", "Помощь"),
    telebot.types.BotCommand("/profile", "Профиль")

])
bot.infinity_polling()

