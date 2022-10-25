from db.engine import session
from db.models import User,Items,Orders,Orders_items
from datetime import datetime
from telebot import types
from cryptopayment.crypto import  EthModule
import os
from dotenv import load_dotenv
import threading
load_dotenv()
class Steps(EthModule):

    def __init__(self,bot,httpprovider,api_key,base_url,wallet,waiting_time):
        super(self.__class__,self).__init__(httpprovider,api_key,base_url,wallet,waiting_time)
        self.bot = bot
    def buttons(self):
        keyboard = types.InlineKeyboardMarkup()
        profile = types.InlineKeyboardButton(f'Профиль', callback_data='profile')
        items = types.InlineKeyboardButton(f'Товары', callback_data='items')
        orders = types.InlineKeyboardButton(f'Покупки', callback_data='orders')
        keyboard.add(profile)
        keyboard.add(items)
        keyboard.add(orders)

        return  keyboard

    def crypto_pay(self,message):
        try:
            fiat_amount = int(message.text)

            crypto_amount = self.convertFiat(fiat_amount)
            msg = f"""
                Для успешного пополнения отправьте ровно {crypto_amount} ETH на указанный ниже кошелек в течение {self.waiting_time} минут
            """
            self.bot.send_message(message.chat.id, text=msg, parse_mode='html')
            self.bot.send_message(message.chat.id, text=self.wallet, parse_mode='html')

            checking_deposit = threading.Thread(target=self.send_reuslt_as_complete_ctypto,args = (message,crypto_amount,fiat_amount))
            checking_deposit.start()

        except Exception as e:
            print(e)
    def send_reuslt_as_complete_ctypto(self,message,crypto_amount,fiat_amount):
        deposited = self.checkDeposit(deposit=crypto_amount)
        if deposited:
            user_id = message.from_user.id
            user = session.query(User).filter(User.username == f"{user_id}").all()[0]
            user.balance +=fiat_amount
            session.commit()
            session.flush()
            self.bot.send_message(message.chat.id, text="Ваш кошелек успешно пополнен", parse_mode='html')
        else:
            self.bot.send_message(message.chat.id, text="Время для депозита искекло", parse_mode='html')

    def card_pay(self,message):
        try:
            amount = int(message.text)
            user_id = message.from_user.id
            user = session.query(User).filter(User.username == f"{user_id}").all()[0]
            user.balance += amount

            session.commit()
            session.flush()
            print(message.text)

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
        amount = int(message.text)
        item.amount-=amount

        user_id = message.from_user.id
        user = session.query(User).filter(User.username == f"{user_id}").all()[0]
        keyboard = self.buttons()
        if user.balance >=amount*item.price:

            user.balance-=amount*item.price
            order = Orders(date=datetime.now(), user_id=user.id)
            session.add(order)
            session.flush()
            session.refresh(order)

            order_items = Orders_items(order_id = order.id,quantity = amount,item_id = item.id)
            session.add(order_items)
            session.flush()





            msg = f'Вы купили {item.name} в количестве {amount}'
            f = open(f"1234.txt", "rb")
            keyboard = self.buttons()

            session.commit()

            self.bot.send_document(message.chat.id,f)
            self.bot.send_message(message.chat.id, text=msg, parse_mode='HTML', reply_markup=keyboard)

        else:
            self.bot.send_message(message.chat.id, text='ты нищий ебанат', parse_mode='HTML', reply_markup=keyboard)


        # self.bot.send_document(message.chat.id, f)

