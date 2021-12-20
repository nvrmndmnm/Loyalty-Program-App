from telegram import Bot, InlineKeyboardButton
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext

from config import TG_TOKEN

def about(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Приложение LoyaltyBot позволяет получать бесплатные товары за покупки")

def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Для получения бонусов просто приходите в заведение и сканируйте QR код")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    bot = Bot(
        token = TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    about_handler = CommandHandler('about', about)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(about_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
if __name__ =='__main__':
    main()

# создание клавиатуры
def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

# список кнопок
