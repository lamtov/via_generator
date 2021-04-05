from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import io, json, os
import time
import platform
from fake_useragent import UserAgent
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import staleness_of
NEW_PAGE_LOAD_PAUSE_TIME = 1
AFTER_RANDOM_CLICK_ANDSCROLL_PAUSE_TIME = 2
BUTTON_CLICK_PAUSE_TIME = 1
SCROLL_PAUSE_TIME = 0.01
def wait_for_page_load(browser, timeout=30):
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )
def init_driver(_proxy, _change_agent):
    chrome_options = Options()
    if _proxy is not None and _proxy != "0.0.0.0:0":
        PROXY = _proxy.replace('\n', '')
        print(PROXY)
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
    if _change_agent == True:
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("ignore-certificate-errors")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument("--window-size=1920x1080")
    if 'ubuntu' in platform.platform().lower() or 'linux' in platform.platform().lower():
        print('using ubuntu or linux')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        cur_dir = os.getcwd()
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=cur_dir + "/window_driver" + "/chromedriver.exe")
        print(driver.execute_script("return navigator.userAgent;"))
    return driver

class Bot():
    def __init__(self, _proxy, link_spam, ):
        try:
            self.browser = init_driver(_proxy, True)
            self.status = 'init'
            self.link_spam = link_spam
        except Exception as e:
            print(e)
            self.status = str(traceback.format_exc())
    def spam_click_on_gesty(self):
        pass
    def spam_click_and_scroll(self):
        pass
    def spam(self):
        try:
            self.browser.get(self.link_spam)
            self.status = 'OK'
        except Exception as e:
            print(str(e))
    def set_link_spam(self,link_spam):
        self.link_spam=link_spam
    def spam_theverge_com(self):
        list_user_comment=set()
        author_name=""
        try:
            self.browser.get(self.link_spam)
            self.status = 'OK'
            try:
                number_comment=WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '''//em[@class='count']''')))
                count=int(number_comment.text)
                # print(count)
                if count>0:
                    try:
                        btn_show_comment = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '''//a[contains(text(),'Read them.')]
                    ''')))
                        btn_show_comment.click()
                        find_comment = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '''//div[@class='comment comment_inner']
                    ''')))
                    except:
                        pass
            except:
                pass
            page_source = self.browser.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            try:
                author_name = soup.find('a', class_='author fn').text
            except:
                pass
            list_div_comment = soup.findAll('div', class_='username')

            for div_comment in list_div_comment:
                try:
                    if len(div_comment.contents) > 0 and div_comment.contents[0].name == 'a':
                        list_user_comment.add(div_comment.contents[0].text)
                except:
                    pass
            return  list_user_comment, author_name
        except Exception as e:
            print(e)
            print(self.link_spam)
            print(str(e))
            return list_user_comment, author_name
    def spam_etsy_com(self):
        list_user_review=set()
        try:
            self.browser.get(self.link_spam)
            self.status = 'OK'

            is_Continue=True
            page=0
            while is_Continue is True:
                try:
                    page=page+1
                    btn_show_comment = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '''//a[@class='page-{0} text-decoration-none']'''.format(str(page)))))
                    btn_show_comment.click()
                    time.sleep(0.3)

                    try:
                        WebDriverWait(self.browser, 3).until(ec.visibility_of_element_located(
                        (By.XPATH, '''//p[@class='shop2-review-attribution']''')))
                    except:
                        pass
                    page_source = self.browser.page_source
                    soup = BeautifulSoup(page_source, 'lxml')
                    try:
                        list_div_review = soup.findAll('p', class_='shop2-review-attribution')
                        for div_review in list_div_review:
                            try:
                                if (len(div_review.contents) > 0 and div_review.contents[0].name == 'a') or (len(div_review.contents) > 1 and div_review.contents[1].name == 'a') :
                                    if div_review.contents[0].name == 'a':
                                        list_user_review.add(div_review.contents[0].text)
                                    else:
                                        list_user_review.add(div_review.contents[1].text)
                            except:
                                pass
                    except:
                        pass
                except:
                    is_Continue=False
            return list_user_review
        except:
            print(self.link_spam)
            return list_user_review

import os.path

if __name__ == "__main__":
    link_spam = "https://www.etsy.com/shop/souslamansarde#reviews"
    proxy = '0.0.0.0:0'

    t = Bot(proxy, link_spam)
    # t.spam_etsy_com()
    print(t.spam_etsy_com())




