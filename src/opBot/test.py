# with open("links.txt", "r+") as file:
#     lines = file.readlines()
#     first_line = lines[0]
#     print(first_line)
#     file.writelines(first_line)
#     lines = lines[:0]


# with open('links.txt', 'r+') as f:
#     lines = f.readlines()
#     last_line = lines[-1]
#     lines.pop(-1)
#     print(last_line)

# with open('links.txt', 'r+') as f:
#     lines = f.readlines()
#     last_line = lines.pop(-1)
#     print(last_line)
#     lines.insert(0, last_line)
#
# with open('links.txt', 'w') as f:
#     f.writelines(lines)

db_path = r"lib/links_AG.txt"

with open(db_path, 'r') as f:
    lines = f.readlines()
    last_line = lines[-1]
    print(last_line)



import asyncio
import logging
import random
import os
import schedule

from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, URLInputFile
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException

from handler import is_instagram_reels_url, download_reels, db_path_remove_lines, \
    db_path_get_url
from lib.AG_caption_list import caption_list
from lists import caption_list

token = os.environ.get('BOT_TOKEN_AG')
group_id = os.environ.get('GROUP_ID_AG')
db_path = r"lib/links_AG.txt"

bot = Bot(token=token)
dp = Dispatcher()
load_dotenv()


@dp.message(Command('go'))
async def go(msg: Message):
    await msg.answer('Привет')


# @dp.message(Command('Hi'))
# async def send_video(msg: Message):
#     async def job():
#         await msg.answer('Aloha')
#
#     schedule.every(5).seconds.do(lambda: asyncio.create_task(job()))
#
#     while True:
#         await asyncio.sleep(0.1)
#         schedule.run_pending()


@dp.message(CommandStart())
async def cmd_start(msg: Message):
    print('bot started')

    async def job():
        msg_caption = random.choice(caption_list)
        current_datetime = datetime.now()

        # get src ang download video
        video_src = download_reels(msg.text)
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

    # schedule.every(20).seconds.do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("10:00").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("15:00").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("20:00").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("00:00").do(lambda: asyncio.create_task(job()))
    schedule.every().day.at("04:00").do(lambda: asyncio.create_task(job()))

    while True:
        await asyncio.sleep(0.1)
        schedule.run_pending()


@dp.message()
async def save_url_to_list(msg: Message):
    if not is_instagram_reels_url(msg.text):
        await msg.answer("The given URL is not valid")
    else:
        with open(db_path, "a") as file:
            # print(msg) - info about user
            msg_url = msg.text
            file.write(msg_url + '\n')
        await msg.answer("Link received and write to DB")
        print('Link received and write to LIST')


# @dp.message(F.text == 'Как дела?')
# async def zbs(msg: Message):
# await msg.answer("ZBS")

@dp.message(Command('test'))
async def cmd_test(msg: Message):
    print('bot started')

    msg_caption = random.choice(caption_list)
    current_datetime = datetime.now()

    # get src ang download video
    video_src = download_reels(msg.text)
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


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

