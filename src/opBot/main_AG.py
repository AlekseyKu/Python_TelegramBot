import telebot
import os
import random
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

from handler import is_instagram_reels_url, download_reels, get_url
from lists import caption_list

load_dotenv()

token = os.environ.get('BOT_TOKEN_AG')
group_id = os.environ.get('GROUP_ID_AG')

bot = telebot.TeleBot(token, parse_mode=None, threaded=False)


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    video = "upload_video"
    msg_caption = random.choice(caption_list)
    if not is_instagram_reels_url(message.text):
        bot.reply_to(message, "The given URL is not valid")
    else:
        bot.send_message(message.chat.id, "Please wait! Processing the video...")
        print('Link received')

        # write url to lists
        text_url = get_url(message.text)
        with open("links.txt", "a") as file:
            file.write(text_url + '\n')

        bot.send_chat_action(message.chat.id, action=video)

        try:
            # downloads reels
            video_file = download_reels(message.text)
            bot.send_video(message.chat.id, video_file)

            print('Video downloaded')

            try:
                # sends to group
                bot.send_video(group_id, video_file, caption=msg_caption)
                print(msg_caption)
                print(f'video send to {group_id}')
            except Exception as e:
                print(f'Failed to send to {group_id}')

        except TimeoutException:
            bot.send_message(message.chat.id, "Unable to download the video. Please make sure the URL is valid.")


bot.infinity_polling()