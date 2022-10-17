from db.engine import session
from db.models import User,Items
from datetime import datetime
from telebot import types

class Steps(object):
    def __init__(self,bot):
        self.bot = bot
    def buttons(self):
        keyboard = types.InlineKeyboardMarkup()
        profile = types.InlineKeyboardButton(f'Профиль', callback_data='profile')
        items = types.InlineKeyboardButton(f'Товары', callback_data='items')
        keyboard.add(profile)
        keyboard.add(items)
        return  keyboard
    def deposit_step(self,message):
        print(message.text)
        try:
            user_id = message.from_user.id
            user = session.query(User).filter(User.username == f"{user_id}").all()[0]
            user.balance += int(message.text)
            session.commit()

            balance = types.InlineKeyboardButton(f'{user.balance} рублей| Пополнить', callback_data='deposit')
            back = types.InlineKeyboardButton(f'Назад', callback_data='back_profile')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(balance)
            keyboard.add(back)
            self.bot.send_message(message.chat.id, text='Баланс пополнен', parse_mode='html')
            self.bot.send_message(message.chat.id, text='Профиль', parse_mode='html', reply_markup=keyboard)
        except Exception as e:
            keyboard = self.buttons()
            self.bot.send_message(message.chat.id, text='Меню', parse_mode='html', reply_markup=keyboard)
    def amount_purchase(self,message,item):
        try:
            amount = int(message.text)
            item.amount-=amount

            user_id = message.from_user.id
            user = session.query(User).filter(User.username == f"{user_id}").all()[0]
            keyboard = self.buttons()
            if user.balance >=amount*item.price:

                user.balance-=amount*item.price

                msg = f'Вы купили {item.name} в количестве {amount}'
                f = open(f"1234.txt", "rb")
                keyboard = types.InlineKeyboardMarkup()
                profile = types.InlineKeyboardButton(f'Профиль', callback_data='profile')
                items = types.InlineKeyboardButton(f'Товары', callback_data='items')

                keyboard.add(profile)
                keyboard.add(items)

                session.commit()

                self.bot.send_document(message.chat.id,f)
                self.bot.send_message(message.chat.id, text=msg, parse_mode='HTML', reply_markup=keyboard)

            else:
                self.bot.send_message(message.chat.id, text='ты нищий ебанат', parse_mode='HTML', reply_markup=keyboard)


            # self.bot.send_document(message.chat.id, f)
        except Exception as e:
            keyboard = types.InlineKeyboardMarkup()
            profile = types.InlineKeyboardButton(f'Профиль', callback_data='profile')
            items = types.InlineKeyboardButton(f'Товары', callback_data='items')
            keyboard.add(profile)
            keyboard.add(items)
            self.bot.send_message(message.chat.id, text='Меню', parse_mode='html', reply_markup=keyboard)
