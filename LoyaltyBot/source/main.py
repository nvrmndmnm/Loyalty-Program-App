import requests
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext
from uplink import Consumer, returns, get, post, Body, json
from buttons import get_register_keyboard, get_base_reply_keyboard
from pathlib import Path
import qrcode
import os
# from dotenv import load_dotenv
# load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
TG_TOKEN = os.getenv('TG_TOKEN')
SITE = os.getenv('TG_SITE')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать! Пожалуйста, авторизуйтесь для продолжения.',
                              reply_markup=get_register_keyboard())


def about(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='О приложении')


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Помощь')


# Обработка клавиатуры
def branches(update: Update, context: CallbackContext):
    branches = ''
    for i in loyaltyAPI.get_request('branches'):
        branches += f'Название {i["name"]}\n' \
                    f'Aдрес: {i["address"]}\n' \
                    f'{i["description"]}\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=branches, )


# Обработчик кнопки новостей
def news(update: Update, context: CallbackContext):
    response = loyaltyAPI.get_request('articles')
    news_reply_message = 'Новостей пока нет, возвращайтесь позже!'
    if response:
        articles = ''
        for i in response:
            articles += f'{i["time_created"][:10]}\n' \
                        f'{i["title"]}\n' \
                        f'{i["text"]}\n\n'
            news_reply_message = articles
    context.bot.send_message(chat_id=update.effective_chat.id, text=news_reply_message, )


def rewards(update: Update, context: CallbackContext):
    response = loyaltyAPI.get_request(f'users/{update.effective_user.id}/progress')
    user_rewards_reply = ""
    # if not str(response.status_code).startswith('2'):
    #     user_rewards_reply = 'Произошла ошибка. Попробуйте отправить запрос снова.'
    if response.get('program'):
        for i in range(int(response['program'])):
            if i < int(response['completed_orders']):
                user_rewards_reply += '❤️‍🔥 '
            else:
                user_rewards_reply += "🤍 "
        user_rewards_reply += f"\n\nНеобходимо заказов для получения награды: " \
                              f"{int(response['program']) - int(response['completed_orders'])}.\n\n" \
                              f"Доступно наград: {response['active_rewards']}."
    else:
        user_rewards_reply = 'У вас пока нет завершённых заказов.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_rewards_reply, )


def register(update: Update, context: CallbackContext):
    if update.message.contact.user_id == update.message.chat_id:
        data = {'phone': update.message.contact.phone_number.replace('+', ''),
                'tg_id': update.message.contact.user_id,
                'first_name': update.message.contact.first_name,
                'last_name': update.message.contact.last_name}
        response = loyaltyAPI.post_request("users/create", **data)
        qr_result = generate_qr(update, update.message.contact)
        if not qr_result:
            reply_text = 'Произошла ошибка, попробуйте повторить регистрацию.'
        else:
            if str(response.status_code).startswith('2'):
                reply_text = 'Вы успешно авторизованы.'
            else:
                reply_text = 'Произошла ошибка.'
    else:
        reply_text = 'Пожалуйста, укажите данные своего аккаунта.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_markup=get_base_reply_keyboard())


def generate_qr(update, contact):
    phone_number = contact.phone_number.replace('+', '')
    # img = qrcode.make(phone_number) # записать в QR-код только номер телефона
    img = qrcode.make(f'{SITE}ru/s/?id={phone_number}')
    try:
        filename = f'{BASE_DIR}/bot/media/qr/{update.message.chat_id}.png'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img.save(filename)
    except Exception as e:
        print(e)
        return False
    return True


def display_qr(update, context):
    try:
        with open(f'{BASE_DIR}/bot/media/qr/{update.message.chat_id}.png', 'rb') as qr_png:
            context.bot.sendPhoto(chat_id=update.message.chat_id, photo=qr_png,
                                  caption='Покажите ваш QR-код кассиру.')
    except IOError:
        reply_text = 'Не удалось загрузить QR-код. Пожалуйста, перезапустите бота командой /start'
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(TG_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))

    about_handler = CommandHandler('about', about)
    updater.dispatcher.add_handler(about_handler)

    help_handler = CommandHandler('help', help)
    updater.dispatcher.add_handler(help_handler)

    branches_handler = MessageHandler(Filters.regex('Заведения'), branches)
    updater.dispatcher.add_handler(branches_handler)

    news_handler = MessageHandler(Filters.regex('Новости'), news)
    updater.dispatcher.add_handler(news_handler)

    rewards_handler = MessageHandler(Filters.regex('Мои награды'), rewards)
    updater.dispatcher.add_handler(rewards_handler)

    qr_handler = MessageHandler(Filters.regex('QR код'), display_qr)
    updater.dispatcher.add_handler(qr_handler)

    register_handler = MessageHandler(Filters.contact & (~Filters.command), register)
    updater.dispatcher.add_handler(register_handler)

    updater.start_polling()
    updater.idle()


class LoyaltyApi(Consumer):
    @returns.json
    @get("{path}/")
    def get_request(self, path):
        print(path)
        pass

    @post("{path}/")
    def post_request(self, path, **body: Body):
        pass


loyaltyAPI = LoyaltyApi(base_url=f"{SITE}api/")

if __name__ == '__main__':
    main()
