# -*- coding: UTF-8 -*-
import random
import subprocess
import threading
import time
import ctypes
import os
import re

# ARGUMENTS
command = []
used = []
revert = 0
TIME_INTERVAL = 1200
# path = r'D:\test'  # 文件所在的文件夹
path = r'D:\Sean\我的图片\新建文件夹'  # 文件所在的文件夹
tmp_path = r'D:\test\tmp'  # 文件所在的文件夹
out_img_path = ''  # 输出的文件夹 初始化
if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)


# Functions
def running_path():
    running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
    print("waifu2x-caffe-cui.exe所在文件夹:", running)
    command.append(running)


def input_files(folder, image):
    re.sub(folder, r'[A-Z]\:(.*)[^\\]', r'\:\\\\')
    image_path = '\"' + os.path.join(folder, image) + '\"'
    command.append("-i " + image_path)


def output_files(folder, image):
    out_path = '\"' + os.path.join(folder, image) + '\"'
    command.append("-o " + out_path)
    global out_img_path
    out_img_path = os.path.join(folder, image)
    print("输出文件:", out_img_path)


def mode(mode, weight = None, height = None, scale = 2.0, noise = 1):
    modes = {'auto': '-m auto_scale',
             'noise': '-m noise',
             'noise_scale': '-m noise_scale',
             'scale': '-m scale'}
    command.append(modes[mode])
    if scale != 2.0:
        command.append("-s " + str(scale))
    if 'noise' in mode:
        command.append("-n " + str(noise))
    if weight:
        command.append("-w " + str(weight))
    if height:
        command.append("-h " + str(height))


def model(style):
    """
    モデルが格納されているディレクトリへのパスを指定します。デフォルト値は`models/anime_style_art_rgb`です。
    標準では以下のモデルが付属しています。
    * `models/anime_style_art_rgb` : RGBすべてを変換する2次元画像用モデル
    * `models/anime_style_art` : 輝度のみを変換する2次元画像用モデル
    * `models/ukbench` : 写真用モデル(拡大するモデルのみ付属しています。ノイズ除去は出来ません)
    基本的には指定しなくても大丈夫です。デフォルト以外のモデルや自作のモデルを使用する時などに指定して下さい。
    """
    styles = {0: '--model_dir models/anime_style_art_rgb',
              1: '--model_dir models/anime_style_art',
              2: '--model_dir models/ukbench'}
    command.append(styles[style])


def process(pro):
    processes = {'cpu': "-p cpu",
                 'gpu': "-p gpu",
                 'cudnn': "-p cudnn"}
    command.append(processes[pro])


def crop_size(size = 128):
    if size != 128:
        command.append("-c " + str(size))


def output_quality(q = -1):
    if q > 0:
        command.append("-q " + str(q))


def tta(y = 0):
    if y:
        command.append("-t 1")


def file_names(path, tmp_path):
    global out_img_path
    img_ext = ['.bmp', '.jpeg', '.jpg', '.png']
    current_files = set(os.listdir(path))
    # for item in current_files: # 迭代全部
    while current_files:  # 随机选择
        if revert:
            global out_img_path
            # used.append(used.pop(-2))
            if revert < len(used):
                out_img_path = used[-(revert + 1)]
                print("切换回上一张:", out_img_path, '\n')
                yield
                continue
            else:
                print("已经是第一张了")
                print("当前:", out_img_path, '\n')
                yield
                continue

        random_item = random.sample(current_files, 1)[0]
        print("切换模式:", "随机选择")
        print("工作文件夹:", path)
        print("临时文件夹:", tmp_path)
        if os.path.splitext(random_item)[-1] in img_ext:
            img_name = os.path.basename(random_item)
            in_name = img_name
            prefix = re.match(r'\w+ \d+', img_name)
            if prefix:
                out_name = prefix.group() + os.path.splitext(random_item)[1]
            else:
                out_name = os.path.splitext(random_item)[0] + 'tmp' + os.path.splitext(random_item)[1]

            input_files(path, in_name)  # 输入文件名
            if os.path.exists(os.path.join(tmp_path, in_name)):
                global out_img_path
                out_img_path = os.path.join(tmp_path, in_name)
                set_wallpaper()
                continue
            else:
                output_files(tmp_path, out_name)  # 输出文件名
            used.append(out_img_path)
            yield


files = file_names(path, tmp_path)  # 迭代器 当前文件夹的文件


# 执行命令
def run_command():
    command_return = subprocess.Popen(" ".join(command),
                                      shell = True, stdout = subprocess.PIPE).stdout.read()
    # 获取命令显示的文字
    re_value = command_return.decode('shift-jis')
    print(re_value)
    return re_value


def set_wallpaper():
    """Set Windows desktop wallpaper"""
    print("设置壁纸", out_img_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, out_img_path, 0)


def pause():
    # Pause or Hold 1s
    time.sleep(3)
    # os.system("pause")


def get_command():  # 切换下一个壁纸
    running_path()
    next(files)
    mode('auto', 3840)
    process('cudnn')
    # print("命令列表:", command)
    print("执行命令:", " ".join(command))


class Time:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self.thread = threading.Timer(self.interval, self.run)

    def run(self):
        self.func()
        self.thread = threading.Timer(self.interval, self.run)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

    def pause(self):
        self.thread = threading.Timer(self.interval, self.run)
        self.thread.start()


def apply_wallpaper():
    print("时间:", time.ctime())
    now_time = time.perf_counter()

    get_command()
    run_command()
    set_wallpaper()
    global command
    command = []

    now_time -= time.perf_counter()
    print("执行时间: ", -now_time)
    print()
    # pause()


def check_input(timer):
    global revert
    print("\n输入q退出 输入b返回上一张\n"
          "输入l显示处理过的壁纸 输入a暂停 输入s继续\n")
    while True:
        # print("时间:", time.ctime())
        com = input()
        if com == 'q':
            print("结束")
            timer.cancel()
            pause()
            break
        if com == 'b':
            timer.cancel()
            revert += 1
            try:
                next(files)
            except StopIteration:
                pause()
            set_wallpaper()
            timer.pause()
            revert -= 1
            continue
        if com == 'l':
            for item in used:
                print(item)
            continue
        if com == 'a':
            timer.cancel()
        if com == 's':
            timer.cancel()
            timer.run()


timer = Time(apply_wallpaper, TIME_INTERVAL)
apply_wallpaper()
timer.start()
thread2 = threading.Thread(target = check_input(timer), name = "输入检测")
# thread1 = threading.Thread(target = timer.start(), name = "切换壁纸")
# threads = [thread1, thread2]
# if __name__ == '__main__':
#     # apply_wallpaper()
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#
#     print("结束了")
#     pause()


# TODO: 尝试预渲染几张