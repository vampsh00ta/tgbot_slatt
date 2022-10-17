from db.engine import session
from db.models import User,Items
from datetime import datetime
from telebot import types
from setup import bot
from steps import Steps

steps = Steps(bot)
@bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'deposit')
def deposit(data):
    msg = bot.send_message(data.message.chat.id, """\
   Введите сумму
    """)
    bot.register_next_step_handler(msg, steps.deposit_step)
@bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'item')
def purchase(data):
    msg = bot.send_message(data.message.chat.id, """\
     Введите количество
      """)
    item_id = data.data.split('_')[1]
    item = session.query(Items).filter(Items.id == f"{item_id}").all()[0]

    bot.register_next_step_handler(msg, steps.amount_purchase,item)
    # message = f'Вы купили {item.name}'
    # bot.send_message(data.message.chat.id, text=message, parse_mode='HTML')

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
