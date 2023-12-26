import time
from selenium import webdriver
from components.components import ReviewsTwoGis, Browser


def get_all_reviews(work_browser: Browser):
    """view reviews from 2gis page"""

    # get reviews
    reviews_obj = ReviewsTwoGis(work_browser)

    # get count of reviews
    count_reviews = reviews_obj.get_count_reviews()

    # scroll reviews
    reviews_obj.scroll_reviews(count_reviews) # сделать тут перенос класса

    # get class of reviews
    review_class = reviews_obj.get_class_review(count_reviews)

    # get class of review
    return reviews_obj.get_reviews(review_class)


def get_some_reviews(work_browser: Browser):
    """get 30 last reviews"""

    # get reviews
    reviews_obj = ReviewsTwoGis(work_browser)

    # get count of reviews
    count_reviews = reviews_obj.get_count_reviews()

    # scroll reviews
    reviews_obj.scroll_reviews(count_reviews)

    # get class of reviews
    review_class = reviews_obj.get_class_review(count_reviews)

    # get class of review
    return reviews_obj.get_reviews(review_class, repeat=True)


def load_page(yandex_url, proxy: dict, repeat: bool):
    """go to page"""

    browser = Browser('window', proxy)

    # go to page
    browser.driver.get(yandex_url + '/tab/reviews')
    # browser.driver.get('https://2gis.ru/voronezh/firm/4363390419993111/39.185236%2C51.655844/tab/reviews?m=39.188158%2C51.6563%2F16.78')
    time.sleep(5)

    # control repeat and get reviews

    if not repeat:
        reviews = get_some_reviews(browser)
    else:
        reviews = get_all_reviews(browser)

    browser.driver.quit()
    # display.stop()

    return reviews
