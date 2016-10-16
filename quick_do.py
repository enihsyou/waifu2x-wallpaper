# -*- coding: UTF-8 -*-
"""
快速处理一个文件夹，按照2560*1440和3840*2160处理，保证最小边长满足要求。
"""
import os
import subprocess
from shutil import copyfile

from PIL import Image

running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
for file in os.listdir(os.getcwd()):
    file_path = os.path.join(os.getcwd(), file)
    if not os.path.isfile(file_path): continue
    if os.path.splitext(file)[-1] not in ['.bmp', '.jpeg', '.jpg', '.png']: continue
    command = [running]
    try:
        os.mkdir(os.path.join('D:\\', 'temp'))
    except FileExistsError:
        pass
    with Image.open(file) as image:  # type: Image.Image
        width, height = image.size
        ratio = width / height
        print(width, height, ratio, file)
        command.append("-i \"%s\"" % file_path)
        command.append("-o \"%s\"" % os.path.join('D:\\', 'temp', file))
        command.append("-p %s" % 'cudnn')
        if ratio <= 1:
            if not (width < 1440 or height < 2560): continue
            p_height = 1440 / ratio  # 按宽度等比缩放之后 对应的高度
            p_width = 2560 * ratio  # 按高度等比缩放之后 对应的宽度
            if min(p_width, p_height / 16 * 9) == p_width:
                command.append("-w %d" % 1440)
            else:
                command.append("-h %d" % 2560)
        else:
            if not (width < 2160 or height < 2840): continue
            p_height = 2160 / ratio  # 按宽度等比缩放之后 对应的高度
            p_width = 3840 * ratio  # 按高度等比缩放之后 对应的宽度
            if min(p_width, p_height / 16 * 9) == p_width:
                command.append("-h %d" % 2160)
            else:
                command.append("-w %d" % 3840)

        if len(command) > 4:
            command = " ".join(command)
            print(command)
            command_return = subprocess.Popen(command,
                                              shell=True, stdout=subprocess.PIPE).stdout.read()
            print(command_return.decode('shift-jis'))
        else:
            copyfile(file, os.path.join('D:\\', 'temp', file))
