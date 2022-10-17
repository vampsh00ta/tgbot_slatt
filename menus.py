from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Menu(object):
    def main_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
                    [InlineKeyboardButton('Option 2', callback_data='m2')],
                    [InlineKeyboardButton('Option 3', callback_data='m3')]]
        return InlineKeyboardMarkup(keyboard)

    def first_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                    [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
                    [InlineKeyboardButton('Main menu', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    def second_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                    [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                    [InlineKeyboardButton('Main menu', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    def main_menu(self,update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text=self.main_menu_message(),
            reply_markup=self.main_menu_keyboard())

    def first_menu(self,update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text=self.first_menu_message(),
            reply_markup=self.first_menu_keyboard())

    def second_menu(self,update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text=self.second_menu_message(),
            reply_markup=self.second_menu_keyboard())

    # and so on for every callback_data option
    def first_submenu(bot, update):
        pass

    def second_submenu(bot, update):
        pass