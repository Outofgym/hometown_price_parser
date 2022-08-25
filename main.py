from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc

from bs4 import BeautifulSoup
import requests
from time import sleep




ZILLOW_ENDPOINT = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
                  '%22mapBounds%22%3A%7B%22west%22%3A-122.50871658325195%2C%22east%22%3A-122.41464614868164%2C' \
                  '%22south%22%3A37.6929897806257%2C%22north%22%3A37.74757548736077%7D%2C%22mapZoom%22%3A14%2C' \
                  '%22regionSelection%22%3A%5B%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A' \
                  '%7B%22min%22%3A0%2C%22max%22%3A451971%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B' \
                  '%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A2000%7D%2C%22ah%22%3A%7B' \
                  '%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
                  '%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A' \
                  '%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue' \
                  '%7D'

GOOGLE_FORM = 'https://forms.gle/QeEfSvVog31jpNbw9'
GOOGLE_SPREADSHEET = 'https://docs.google.com/forms/d/1jzQrMGWHZxwtYn-5sfpEXXpvg84lDgJfEGzMHT_5zWs/edit#responses'
GOOGLE_LOGIN_PAGE = 'https://accounts.google.com/ServiceLogin/identifier?elo=1&flowName=GlifWebSignIn&flowEntry' \
                    '=ServiceLogin '
GOOGLE_LOGIN = 'login\n'
GOOGLE_PASSWORD = 'passwordgit \n'


class JobAutomation:
    def __init__(self):
        self.driver = None
        self.hometowns_links = []
        self.hometowns_addreses = []
        self.hometowns_prices = []
        self.address_filed = None
        self.price_field = None
        self.link_field = None
        self.send_button = None

    def get_hometowns(self):
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
                   'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
                   }
        response = requests.get(ZILLOW_ENDPOINT, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_articles = soup.find_all('article')
        for article in all_articles:

            try:
                self.hometowns_prices.append(article.find('div', class_='list-card-price').text)
                self.hometowns_links.append(article.a['href'])
                self.hometowns_addreses.append(article.address.text)

            except TypeError:
                continue
            except AttributeError:
                continue

    def check_links(self):
        start = 'https://www.zillow.com'
        for link_index, link in enumerate(self.hometowns_links):
            if not link.startswith('https'):
                self.hometowns_links[link_index] = start + link
        print(self.hometowns_links)

    def find_form_element(self):
        self.address_filed = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[2]/div[1]'
                                                                '/div/div/div[2]/div/div[1]/div/div[1]/input')
        self.price_field = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[2]/div['
                                                              '2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        self.link_field = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[2]/div['
                                                             '3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        self.send_button = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[3]/div['
                                                              '1]/div[1]/div')

    def full_google_form(self):
        self.driver.get(GOOGLE_FORM)
        sleep(5)

        for item_index, item in enumerate(self.hometowns_prices):
            self.find_form_element()
            sleep(2)
            self.address_filed.send_keys(self.hometowns_addreses[item_index])
            self.price_field.send_keys(item)
            self.link_field.send_keys(self.hometowns_links[item_index])
            self.send_button.click()
            sleep(2)
            one_more_answer_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            one_more_answer_button.click()
            sleep(3)

    def login_google_account(self):
        self.driver = uc.Chrome(use_subprocess=True)
        self.driver.get(GOOGLE_LOGIN_PAGE)
        username = self.driver.find_element(By.NAME, 'identifier')
        username.send_keys(GOOGLE_LOGIN)

        sleep(3)

        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys(GOOGLE_PASSWORD)
        sleep(5)

    def create_spreadsheet(self):
        self.driver.get(GOOGLE_SPREADSHEET)
        sleep(3)
        spreadsheet_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div['
                                                                '1]/div[1]/div[2]/div[1]/div/div')
        spreadsheet_button.click()
        sleep(3)

        create_button = self.driver.find_element(By.XPATH, '/html/body/div[9]/div/div[2]/div[3]/div[2]')
        create_button.click()


bot = JobAutomation()
bot.get_hometowns()
bot.check_links()
bot.login_google_account()
bot.full_google_form()
bot.create_spreadsheet()
