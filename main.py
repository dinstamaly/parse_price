__author__ = 'Dinmukhamed Stamaliev'

import io

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
import json

from config.settings import driver
from mailing import send_email_file
from menu import main_menu_keyboard
from report import get_report_file
from service import make_request, get_difference


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Добро пожалоавть, {username}".format(
            username=update.effective_user.first_name \
                if update.effective_user.first_name is not None \
                else update.effective_user.username),
        reply_markup=main_menu_keyboard()
    )


def make_json_file():
    s = make_request()
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Content-Type': 'application/json',
    }
    product_url = 'https://kaspi.kz/merchantcabinet/api/offer'
    request = s.post(
        product_url,
        headers=headers2,
        cookies=s.cookies.get_dict(),
        data=json.dumps({
            'offerStatus': "ACTIVE",
            'start': 0,
            'count': 200
        })

    )
    with open('my_product.json', 'w', encoding='utf-8') as my_json:
        json.dump(request.json(), my_json, ensure_ascii=False, indent=4)
    return request.json()


def demping(update: Update, context: CallbackContext):
    data = make_json_file()
    update.message.reply_text(f'Подождите 5 мин, проводится операция')
    file = get_report_file(data['offers'])
    with open('ExcelFormatTemplate.xlsx', 'wb') as f:
        f.write(file)

    context.bot.sendDocument(
        update.effective_chat.id,
        document=open('ExcelFormatTemplate.xlsx', 'rb')
    )


# data = make_json_file()
# send_email_file(
#     file_attachment=get_report_file(data['offers']),
#     file_name='ExcelFormatTemplate',
#     subject='product',
#     send_to='dinstamaly@gmail.com',
#     text='test'
# )
# driver.quit()
updater = Updater('5498775460:AAHfpZkhhKAyWxPW_31m_W2zH6_y-ghdAAs')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'(a?Демпинг)'), demping))

updater.start_polling()
updater.idle()