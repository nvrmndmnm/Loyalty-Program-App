from webbrowser import get

# import returns as returns
from telegram import Bot, InlineKeyboardButton
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext

from uplink import Consumer ,returns, get

from buttons import *

from config import TG_TOKEN


def about(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Приложение LoyaltyBot позволяет получать бесплатные товары за покупки",reply_markup=get_base_reply_keyboard())


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='для получения бонусов просто приходите в заведение и сканируйте QR-код')

# def echo(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text,)


# Оброботка клавиатуры
def establishments(update: Update, context: CallbackContext):
    branches = ''
    for i in loyaltyapi.get_repos('branches'):
        branches += f'Название {i["name"]}\n' \
                    f'Aдресс: {i["address"]}\n' \
                    f'{i["description"]}\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=branches,)



def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(TG_TOKEN, use_context=True)

    about_handler = CommandHandler('about', about)
    help_handler = CommandHandler('help', help)
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(about_handler)
    updater.dispatcher.add_handler(help_handler)
    # updater.dispatcher.add_handler(echo_handler)

    #handler Для клавиатуры
    establishments_handler = MessageHandler(Filters.text & (~Filters.command), establishments)
    updater.dispatcher.add_handler(establishments_handler)

    updater.start_polling()
    updater.idle()

class LoyaltyApi(Consumer):
    @returns.json
    @get("{path}/")
    def get_repos(self, path):
        pass

loyaltyapi = LoyaltyApi(base_url="http://localhost:8000/api/")


loyaltyapi.get_repos('branches')


if __name__ =='__main__':
    main()
