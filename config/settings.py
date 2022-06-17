import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


dir_path = os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = os.path.join(dir_path, 'chromedriver.exe')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

SMTP = {
    'host': 'smtp.gmail.com',
    'port': 587,
}

MAIL = {
    'username': 'studilimedu@gmail.com',
    'password': 'uaddlvfhddiukgdd',
}

PROF_INFO = {
    'username': "alevtinanur89@gmail.com",
    'password': "T9i9w*k$syv~$m*013"
}