import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from components.exception import ModeException


class Browser:
    """class for create webdriver"""

    company_found: bool
    in_windows: bool

    def __init__(self, mode: str, proxy: dict):
        if mode == 'window':
            options = webdriver.ChromeOptions()

            # set proxy
            proxy_str = proxy.get('ip') + ':' + proxy.get('port')
            options.add_argument('--proxy-server=%s' % proxy_str)

            self.driver = webdriver.Chrome(options=options)
            self.in_windows = True
        elif mode == 'docker':
            # set options for browser in background
            options = FirefoxOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-gpu")

            # run background browser
            self.driver = webdriver.Firefox(
                options=options
            )
            self.in_windows = False
        else:
            raise ModeException()


class ReviewsTwoGis:
    """class for work with reviews"""

    review_class = None

    def __init__(self, browser: Browser):
        self.browser = browser
        time.sleep(1)

    def get_reviews_btn(self):
        """get btn for click"""

        return self.browser.driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value='Отзывы'
        )

    def get_count_reviews(self):
        count = self.browser.driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value='Отзывы'
        ).text

        return int(count[6:])

    def get_class_review(self, count_review):
        """get class of review"""

        time.sleep(count_review / 10 + 1)

        '''
        scroll_elem = self.browser.driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value='Отзывы'
        ).find_element(by=By.XPATH, value='./../../../../../../..')
        class_parent = scroll_elem.get_attribute('class')

        class_review = self.browser.driver.execute_script("return document.querySelector('." + class_parent + "')"
                                                          ".children.item(document.querySelector('"
                                                          "." + class_parent + "')"
                                                          ".children.length - 1).children"
                                                          ".item(document.querySelector('." + class_parent + "')"
                                                          ".children.item(document.querySelector('"
                                                          "." + class_parent + "')"
                                                          ".children.length - 1).children.length - 1).className")
                                                          
        '''

        return '_11gvyqv'

    def scroll_reviews(self, count_review):
        """scroll all reviews for get it"""

        # scroll to start
        scroll_script = ("let a; for (let i of document.querySelectorAll('a')) {"
                         " if (i.innerText.slice(0, 6) "
                         "=== 'Отзывы') { a = i; }}"
                         "let scroll_elem = a.parentElement.parentElement.parentElement.parentElement"
                         ".parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;"
                         "scroll_elem.scrollTo({left: 0, top: scroll_elem.scrollHeight, behavior: 'smooth'}); "
                         "let height = 0;"
                         "function scrollThis() {"
                         "scroll_elem.scrollTo({left: 0, top: scroll_elem.scrollHeight, behavior: 'smooth'});"
                         "if (scroll_elem.scrollHeight !== height) {"
                         "height = scroll_elem.scrollHeight;" 
                         "setTimeout(scrollThis, 1000); }}"
                         "setTimeout(scrollThis, 1000);")

        self.browser.driver.execute_script(scroll_script)

        time.sleep(count_review / 10 + 1)

        # scroll to the end
        scroll_script = ("let a; for (let i of document.querySelectorAll('a')) {"
                         " if (i.innerText.slice(0, 6) "
                         "=== 'Отзывы') { a = i; }} "
                         "a.scrollIntoView()")

        self.browser.driver.execute_script(scroll_script)

        # get response from company
        getting_script = "for (let i of document.querySelectorAll('._j1il10')) { i.click()}"
        self.browser.driver.execute_script(getting_script)

    def is_response(self, class_review, number):
        """it is response from company or no"""

        try:
            inner_test = self.browser.driver.execute_script("return document.querySelectorAll"
                                                            "('." + class_review + "')"
                                                            "[" + str(number) + "].children"
                                                            ".item(2).children[2]"
                                                            ".children.item(0).children.item(1)"
                                                            ".children.item(1).innerText")

        except selenium.common.exceptions.JavascriptException:
            return False

        if 'официальный ответ' in inner_test:
            return True

        return False

    def get_reviews(self, class_review, repeat=False):
        """print all reviews"""

        reviews = []

        tags = self.browser.driver.find_elements(
            by=By.CSS_SELECTOR, value=('.' + class_review)
        )

        b = 1
        for i in tags:
            # control repeat or no
            if repeat and (b == 31):
                break

            a = i.find_element(by=By.CSS_SELECTOR, value='a')
            review_text = a.text

            review_text = self.browser.driver.execute_script(
                "return document.querySelectorAll('." + class_review + "')[" + str(b-1) + "].querySelector('a').innerText"
            )

            # work with name
            for_name = 0
            for j in i.find_elements(by=By.CSS_SELECTOR, value='span'):
                name_elem = j

                if for_name == 1:
                    break
                else:
                    for_name += 1

            review_name = name_elem.text

            review_name = self.browser.driver.execute_script("return document.querySelectorAll"
                                                             "('." + class_review + "')[" + str(b-1) +
                                                             "].querySelectorAll('span')[1]"
                                                             ".innerText")

            # work with date
            date_elem = name_elem.find_element(by=By.XPATH, value='./../..') \
                .find_element(by=By.CSS_SELECTOR, value='div')

            review_date = date_elem.text
            review_date = self.browser.driver.execute_script("return document.querySelectorAll('." + class_review + "')"
                                                             "[" + str(b -1) + "].querySelectorAll('span')"
                                                             "[1].parentElement.parentElement"
                                                             ".querySelector('div').innerText")

            # work with rating
            class_parent_rating = name_elem.find_element(by=By.XPATH, value='./../../../..') \
                .get_attribute('class')

            rating = self.browser.driver.execute_script("return document.querySelectorAll"
                                                        "('." + class_parent_rating + "')"
                                                        "[" + str(b - 1) + "].children"
                                                        ".item(document.querySelectorAll"
                                                        "('._o7qbud')[0].children.length - 1)"
                                                        ".children.item(0).children.item(0)"
                                                        ".querySelectorAll('span').length")

            review_rating = rating

            # work with response
            length_response = self.browser.driver.execute_script("return document.querySelectorAll"
                                                                 "('." + class_review + "')"
                                                                 "[" + str(b - 1) + "].children.item(2)"
                                                                 ".children.length")

            # init company response
            review_response = None
            review_response_text = None

            if (int(length_response) > 2) and self.is_response(class_review, b - 1):
                answer = True
                try:
                    company_response = self.browser.driver.execute_script("return document.querySelectorAll"
                                                                          "('." + class_review + "')"
                                                                          "[" + str(b - 1) + "].children"
                                                                          ".item(2).children[2]"
                                                                          ".querySelector('span').innerText")

                except selenium.common.exceptions.JavascriptException:
                    company_response = self.browser.driver.execute_script("return document.querySelectorAll"
                                                                          "('." + class_review + "')"
                                                                          "[" + str(b - 1) + "].children"
                                                                          ".item(2).children[3]"
                                                                          ".querySelector('span').innerText")

                try:
                    text_response = self.browser.driver.execute_script("return document.querySelectorAll"
                                                                       "('." + class_review + "')"
                                                                       "[" + str(b - 1) + "].children"
                                                                       ".item(2).children.item(2)"
                                                                       ".children.item(0).children"
                                                                       ".item(2).innerText")

                except selenium.common.exceptions.JavascriptException:
                    text_response = self.browser.driver.execute_script("return document.querySelectorAll"
                                                                       "('." + class_review + "')"
                                                                       "[" + str(b - 1) + "].children"
                                                                       ".item(2).children.item(3)"
                                                                       ".children.item(0).children"
                                                                       ".item(2).innerText")


                review_response = company_response
                review_response_text = text_response

            else:
                answer = False

            b += 1
            reviews.append({
                'author': review_name,
                'rating': review_rating,
                'date': review_date,
                'text': review_text,
                'answer_text': review_response_text,
                'answer': answer
            })

        return reviews
