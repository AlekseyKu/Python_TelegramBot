import re
import requests as r
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


def is_instagram_reels_url(url) -> bool:
    """
    Check the url is instagram reels url?
    :param url: instagram reels url
    :return: bool
    """
    pattern = r"https?://(?:www\.)?instagram\.com/reel/.*"
    match = re.match(pattern, url)
    if match:
        return True
    return False


def download_reels(url) -> bytes:
    """
    Download reels video

    :param url: instagram reels url
    :return: bytes
    """
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    reel_source = element.get_attribute('src')

    return r.get(reel_source).content


# def download_info_from_reels(text) -> str:
#     driver.get(text)
#     wait = WebDriverWait(driver, 10)
#     element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                          '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[19]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/span/text()')))
#     reel_source = element.get_attribute('text')
#     print(reel_source)
#
#     return r.get(reel_source).text