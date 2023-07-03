from selenium import webdriver
from selenium.webdriver.common.by import By

from components.components import Browser, ReviewsTwoGis


def work_with_browser(browser_obj: Browser):
    """use methods ReviewsTwoGis"""

    # get reviews
    reviews_obj = ReviewsTwoGis(browser_obj)

    btn = reviews_obj.get_reviews_btn()
    btn.click()

    # get count of reviews
    count_reviews = reviews_obj.get_count_reviews()

    # scroll reviews
    reviews_obj.scroll_reviews()

    # get class of reviews
    review_class = reviews_obj.get_class_review(count_reviews)

    # get class of review
    reviews_obj.get_reviews(review_class)


if __name__ == '__main__':
    # get id of firm
    firm_id = input()

    # go to page
    browser = Browser(mode='window')
    browser.driver.get('https://2gis.ru/firm/' + firm_id)

    # work with browser
    work_with_browser(browser)

    # quit from browser
    browser.driver.quit()
