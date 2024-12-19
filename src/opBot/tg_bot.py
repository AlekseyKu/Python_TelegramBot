import asyncio
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
from selenium.webdriver.common.by import By

load_dotenv()
token_AG = os.environ.get('BOT_TOKEN_AG')
group_id_AG = os.environ.get('GROUP_ID_AG')
db_path_AG = r"lib/links_AG.txt"

token_AW = os.environ.get('BOT_TOKEN_AW')
group_id_AW = os.environ.get('GROUP_ID_AW')
db_path_AW = r"lib/links_AW.txt"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')  # (!) for hosting
driver = webdriver.Chrome(options=options)

# bot = Bot(token=token)
bot_AW = Bot(token=token_AW)
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
    with open(db_path_AW, 'r') as f:
        lines = f.readlines()
        last_line = lines.pop(-1)
        lines.insert(0, last_line)

    with open(db_path_AW, 'w') as f:
        f.writelines(lines)

        return last_line


# get last lines from DB only
def db_get_last_url_only():
    with open(db_path_AW, 'r') as f:
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
    title = soup.title.string.split('\n')[0]
    words_remove = "Instagram"
    for word in words_remove:
        title = title.replace(word, "")

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
    await bot_AW.send_message(msg.chat.id, f'Bot started at {current_datetime}')

    async def job():
        msg_discription = get_discription()
        group_description = '<a href="https://t.me/amaziworld">Amazing World</a>'
        msg_caption = msg_discription + '\n' + group_description
        current_datetime = datetime.now().strftime('%H:%M')

        try:
            # get src and download video
            video_src = get_video_src(msg.text)
            video_file = URLInputFile(video_src)

            try:
                # send video to group AG
                # await bot.send_video(group_id_AG, video_file, caption=msg_caption, width=720, height=1080)
                # await bot.send_message(msg.chat.id, f'Video send to AG group at {current_datetime}')
                # print(f'Video send to AG {group_id_AG} at {current_datetime}')

                # send video to group AW
                await bot_AW.send_video(group_id_AW, video_file, caption=msg_caption, width=720, parse_mode="HTML")
                await bot_AW.send_message(msg.chat.id, f'Video send to AW group at {current_datetime}')
                print(f'Video send to AW {group_id_AW} at {current_datetime}')

            except Exception as e:
                # await bot.send_message(msg.chat.id, f'Failed to send to AG group at {current_datetime}')
                # print(f'Failed to send to AG {group_id_AG} at {current_datetime}')

                await bot_AW.send_message(msg.chat.id, f'Failed to send to AW group at {current_datetime}')
                print(f'Failed to send to AW {group_id_AW} at {current_datetime}')

            except TimeoutException:
                # await bot.send_message(msg.chat.id, "Unable to download")
                await bot_AW.send_message(msg.chat.id, "Unable to download")

        except Exception as e:

            await bot_AW.send_message(msg.chat.id, f'Failed to find video from URL and try again')
            print(f'Failed to find video from URL and try again')

            try:
                await job()
            except Exception as e:
                await bot_AW.send_message(msg.chat.id, f'Failed second time to send to AW group at {current_datetime}')
                print(f'Failed second time to send to AW group at {current_datetime}')

    # schedule for run a bot for sending videos
    # schedule.every(30).minutes.do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("17:00").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("17:21").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("17:52").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("22:49").do(lambda: asyncio.create_task(job()))
    # schedule.every().day.at("22:30").do(lambda: asyncio.create_task(job()))

    await job()
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
        await bot_AW.send_video(group_id_AW, video_file, caption=msg_caption, width=320)
        await bot_AW.send_message(msg.chat.id, f'Video send to AG group at {current_datetime}')
        print(f'Video send to AG {group_id_AW} at {current_datetime}')

    except Exception as e:
        await bot_AW.send_message(msg.chat.id, f'Failed to send to AG group at {current_datetime}')
        print(f'Failed to send to AG {group_id_AW} at {current_datetime}')

    except TimeoutException:
        await bot_AW.send_message(msg.chat.id, "Unable to download")


# get url video from bot (admin send url) and save to DB
@dp.message()
async def save_url_to_list(msg: Message):
    if not instagram_reels_url(msg.text):
        await msg.answer("The given URL is not valid")
    else:
        with open(db_path_AW, "a") as file:
            # print(msg) - info about user
            msg_url = msg.text
            file.write(msg_url + '\n')
        await msg.answer("Link received and write to DB")
        print('Link received and write to LIST')


async def task(msg: Message):
    await bot_AW.send_message(msg.chat.id, "/op")


async def main():
    # await dp.start_polling(bot)
    await dp.start_polling(bot_AW)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
