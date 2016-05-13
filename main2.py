# -*- coding: UTF-8 -*-
from functions import *

command = []
used = []
TIME_INTERVAL = 600
path = r'D:\Sean\我的图片\WallPaper\2k'  # 文件所在的文件夹
# path = r'D:\test'  # 文件所在的文件夹
tmp_path = r'D:\test\tmp'  # 文件所在的文件夹
if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

paper = Command(path, tmp_path)
paper.set_interval(TIME_INTERVAL)
paper.modes('auto', 3840)
next_file = paper.get_next_file()

next(next_file)
paper.apply()

timer = Time(paper.next, TIME_INTERVAL)
thread2 = threading.Thread(target = check_input(timer, paper), name = "输入检测")
