import asyncio
# import logging
# import random
import os
import re
import schedule
import requests

from datetime import datetime
from dotenv import load_dotenv

from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, URLInputFile

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# from handler import is_instagram_reels_url, download_reels, db_path_remove_lines, db_path_get_url
# from lib.AG_caption_list import caption_list
# from lists import caption_list

load_dotenv()
token = os.environ.get('BOT_TOKEN_AG')
group_id = os.environ.get('GROUP_ID_AG')
db_path = r"lib/links_AG.txt"

# service = Service(executable_path="/home/tg_bot/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

bot = Bot(token=token)
dp = Dispatcher()


# checking instagram link
def instagram_reels_url(url) -> bool:
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


# get last lines from DB and move to first line
def db_get_urls():
    print('db path update')
    with open(db_path, 'r') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)
        lines.insert(0, last_line)

    with open(db_path, 'w') as f:
        f.writelines(lines)

        return last_line


# get last lines from DB only
def db_get_last_url_only():
    with open(db_path, 'r') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)

        return last_line


# get video
def get_video_src(url) -> str:
    url = db_get_urls()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    reel_source = element.get_attribute('src')

    return reel_source


# get video by bs4 - (!) improvements needed / html.parser search doesn't work
def get_video_src_bs4():
    url = db_get_last_url_only()

    headers = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                    'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    soup.find("video")


# get discription from video
def get_discription():
    # url = 'https://www.instagram.com/reel/C4iOAtroTD6/'
    url = db_get_last_url_only()

    headers = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                    'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    title = soup.title.string.split('|')[0]

    return title


# test command
@dp.message(Command('q'))
async def print_desc(msg: Message):
    print(get_discription())


# test command
@dp.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer('Привет')


# test command
@dp.message(Command('Hi'))
async def send_video(msg: Message):
    async def job():
        await msg.answer('Aloha')

    schedule.every(5).seconds.do(lambda: asyncio.create_task(job()))

    while True:
        await asyncio.sleep(0.1)
        schedule.run_pending()


# main command
@dp.message(Command('op'))
async def cmd_start_bot(msg: Message):
    print('bot started')
    current_datetime = datetime.now().strftime('%H:%M')
    await bot.send_message(msg.chat.id, f'Bot started at {current_datetime}')

    async def job():
        msg_caption = get_discription()
        current_datetime = datetime.now().strftime('%H:%M')

        # get src and download video
        video_src = get_video_src(msg.text)
        video_file = URLInputFile(video_src)

        try:
            # send video to group
            await bot.send_video(group_id, video_file, caption=msg_caption, width=1080, height=720)
            await bot.send_message(msg.chat.id, f'Video send to AG group at {current_datetime}')
            print(f'Video send to AG {group_id} at {current_datetime}')

        except Exception as e:
            await bot.send_message(msg.chat.id, f'Failed to send to AG group at {current_datetime}')
            print(f'Failed to send to AG {group_id} at {current_datetime}')

        except TimeoutException:
            await bot.send_message(msg.chat.id, "Unable to download")

    # schedule for run a bot for sending videos
    # schedule.every(30).minutes.do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("17:00").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("17:21").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("17:52").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("22:49").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("22:30").do(lambda: asyncio.create_task(job()))

    # await job()
    while True:
        await asyncio.sleep(0.1)
        schedule.run_pending()


# test command run main bot 1 time
@dp.message(Command('test'))
async def cmd_test(msg: Message):
    print('bot started to send video 1 time')

    msg_caption = get_discription()
    current_datetime = datetime.now().strftime('%H:%M')

    # get src ang download video
    video_src = get_video_src(msg.text)
    video_file = URLInputFile(video_src)

    try:
        # send video to group
        await bot.send_video(group_id, video_file, caption=msg_caption, width=1080, height=720)
        await bot.send_message(msg.chat.id, f'Video send to AG group at {current_datetime}')
        print(f'Video send to AG {group_id} at {current_datetime}')

    except Exception as e:
        await bot.send_message(msg.chat.id, f'Failed to send to AG group at {current_datetime}')
        print(f'Failed to send to AG {group_id} at {current_datetime}')

    except TimeoutException:
        await bot.send_message(msg.chat.id, "Unable to download")


# TODO Сделать проверку на нерабочую ссылку
# https://www.instagram.com/reel/C2a0lqwoKFO/?igsh=YWsxbnJtOHllMnB4


# get url video from bot (admin send url) and save to DB
@dp.message()
async def save_url_to_list(msg: Message):
    if not instagram_reels_url(msg.text):
        await msg.answer("The given URL is not valid")
    else:
        with open(db_path, "a") as file:
            # print(msg) - info about user
            msg_url = msg.text
            file.write(msg_url + '\n')
        await msg.answer("Link received and write to DB")
        print('Link received and write to LIST')


# @dp.message(Command('cap'))
# async def cap(msg: Message):
#     photo = png.png
#     await bot.send_photo(msg.chat.id, caption="caption!!!")


# @dp.message(F.text == 'Как дела?')
# async def zbs(msg: Message):
# await msg.answer("ZBS")


async def task(msg: Message):
    await bot.send_message(msg.chat.id, "/op")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

# TODO нет решения. Ошибка при простое.
# Failed to fetch updates - TelegramConflictError: Telegram server says - Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
# Sleep for 1.000000 seconds and try again... (tryings = 0, bot id = 7067956532)
