from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON1_ESTABLISHMENTS = 'Заведения'
BUTTON2_NEWS = 'Новости'
BUTTON3_AWARDS = 'Мои награды'
BUTTON4_SETTINGS = 'Настройки'
BUTTON5_QR = 'QR код'



def get_base_reply_keyboard():
    keyboard =[
          [KeyboardButton(BUTTON1_ESTABLISHMENTS), KeyboardButton(BUTTON2_NEWS)],
          [KeyboardButton(BUTTON3_AWARDS), KeyboardButton(BUTTON4_SETTINGS)],
          [KeyboardButton(BUTTON5_QR)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )