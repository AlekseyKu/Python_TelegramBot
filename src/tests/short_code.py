import re

from bs4 import BeautifulSoup
from lxml import etree
import requests
import urllib
import urllib.request
import urllib.parse
#



url = 'https://www.instagram.com/reel/C1kHvkXqO0i/?igsh=eGJhMjZja2F6M3lu'
# url = db_get_last_url_only()

headers = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(url, headers=headers)
soup = BeautifulSoup(webpage.content, "html.parser")
title1 = soup.title
title2 = soup.title.string.split('\n')[0]
#title = str(title1 - title2)

print(title2)

# html = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(html, 'html.parser')
# data = soup.find('video')
# print(html)
#print(data)


# headers = {
#     # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
# }
#
# r = requests.get(url, timeout=30, headers=headers)
#
# soup = BeautifulSoup(r.content, "lxml")
# video_tag = soup.find('video')
# print(video_tag)
# print(soup)



# headers = ({'User-Agent':
#                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
#                 'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
#
# webpage = requests.get(url, headers=headers)
# soup = BeautifulSoup(webpage.content, "html.parser")
# video_tag = soup.find('video')
#
# print(video_tag)


#
# html_content = '''
# <video class="x1lliihq x5yr21d xh8yej3" playsinline="" preload="none" src="https://scontent.cdninstagram.com/o1/v/t16/f1/m82/4A498DF825C0C5F2BAAB3DA9EFCD4AB9_video_dashinit.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuMzYwLmJhc2VsaW5lIn0&_nc_ht=scontent.cdninstagram.com&_nc_cat=108&vs=377010848444093_2238943762&_nc_vs=HBksFQIYT2lnX3hwdl9yZWVsc19wZXJtYW5lbnRfcHJvZC80QTQ5OERGODI1QzBDNUYyQkFBQjNEQTlFRkNENEFCOV92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dLX092eFp5ZWdSa2piUUVBS3FncS00S0k5OWVicFIxQUFBRhUCAsgBACgAGAAbABUAACaC2eXlxNH7PxUCKAJDMywXQDn752yLQ5YYEmRhc2hfYmFzZWxpbmVfMl92MREAdf4HAA%3D%3D&_nc_rid=dbb5b4f5b4&ccb=9-4&oh=00_AfBVS7Kc7M1vxT2Lsreylh2OE0OLteuz7TWxx4Kp073LtQ&oe=66181A55&_nc_sid=10d13b"></video>
# '''
#
# soup = BeautifulSoup(html_content, 'html.parser')
# video_tag = soup.find('video')
#
# if video_tag:
#     video_src = video_tag.get('src')
#     print(video_src)
# else:
#     print('Video tag not found in the HTML content.')
