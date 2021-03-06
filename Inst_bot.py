from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
import requests


class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver/chromedriver")

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))
        time.sleep(2)
        username_input = browser.find_element(by=By.NAME, value='username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)
        password_input = browser.find_element(by=By.NAME, value='password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    def element_exists(self,type_object, object):
        browser = self.browser
        if type_object == 'xpath':
            try:
                browser.find_element(by=By.XPATH, value=object)
                exist = True
            except NoSuchElementException:
                exist = False
            return exist
        elif type_object == 'class':
            try:
                browser.find_element(by=By.CLASS_NAME, value=object)
                exist = True
            except Exception as ex:
                print(ex)
                exist = False
            return exist
        elif type_object == 'css':
            try:
                browser.find_element(by=By.CSS_SELECTOR, value=object)
                exist = True
            except NoSuchElementException:
                exist = False
            return exist

    def like_by_link(self, url):
        browser = self.browser
        browser.get(url)
        if self.element_exists('xpath', '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div/h2'):
            print(f'{url}    ?? ??????????????????, ?????? ???????????????? ????????????????????.')
            self.close_browser()
        else:
            time.sleep(3)
            browser.find_element(by=By.XPATH,
                                 value='/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()

    def get_all_posts(self):
        browser = self.browser
        if self.element_exists('xpath', '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div/h2'):
            print(f'?? ??????????????????, ?????? ???????????????? ????????????????????.')
            self.close_browser()
        else:
            time.sleep(random.randrange(3, 5))
            number_posts = int(''.join(browser.find_element(by=By.CLASS_NAME, value='_ac2a').text.split(',')))
            for i in range(number_posts // 12 + 1):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            hrefs = browser.find_elements(by=By.TAG_NAME, value='a')
            post_urls = set([i.get_attribute('href') for i in hrefs if '/p/' in i.get_attribute('href')])
            return post_urls

    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)
        post_urls = self.get_all_posts()
        for url in post_urls:
            print(url)
            try:
                self.like_by_link(url)
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def like_all_photo_user(self, nickname):
        browser = self.browser
        browser.get(f'https://www.instagram.com/{nickname}/')
        post_urls = self.get_all_posts()
        for url in post_urls:
            print(url)
            try:
                self.like_by_link(url)
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def follow_by_url(self, nickname):
        browser = self.browser
        browser.get(f'https://www.instagram.com/{nickname}/')
        time.sleep(random.randrange(3, 5))
        if self.element_exists('xpath', '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div/h2'):
            print(f'???????????????????????? ?? ?????????? {nickname} ???? ????????????????????')
            self.close_browser()
        elif self.element_exists('xpath', '//div[text()="???????????? ??????????????????"]'):
            print(f'?????? ???????????????? ?????????????? ???? ?????? ?????????????????? ???????????? ???? ???????????????? ???? {nickname}')
            self.close_browser()
        elif self.element_exists('xpath', '//a[text()="?????????????????????????? ??????????????"]'):
            print(f'?????? ?????? ??????????????')
            self.close_browser()
        elif self.element_exists('css', 'svg[aria-label="????????????????"]'):
            print(f'???? ?????? ?????????????????? ???? {nickname}')
            self.close_browser()
        else:
            browser.find_element(by=By.XPATH, value='//div[text()="??????????????????????"]').click()
            time.sleep(random.randrange(2, 4))
            
#need to add saving video content
    def save_content_by_url(self, url):
        all_content_urls= []
        browser = self.browser
        browser.get(url)
        time.sleep(random.randrange(2, 4))
        if self.element_exists('css', 'button[aria-label="??????????"]'):
            num = 0
            for _ in browser.find_elements(by=By.CLASS_NAME, value='_acnb'):
                num += 1
            for img in browser.find_elements(by=By.CLASS_NAME, value='_aagt')[0:num]:
                all_content_urls.append(img.get_attribute('src'))
                time.sleep(1)
        else:
            all_content_urls.append(browser.find_elements(by=By.CLASS_NAME, value='_aagt')[0].get_attribute('src'))
        for content in all_content_urls:
            request = requests.get(content)
            with open(f'data/{content.split("/")[5].split(".")[0]}_img.jpg', 'wb') as img_file:
                img_file.write(request.content)
        self.close_browser()
        
my_bot = InstagramBot(username, password)
my_bot.login()
