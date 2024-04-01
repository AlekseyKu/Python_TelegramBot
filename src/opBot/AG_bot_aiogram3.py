import asyncio
import logging
import random
import os
import re
import schedule

from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, URLInputFile

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


from handler import is_instagram_reels_url, download_reels, db_path_remove_lines, \
    db_path_get_url
from lib.AG_caption_list import caption_list
from lists import caption_list

load_dotenv()
token = os.environ.get('BOT_TOKEN_AG')
group_id = os.environ.get('GROUP_ID_AG')
db_path = r"lib/links_AG.txt"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

bot = Bot(token=token)
dp = Dispatcher()



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

def download_instagram_reels(url) -> str:
    url = db_path_get_url()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    reel_source = element.get_attribute('src')

    return reel_source

def db_path_get_urls():
    # get last lines
    with open(db_path, 'r') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)
        lines.insert(0, last_line)

    with open(db_path, 'w') as f:
        f.writelines(lines)

        return last_line

@dp.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer('Привет')


@dp.message(Command('Hi'))
async def send_video(msg: Message):
    async def job():
        await msg.answer('Aloha')

    schedule.every(5).seconds.do(lambda: asyncio.create_task(job()))

    while True:
        await asyncio.sleep(0.1)
        schedule.run_pending()


@dp.message(Command('op'))
async def cmd_start_bot(msg: Message):
    print('bot started')

    async def job():
        msg_caption = random.choice(caption_list)
        current_datetime = datetime.now().strftime('%H:%M')

        # get src ang download video
        video_src = download_instagram_reels(msg.text)
        video_file = URLInputFile(video_src)

        try:
            await bot.send_video(msg.chat.id, video_file)
            # db_path_remove_lines()

            print('db path update')

            try:
                await bot.send_video(group_id, video_file)
                print(f'Video send to AG {group_id} at {current_datetime}')
            except Exception as e:
                print(f'Failed to send to AG {group_id} at {current_datetime}')

        except TimeoutException:
            await bot.send_message(msg.chat.id, "Unable to download")

    # schedule.every(1).minutes.do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("17:48").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("13:41").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("22:22").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("22:49").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("22:30").do(lambda: asyncio.create_task(job()))

    while True:
        await asyncio.sleep(0.1)
        schedule.run_pending()


@dp.message(Command('test'))
async def cmd_test(msg: Message):
    print('bot started to send video 1 time')

    msg_caption = random.choice(caption_list)
    current_datetime = datetime.now()

    # get src ang download video
    video_src = download_instagram_reels(msg.text)
    video_file = URLInputFile(video_src)

    try:
        await bot.send_video(msg.chat.id, video_file)
        # db_path_remove_lines()

        print('db path update')

        try:
            # send video to group
            await bot.send_video(group_id, video_file, caption=msg_caption)
            print(f'Video send to AG {group_id} at {current_datetime}')
        except Exception as e:
            print(f'Failed to send to AG {group_id} at {current_datetime}')

    except TimeoutException:
        await bot.send_message(msg.chat.id, "Unable to download")


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
    await bot.send_message(msg.chat.id, "task")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

# нет решения
# Failed to fetch updates - TelegramConflictError: Telegram server says - Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
# Sleep for 1.000000 seconds and try again... (tryings = 0, bot id = 7067956532)
