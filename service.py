__author__ = 'Dinmukhamed Stamaliev'

import json

import requests
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import PROF_INFO, driver


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


def upload_file():
    s = make_request()
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Content-Type': 'application/json',
    }
    product_url = 'https://kaspi.kz/merchantcabinet/api/offer/upload'
    request = s.post(
        product_url,
        headers=headers2,
        cookies=s.cookies.get_dict(),
        # data=json.dumps(
        #     {
        #         "cityId": "750000000",
        #         "id": "100883228",
        #         # "merchantUID":null,
        #         "limit": 5,
        #         "page": 0,
        #         "sort": True,
        #         "product": {
        #             "brand": "California Gold Nutrition",
        #             "categoryCodes": [
        #                 "Vitamins",
        #                 "Pharmacy",
        #                 "Categories"
        #             ],
        #             "baseProductCodes": [],
        #             "groups": []
        #         },
        #         "installationId": "-1"}
        # )

    )
    print(request.text)
    return request


def get_difference(url):
    driver.get(url + '?c=750000000')
    print(url)
    try:
        a1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//tr[1]//td[@class='sellers-table__cell']//a"))
        )
        a2 = driver.find_element_by_xpath(
            ".//tr[1]//td[@class='sellers-table__cell']//div[@class='sellers-table__price-cell-text']")

        rows = driver.find_elements_by_xpath(
            "//table[@class='sellers-table__self']/tbody/tr")

        if len(rows) >= 2:
            if 'eco iherbkz' in a1.text:
                a3 = driver.find_element_by_xpath(
                    ".//tr[2]//td[@class='sellers-table__cell']//a")
                a4 = driver.find_element_by_xpath(
                    ".//tr[2]//td[@class='sellers-table__cell']//div[@class='sellers-table__price-cell-text']")
                a4 = a4.text.replace(' ', '')
                return a3.text, float(a4[:-1])
        a2 = a2.text.replace(' ', '')
        return a1.text, float(a2[:-1])
    except TimeoutException:
        print('time out')


def get_min_value(url, price):
    name, _price = get_difference(url)
    data_dict = {}
    diff = _price - price
    if 'eco iherbkz' in name or diff in [0, 1]:
        return data_dict
    # if _price < price:
    data_dict['name'] = name
    data_dict['price'] = _price
    data_dict['difference'] = diff

    return data_dict
