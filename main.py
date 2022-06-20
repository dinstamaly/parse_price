__author__ = 'Dinmukhamed Stamaliev'

import json

from config.settings import driver
from mailing import send_email_file
from report import get_report_file
from service import make_request, get_difference


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


data = make_json_file()
send_email_file(
    file_attachment=get_report_file(data['offers']),
    file_name='ExcelFormatTemplate',
    subject='product',
    send_to='chikuplusdin@gmail.com',
    text='test'
)
driver.quit()