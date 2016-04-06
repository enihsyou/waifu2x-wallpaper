# -*- coding: UTF-8 -*-
from functions import *

command = []
used = []
TIME_INTERVAL = 3
path = r'D:\test'  # 文件所在的文件夹
tmp_path = r'D:\test\tmp'  # 文件所在的文件夹
out_img_path = ''  # 输出的文件夹 初始化
if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

paper = GetCommand(path, tmp_path)
paper.add_running_path()
paper.mode('auto', 1280)

next_file = paper.get_next_file()
next(next_file)
paper.apply()

next(next_file)
paper.apply()

next(next_file)
next(next_file)
next(next_file)
next(next_file)
next(next_file)

paper.apply()
paper.apply()
paper.apply()
