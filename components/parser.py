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
    reviews_obj.scroll_reviews(count_reviews)

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


def work_with_browser(browser_obj):
    """use methods ReviewsTwoGis"""

    # get reviews
    reviews_obj = ReviewsTwoGis(browser_obj)

    btn = reviews_obj.get_reviews_btn()
    btn.click()

    # get count of reviews
    count_reviews = reviews_obj.get_count_reviews()

    # scroll reviews
    reviews_obj.scroll_reviews(count_reviews)

    # get class of reviews
    review_class = reviews_obj.get_class_review(count_reviews)

    # get class of review
    reviews_obj.get_reviews(review_class)


def load_page(yandex_url, proxy: dict, repeat: bool):
    """go to page"""

    browser = Browser('window')

    # go to page
    browser.driver.get(yandex_url + '/tab/reviews')
    time.sleep(5)

    # control repeat and get reviews

    if repeat:
        reviews = get_some_reviews(browser)
    else:
        reviews = get_all_reviews(browser)

    browser.driver.quit()
    # display.stop()

    return reviews
