# -*- coding: UTF-8 -*-
"""
快速处理一个文件夹，按照1440*2560和3840*2160 (w*h)处理，保证最小边长满足要求。
"""
import os
import subprocess
from shutil import copyfile

from PIL import Image

caffe_base = 'D:\\Program Files (x86)\\waifu2x-caffe\\'
caffe_exe = r'waifu2x-caffe-cui.exe'
caffe_location = os.path.join(caffe_base, caffe_exe)
temp_folder_path = os.path.join('D:\\', 'temp')


class NoMoreWordException(Exception):
    pass


for file in os.listdir(os.getcwd()):
    original_path = os.path.join(os.getcwd(), file)  # 来源图片绝对路径
    destination_path = os.path.join('D:\\', 'temp', file)  # 目标图片绝对路径
    # 如果这路径指向的根本就不是图片文件，跳过不处理
    if not os.path.isfile(original_path):
        continue
    # 如果这路径指向的不是列表中允许的图片格式，跳过不处理
    if os.path.splitext(file)[-1] not in ('.jpg', '.png', '.bmp', '.jpeg'):
        continue
    # 如果这路径指向的文件已存在，跳过不处理
    if os.path.exists(destination_path):
        continue
    if not os.path.exists(temp_folder_path):
        try:  # 防止中途文件夹被删除
            os.mkdir(temp_folder_path)
        except FileExistsError or NotImplementedError:
            pass
    command = [caffe_location]

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
            copyfile(file, destination_path)
            continue
        else:
            command.append("-i \"%s\"" % original_path)
            command.append("-o \"%s\"" % destination_path)
            command.append("-p %s" % 'cudnn')
            print("当前处理: {}\n原大小: ({}, {}) 比例: {:.4f} 新大小: ({}, {})".format(
                file, width, height, ratio, new_width, new_height))

            command.append("-m auto_scale")
            command.append("-t 1")
            command.append("-c 240")
            command.append('--model_dir "%s"' % os.path.join(caffe_base, "models\\upconv_7_anime_style_art_rgb"))
            command_return = subprocess.Popen(" ".join(command),
                                              shell=True, stdout=subprocess.PIPE).stdout.read()
            print(command_return.decode('shift-jis'))

input("{:-^80}".format("FINISHED"))
