from telegram import Bot, InlineKeyboardButton
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext

from uplink import Consumer ,returns, get

from buttons import *

from config import TG_TOKEN
import requests


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать в нашего бота-шмота! Пожалуйста, авторизуйтесь для продолжения.',
                              reply_markup=get_register_keyboard())


def about(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=do_echo(update, context),
                             reply_markup=get_register_keyboard()
                             )


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=sendRequest(),
                             reply_markup=get_register_keyboard()
                             )


def sendRequest():
    response = requests.get('http://localhost:8002/api/branches/').json()
    return response
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



def register(update: Update, context: CallbackContext):
    if update.message.contact.user_id == update.message.chat_id:
        url = 'http://localhost:8002/api/users/create/'
        data = {'phone': update.message.contact.phone_number.replace('+', ''),
                'tg_id': update.message.contact.user_id}
        response = requests.post(url, data=data)
        print(response.text)
        resp = response.text
    else:
        resp = 'Пожалуйста, укажите данные своего аккаунта.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=resp, reply_markup=get_base_reply_keyboard())


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    update.message.reply_text(
        text=f"Yo {text}"
    )


def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(TG_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    about_handler = CommandHandler('about', about)
    help_handler = CommandHandler('help', help)
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(about_handler)
    updater.dispatcher.add_handler(help_handler)
    # updater.dispatcher.add_handler(echo_handler)

    #handler Для клавиатуры
    establishments_handler = MessageHandler(Filters.text & (~Filters.command), establishments)
    updater.dispatcher.add_handler(establishments_handler)

    register_handler = MessageHandler(Filters.contact & (~Filters.command), register)
    updater.dispatcher.add_handler(register_handler)

    updater.start_polling()

    updater.idle()

class LoyaltyApi(Consumer):
    @returns.json
    @get("{path}/")
    def get_repos(self, path):
        pass

loyaltyapi = LoyaltyApi(base_url="http://localhost:8000/api/")


loyaltyapi.get_repos('branches')


if __name__ == '__main__':
    main()


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    print(buttons)
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
