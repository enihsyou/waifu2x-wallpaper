# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup, Tag
import os
import os.path as path
import queue
from PIL import Image

BASE_URL = r"https://saucenao.com/search.php"
BASE_URL = r"http://httpbin.org/post"

pictures = []  # 文件夹下面的图片


def scan_dir(location="."):
    """搜索文件夹下面的所有符合扩展名的图片，添加到list里"""
    if not path.isdir(location):
        print("%s is not a directory" % location)
        return
    for file in os.scandir(location):
        if file.is_file():
            basename, ext = path.splitext(file.name)
            if ext in (".jpg", ".png", ".bmp", ".jpeg"):
                pictures.append(file.path)


def make_request(image_path):
    with Image.open(image_path) as image:  # type:Image.Image
        # 缩小图片尺寸
        # orig_width, orig_height = image.size
        # new_width = max(min(orig_width * 0.4, 960) ,640)
        # new_height = max(orig_height * (new_width / orig_width), 360)
        # image = image.resize((new_width, new_height))
        image.thumbnail((960, 540))
        payload = {
            'file': image.tobytes()
        }
        proxies = {
            'http': 'http://127.0.0.1:10800',
            'https': 'http://127.0.0.1:10800',
        }
        response = requests.post(BASE_URL, files=payload, proxies=proxies)
        print(response.text)


def main():
    scan_dir()
    for i in pictures:
        print(i)
    for i in pictures[:1]:
        make_request(image_path=i)

    return 0


if __name__ == "__main__":
    main()
