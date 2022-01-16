from telegram import Bot, InlineKeyboardButton
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext
from uplink import Consumer, returns, get
from .buttons import get_register_keyboard, get_base_reply_keyboard
from .config import TG_TOKEN
import requests
import qrcode


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать! Пожалуйста, авторизуйтесь для продолжения.',
                              reply_markup=get_register_keyboard())


def about(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='О приложении')


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Помощь')


def sendRequest():
    response = requests.get('http://localhost:8002/api/branches/').json()
    return response


# Оброботка клавиатуры
def establishments(update: Update, context: CallbackContext):
    branches = ''
    for i in loyaltyapi.get_repos('branches'):
        branches += f'Название {i["name"]}\n' \
                    f'Aдрес: {i["address"]}\n' \
                    f'{i["description"]}\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=branches, )


# оброботчик кнопки новостей
def news(update: Update, context: CallbackContext):
    articles = ''
    for i in loyaltyapi.get_repos('articles'):
        articles += f'{i["time_created"][:10]}\n' \
                    f'{i["title"]}\n' \
                    f'{i["text"]}\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=articles, )


def awards(update: Update, context: CallbackContext):
    response = loyaltyapi.get_repos(f'users/{update.effective_user.id}/progress')
    user_rewards_reply = ""
    for i in range(int(response['program'])):
        if i < int(response['completed_orders']):
            user_rewards_reply += '❤️‍🔥 '
        else:
            user_rewards_reply += "🤍 "
    user_rewards_reply += f"\n\nНеобходимо заказов для получения награды: " \
                          f"{int(response['program']) - int(response['completed_orders'])}.\n\n" \
                          f"Доступно наград: {response['active_rewards']}."
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_rewards_reply, )


def register(update: Update, context: CallbackContext):
    if update.message.contact.user_id == update.message.chat_id:
        url = 'http://localhost:8002/api/users/create/'
        data = {'phone': update.message.contact.phone_number.replace('+', ''),
                'tg_id': update.message.contact.user_id,
                'first_name': update.message.contact.first_name,
                'last_name': update.message.contact.last_name}
        response = requests.post(url, data=data)
        generate_qr(update, update.message.contact)
        if str(response.status_code).startswith('2'):
            reply_text = 'Вы успешно авторизованы.'
        else:
            reply_text = response.text
    else:
        reply_text = 'Пожалуйста, укажите данные своего аккаунта.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_markup=get_base_reply_keyboard())


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    update.message.reply_text(
        text=f"{text}"
    )


def generate_qr(update, contact):
    phone_number = contact.phone_number.replace('+', '')
    img = qrcode.make(phone_number)
    img.save(f'temp/qr/{update.message.chat_id}.png')


def display_qr(update, context):
    with open(f'temp/qr/{update.message.chat_id}.png', 'rb') as qr_png:
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=qr_png,
                              caption='Покажите ваш QR-код кассиру.')


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

    # handler Для клавиатуры

    establishments_handler = MessageHandler(Filters.regex('Заведения'), establishments)
    updater.dispatcher.add_handler(establishments_handler)

    news_handler = MessageHandler(Filters.regex('Новости'), news)
    updater.dispatcher.add_handler(news_handler)

    awards_handler = MessageHandler(Filters.regex('Мои награды'), awards)
    updater.dispatcher.add_handler(awards_handler)

    qr_handler = MessageHandler(Filters.regex('QR код'), display_qr)
    updater.dispatcher.add_handler(qr_handler)

    register_handler = MessageHandler(Filters.contact & (~Filters.command), register)
    updater.dispatcher.add_handler(register_handler)

    updater.start_polling()
    updater.idle()


class LoyaltyApi(Consumer):
    @returns.json
    @get("{path}/")
    def get_repos(self, path):
        pass


loyaltyapi = LoyaltyApi(base_url="http://localhost:8002/api/")

if __name__ == '__main__':
    main()
