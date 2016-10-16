# -*- coding: UTF-8 -*-
from functions import *

command = []
used = []
TIME_INTERVAL = 600  # 更换间隔 (秒)
running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"  # waifu2x-coffe所在文件夹
path = r'D:\Sean\我的图片\WallPaper\osusume'  # 壁纸文件所在的文件夹
tmp_path = r'D:\test\tmp'  # 临时文件所在的文件夹
if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

paper = Command(path, tmp_path)
paper.set_interval(TIME_INTERVAL)
paper.modes('auto', 3840)
next_file = paper.get_next_file()

# next(next_file)
print("通过回车空格键确认")
paper.next()

timer = Time(paper.next, TIME_INTERVAL)
thread2 = threading.Thread(target = check_input(timer, paper), name = "输入检测")

