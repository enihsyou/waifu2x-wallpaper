# -*- coding: UTF-8 -*-
"""
快速处理一个文件夹，按照1440*2560和3840*2160 (w*h)处理，保证最小边长满足要求。
"""
import os
import subprocess
from shutil import copyfile

from PIL import Image

running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
# 创建目标文件夹
output_folder = os.path.join('D:\\', 'temp')
try:
    os.mkdir(output_folder)
    print("目标文件夹: {} 已创建".format(output_folder))
except FileExistsError:
    print("目标文件夹: {} 已存在".format(output_folder))

# 处理数量计数器
no = 0

for file in os.listdir(os.getcwd()):
    file_path = os.path.join(os.getcwd(), file)  # 来源文件路径
    if not os.path.isfile(file_path):
        continue
    if os.path.splitext(file)[-1] not in ('.jpg', '.png', '.bmp', '.jpeg'):
        continue

    command = [running]
    no += 1

    with Image.open(file) as image:  # type: Image.Image
        width, height = image.size

    if height and width:
        ratio = width / height
    else:
        print("#{:d}: 图片维度信息错误\n\t文件名: {}".format(no, file))
        continue

    magnitude = 1
    command.append("-i \"%s\"" % file_path)
    command.append("-o \"%s\"" % os.path.join('D:\\', 'temp', file))
    command.append("-p %s" % 'cudnn')
    if ratio <= 5 / 4:  # 是否是纵向
        if width < 1440 or height < 2560:
            t_ratio = 1440 / width  # 横向长度比例

            if height * t_ratio >= 2560:
                command.append("-w %d" % 1440)
                magnitude = t_ratio
            else:
                command.append("-h %d" % 2560)
                magnitude = 2560 / height
    else:
        if width < 3840 or height < 2160:
            t_ratio = 3840 / width  # 横向长度比例

            if height * t_ratio >= 2160:
                command.append("-w %d" % 3840)
                magnitude = t_ratio
            else:
                command.append("-h %d" % 2160)
                magnitude = 2160 / height

    if len(command) > 4:
        print("#{:d}: 原始分辨率: ({:d}, {:d}) 比例: {:.4f} 放大率: {:.4f}\n\t文件名: {}".format(
            no, width, height, ratio, magnitude, file))
        command = " ".join(command)
        command_return = subprocess.Popen(command,
                                          shell=True, stdout=subprocess.PIPE).stdout.read()
        print("\t{}".format(command_return.decode('shift-jis')))
    else:
        print("#{:d}: 原始分辨率: ({:d}, {:d}) 比例: {:.4f}\n\t文件名: {}".format(
            no, width, height, ratio, file))
        copyfile(file, os.path.join('D:\\', 'temp', file))
        print("\t无需处理，跳过")
