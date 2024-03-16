import re
import requests as r
import schedule
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

db_path = r"lib/links_AG.txt"


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


def download_reels(url) -> str:
    url = db_path_get_url()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    reel_source = element.get_attribute('src')

    return reel_source
    # return r.get(reel_source).content


def db_path_get_url():
    # get last lines
    with open(db_path, 'r') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)
        lines.insert(0, last_line)

    with open(db_path, 'w') as f:
        f.writelines(lines)

        return last_line


def db_path_remove_lines():
    with open(db_path, 'r+') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)
        lines.insert(0, last_line)

    with open(db_path, 'w') as f:
        f.writelines(lines)


def get_url(url):
    driver.get(url)
    return url
