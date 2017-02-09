# -*- coding: UTF-8 -*-
"""
快速处理一个文件夹，按照1440*2560和3840*2160 (w*h)处理，保证最小边长满足要求。
"""
import os
import subprocess
from shutil import copyfile

from PIL import Image

running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
for file in os.listdir(os.getcwd()):
    file_path = os.path.join(os.getcwd(), file)
    if not os.path.isfile(file_path):
        continue
    if os.path.splitext(file)[-1] not in ['.bmp', '.jpeg', '.jpg', '.png']:
        continue

    command = [running]

    try:
        os.mkdir(os.path.join('D:\\', 'temp'))
    except FileExistsError:
        pass
    with Image.open(file) as image:  # type: Image.Image
        width, height = image.size
        ratio = width / height
        print("当前处理: ({}, {}) 比例: {:.4f} {}".format(width, height, ratio, file))
        command.append("-i \"%s\"" % file_path)
        command.append("-o \"%s\"" % os.path.join('D:\\', 'temp', file))
        command.append("-p %s" % 'cudnn')
        if ratio <= 5 / 4:  # 是否是纵向
            if width < 1440 or height < 2560:
                t_ratio = 1440 / width  # 横向长度比例

                if height * t_ratio >= 2560:
                    command.append("-w %d" % 1440)
                else:
                    command.append("-h %d" % 2560)
        else:
            if width < 3840 or height < 2160:
                t_ratio = 3840 / width  # 横向长度比例

                if height * t_ratio >= 2160:
                    command.append("-w %d" % 3840)
                else:
                    command.append("-h %d" % 2160)

        if len(command) > 4:
            command = " ".join(command)
            command_return = subprocess.Popen(command,
                                              shell=True, stdout=subprocess.PIPE).stdout.read()
            print(command_return.decode('shift-jis'))
        else:
            copyfile(file, os.path.join('D:\\', 'temp', file))
            print("跳过\n")
