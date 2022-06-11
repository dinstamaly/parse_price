__author__ = 'Dinmukhamed Stamaliev'

import json

import requests
from config.settings import PROF_INFO
from bs4 import BeautifulSoup


def make_request():
    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    data = {
        'action': 'login',
        'username': PROF_INFO.get('username'),
        'password': PROF_INFO.get('password')
    }
    login_url = 'https://kaspi.kz/merchantcabinet/login'

    s.post(
        url=login_url,
        headers=headers,
        data=data
    )
    return s


def get_difference():
    s = make_request()
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        # 'Content-Type': 'application/json',
        'X-Auth-Token': 'lYKsfVT9UGbRAwVico5QsZHmY88vB87W/YDod7kD95M=',
    }
    product_url = 'https://kaspi.kz/shop/p/sports-research-rybii-zhir-triple-strength-omega-3-fish-oil-30-tabletok-104787250/?c=750000000'
    request = s.get(
        product_url,
        verify=True,
        headers=headers2,

    )
    soup = BeautifulSoup(request.text, 'html.parser')
    items = soup.find_all('td')
    print(items)
    for item in items:
        print(item.get_text())
    return request
#
# def get_difference():
#     s = make_request()
#     headers2 = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
#         'Content-Type': 'application/json',
#         # 'X-Auth-Token': 'lYKsfVT9UGbRAwVico5QsZHmY88vB87W/YDod7kD95M=',
#     }
#     product_url = 'https://kaspi.kz/yml/offer-view/offers/104787250'
#     request = requests.post(
#         product_url,
#         verify=True,
#         headers=headers2,
#         # cookies=s.cookies.get_dict(),
#         data=json.dumps(
#             {
#                 "cityId": "750000000",
#                 "id": "104787250",
#                 # "merchantUID": null,
#                 "limit": 5,
#                 "page": 0,
#                 "sort": True,
#                 "product": {
#                     "brand": "Sports Research",
#                     "categoryCodes":
#                         [
#                             "Vitamins",
#                             "Pharmacy",
#                             "Categories"
#                         ],
#                     "baseProductCodes": [],
#                     "groups": []
#                 },
#                 "installationId": "-1"}
#         )
#
#     )
#     print(request)
#     return request


def get_min_value(index_data, price):
    data = get_difference(index_data)
    data_dict = {}
    temp = 0
    for i in data['offers']:
        if 'eco iherbkz' in i['merchantName']:
            continue
        diff = i['price'] - price
        if diff < temp:
            data_dict['name'] = i['merchantName']
            data_dict['price'] = i['price']
            data_dict['difference'] = abs(diff)
            temp = diff

    return data_dict
