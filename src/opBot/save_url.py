import asyncio
import os
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

from handler import is_instagram_reels_url, download_reels, get_url
from lists import caption_list

load_dotenv()

token = os.environ.get('BOT_TOKEN_AG')
bot = Bot(token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot=bot)


@dp.message_handler()
# Get & save url to list from user
async def save_url_to_list(msg: types.Message):
    msg_caption = random.choice(caption_list)
    if not is_instagram_reels_url(msg.text):
        await bot.send_message(msg.chat.id, "The given URL is not valid")
    else:
        with open("links.txt", "a") as file:
            # print(msg) - info about user
            msg_url = msg.text
            file.write(msg_url + '\n')
        await bot.send_message(msg.chat.id, "Please wait! Processing the video...")
        print('Link received and write to LIST')


# Get url from list & send download video & send to group
async def send_message(msg: types.Message):

    await bot.send_message(msg.chat.id, "1")
    await asyncio.sleep(3)
    await bot.send_message(msg.chat.id, "2")


async def main():
    async with asyncio.TaskGroup() as tg:
        msg = types.Message()
        tg.create_task(save_url_to_list(msg))
        tg.create_task(send_message(msg))

#asyncio.run(main())
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
