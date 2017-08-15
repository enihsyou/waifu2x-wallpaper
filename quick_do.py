# -*- coding: UTF-8 -*-
"""
快速处理一个文件夹，按照1440*2560和3840*2160 (w*h)处理，保证最小边长满足要求。
"""
import os
import subprocess
from shutil import copyfile

from PIL import Image

caffe_location = r'"D:\Program Files (x86)\waifu2x-caffe\waifu2x-caffe-cui.exe"'


class NoMoreWordException(Exception):
    pass


for file in os.listdir(os.getcwd()):
    file_path = os.path.join(os.getcwd(), file)
    if not os.path.isfile(file_path):
        continue
    if os.path.splitext(file)[-1] not in ('.jpg', '.png', '.bmp', '.jpeg'):
        continue

    command = [caffe_location]

    try:
        os.mkdir(os.path.join('D:\\', 'temp'))
    except FileExistsError:
        pass
    with Image.open(file) as image:  # type: Image.Image
        width, height = image.size
        ratio = width / height
        try:
            if ratio <= 5 / 4:  # 是纵向
                if width < 1440 or height < 2560:
                    t_ratio = 1440 / width  # 横向长度比例

                    if height * t_ratio >= 2560:
                        new_width, new_height = 1440, int(height * t_ratio)
                        command.append("-w %d" % 1440)
                    else:
                        new_width, new_height = int(2560 / height * width), 2560
                        command.append("-h %d" % 2560)
                else:
                    raise NoMoreWordException
            else:
                if width < 3840 or height < 2160:
                    t_ratio = 3840 / width  # 横向缩放到3840 所需的比例

                    if height * t_ratio >= 2160:
                        new_width, new_height = 3840, int(height * t_ratio)
                        command.append("-w %d" % 3840)
                    else:
                        new_width, new_height = int(2160 / height * width), 2160
                        command.append("-h %d" % 2160)
                else:
                    raise NoMoreWordException
        except NoMoreWordException:
            print("当前处理: {}\n 大小: ({}, {}) 跳过".format(
                file, width, height))
            copyfile(file, os.path.join('D:\\', 'temp', file))
            continue
        else:
            command.append("-i \"%s\"" % file_path)
            command.append("-o \"%s\"" % os.path.join('D:\\', 'temp', file))
            command.append("-p %s" % 'cudnn')
            print("当前处理: {}\n原大小: ({}, {}) 比例: {:.4f} 新大小: ({}, {})".format(
                file, width, height, ratio, new_width, new_height))

            command.append("-m auto_scale")
            command.append("-t 1")
            command.append("-c 240")
            command.append(r'--model_dir "D:\Program Files (x86)\waifu2x-caffe\models\upconv_7_anime_style_art_rgb"')
            command_return = subprocess.Popen(" ".join(command),
                                              shell=True, stdout=subprocess.PIPE).stdout.read()
            print(command_return.decode('shift-jis'))

input("{:-^80}".format("FINISHED"))
