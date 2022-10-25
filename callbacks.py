from db.engine import session
from db.models import User,Items,Orders
from datetime import datetime
from telebot import types
from setup import bot
from steps import Steps
import os
from dotenv import load_dotenv
load_dotenv()


steps = Steps(bot=bot,httpprovider = os.getenv('HTTP_PROVIDER'),
                base_url=os.getenv('API_ETH_BASE_URL'),
                api_key=os.getenv('ETH_API_KEY'),
                wallet = os.getenv('ETH_WALLET'),
                waiting_time = os.getenv('WAITING_TIME'))


@bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'card')
def card(data):
    msg = bot.send_message(data.message.chat.id, """\
   Введите сумму
    """)
    bot.register_next_step_handler(msg, steps.card_pay)

@bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'deposit')
def deposit(data):
    keyboard = types.InlineKeyboardMarkup()
    crypto = types.InlineKeyboardButton(f'Криптовалюта', callback_data='crypto')
    card = types.InlineKeyboardButton(f'Картой', callback_data='card')

    keyboard.add(crypto)
    keyboard.add(card)

    bot.send_message(data.message.chat.id, text='Выберите способ оплаты', parse_mode='html', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda callback: callback.data == 'crypto')
def crypto(data):
    msg = bot.send_message(data.message.chat.id, """\
   Введите сумму
    """)
    bot.register_next_step_handler(msg, steps.crypto_pay)
@bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'item')
def purchase(data):
    msg = bot.send_message(data.message.chat.id, """\
     Введите количество
      """)
    item_id = data.data.split('_')[1]
    item = session.query(Items).filter(Items.id == f"{item_id}").all()[0]

    bot.register_next_step_handler(msg, steps.amount_purchase,item)


@bot.callback_query_handler(func=lambda callback: callback.data == 'profile')
def profile(data):
    user_id = data.from_user.id
    result = session.query(User).filter(User.username == f"{user_id}").all()
    print(len(result))
    if len(result) == 0:
        query = User(username=user_id, fullname=data.from_user.username, date=datetime.now())
        session.add(query)


        user = session.query(User).filter(User.username == f"{user_id}").all()[0]
        user.balance = 0
        session.commit()

    else:
        user = result[0]




    balance = user.balance
    keyboard = types.InlineKeyboardMarkup()
    balance = types.InlineKeyboardButton(f'{balance} рублей| Пополнить', callback_data='deposit')
    back = types.InlineKeyboardButton(f'Назад', callback_data='back_profile')

    keyboard.add(balance)
    keyboard.add(back)

    bot.send_message(data.message.chat.id, text='Выберите', parse_mode='html', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data == 'items')
def items(data):
    keyboard = types.InlineKeyboardMarkup()
    get_all_items = session.query(Items).all()
    for product in get_all_items:
        if product.amount > 0:
            button = types.InlineKeyboardButton(f'{product.name} | {product.price} рублей | {product.amount} доступно ' ,
                                                callback_data=f'item_{product.id}')
            keyboard.add(button)

    bot.send_message(data.message.chat.id, text='Товары', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data == 'orders')
def orders(data):
    user_id = data.from_user.id
    user = session.query(User).filter(User.username == f"{user_id}").all()[0]
    keyboard = types.InlineKeyboardMarkup()
    if user.orders:
        for order in user.orders:
            price = int(order.orders_items[0].items.price) * int(order.orders_items[0].quantity)
            keyboard.add(types.InlineKeyboardButton(f'Общая сумма: {price} | Дата {order.date}', callback_data=f'{order.id}'))
        back = types.InlineKeyboardButton(f'Назад', callback_data=f'back_profile')
        keyboard.add(back)
        bot.send_message(data.message.chat.id,text='История заказов',reply_markup=keyboard)
    else:
        slatt = types.InlineKeyboardButton(f'У вас нет покупок', callback_data=f'no_ordees')
        keyboard.add(slatt)
        bot.send_message(data.message.chat.id, text='История заказов', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data.split("_")[0] == 'order')
def full_order(data):
    user_id = data.from_user.id
    user = session.query(User).filter(User.username == f"{user_id}").all()[0]
    keyboard = types.InlineKeyboardMarkup()
    if user.orders:
        for order in user.orders:
            price = int(order.orders_items[0].items.price) * int(order.orders_items[0].quantity)
            keyboard.add(types.InlineKeyboardButton(f'Общая сумма: {price} | Дата {order.date}', callback_data=f'{order.id}'))
        back = types.InlineKeyboardButton(f'Назад', callback_data=f'back_profile')
        keyboard.add(back)
        bot.send_message(data.message.chat.id,text='История заказов',reply_markup=keyboard)
    else:
        slatt = types.InlineKeyboardButton(f'У вас нет покупок', callback_data=f'no_ordees')
        keyboard.add(slatt)
        bot.send_message(data.message.chat.id,text='История заказов',reply_markup=keyboard)
