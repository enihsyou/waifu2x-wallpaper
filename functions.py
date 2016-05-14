# -*- coding: UTF-8 -*-
import ctypes
import os
import random
import re
import subprocess
import threading
import time
import webbrowser

import psutil
from PIL import Image


class Time:
    def __init__(self, func, interval = 600):
        self.func = func
        self.interval = interval
        self.break_flag = False
        self.stop_flag = False
        self.show_time = False
        self.t = 0

    def start_timer(self):
        """每秒增加时间 遇到终止符返回"""
        self.t += 1

        if self.t >= self.interval and not(self.stop_flag or self.break_flag):
            self.reset()
            self.func()

        if self.show_time:
            self.show_time = False
            print("剩余时间: {}s".format(self.interval - self.t))

        threading.Timer(1, self.start_timer).start()

    def show(self):
        """显示剩余时间"""
        self.show_time = True

    def stop(self):
        """终止时钟"""
        self.break_flag = True
        self.stop_flag = True
        self.reset()

    def start(self):
        self.break_flag = False
        self.stop_flag = False
        self.func()

    def set_interval(self, new_interval):
        """设置函数运行间隔"""
        self.interval = new_interval

    def pause(self):
        """暂停时钟"""
        self.break_flag = True

    def resume(self):
        """恢复暂停了的时钟"""
        self.break_flag = False

    def reset(self):
        """将时间重置"""
        self.t = 0


class Command:
    def __init__(self, path, tmp_path, *args):
        self.path = path  # D:\test
        self.tmp_path = tmp_path  # D:\test\tmp
        self.args = args
        self.commands = []
        self.image_path = r''  # D:\test\konachan 217778 black.jpg
        self.tmp_img_path = r''  # D:\test\tmp\konachan 217778.jpg
        self.tmp_img_name = r''  # konachan 217778.jpg
        self.image_name = r''  # konachan 217778
        self.used = []
        self.used_orig = {}
        self.same_file = False
        self.interval = 5  # pause time in seconds
        self.now_time = 0
        self.revert = 0

        self.mode = r''
        self.width = 0
        self.height = 0
        self.img_width = 0
        self.img_height = 0
        self.scale = 0
        self.noise = 0

        self.aspect_ratio = 1

    def add_running_path(self):
        running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
        # print("waifu2x-caffe-cui.exe所在文件夹:", running)
        self.commands.append(running)

    def add_input_file(self):
        # re.sub(self.tmp_img_name, r'[A-Z]\:(.*)[^\\]', r'\:\\\\')
        self.image_path = os.path.join(self.path, self.image_name)
        self.commands.append("-i " + '\"' + self.image_path + '\"')

    def add_output_file(self):
        self.tmp_img_path = os.path.join(self.tmp_path, self.tmp_img_name)
        self.commands.append("-o " + '\"' + self.tmp_img_path + '\"')
        self.used.append(self.tmp_img_path)
        self.used_orig[self.tmp_img_path] = self.image_path
        print("原始文件:", self.image_path)
        print("输出文件:", self.tmp_img_path)

    def modes(self, mode, width = None, height = None, scale = 2.0, noise = 1):
        modes = {'auto'       : '-m auto_scale',
                 'noise'      : '-m noise',
                 'noise_scale': '-m noise_scale',
                 'scale'      : '-m scale'}
        self.mode = mode
        self.commands.append(modes[mode])
        if scale != 2.0:
            self.scale = scale
            self.commands.append("-s " + str(scale))
        if 'noise' in mode:
            self.noise = noise
            self.commands.append("-n " + str(noise))
        if width:
            self.width = width
            self.commands.append("-w " + str(width))
        if height:
            self.height = height
            self.commands.append("-h " + str(height))
        else:
            self.height = self.width * 9 / 16

    def model(self, style):
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
        self.commands.append(styles[style])

    def process(self, pro):
        processes = {'cpu'  : "-p cpu",
                     'gpu'  : "-p gpu",
                     'cudnn': "-p cudnn"}
        self.commands.append(processes[pro])

    def crop_size(self, size = 128):
        if size != 128:
            self.commands.append("-c " + str(size))

    def output_quality(self, q = -1):
        if q > 0:
            self.commands.append("-q " + str(q))

    def tta(self, y = 0):
        if y:
            self.commands.append("-t 1")

    def run_command(self):
        if self.img_width >= self.width or self.img_height >= self.height:
            print("图片质量优秀")
        elif self.aspect_ratio <= 1.5:
            print("大概不适合桌面")
            next(self.get_next_file())
            self.run_command()

        command_return = subprocess.Popen(" ".join(self.commands),
                                          shell = True, stdout = subprocess.PIPE).stdout.read()
        re_value = command_return.decode('shift-jis')
        print(re_value)
        # return re_value

    def set_wallpaper(self):
        """Set Windows desktop wallpaper"""
        print("设置壁纸", self.tmp_img_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.tmp_img_path, 0)
        print("时间:", time.ctime())

    def set_interval(self, interval):
        self.interval = interval

    def pause(self, sec = 0):
        # Pause or Hold 1s
        if sec: self.interval = sec
        time.sleep(self.interval)
        # os.system("pause")

    def get_next_file(self, path = r'', tmp_path = r''):
        """获取下一个文件"""
        if path:
            self.path = path
        if tmp_path:
            self.tmp_path = tmp_path
        img_ext = ['bmp', 'jpeg', 'jpg', 'png']
        current_files = os.listdir(self.path)
        # for item in current_files: # 迭代全部
        while current_files:  # 随机选择 TODO: 添加文件尺寸的检测
            if self.revert:
                if self.revert < len(self.used):
                    self.used.pop()
                    self.tmp_img_path = self.used[-1]
                    print("切换回上一张:", self.tmp_img_path, '\n')
                    self.same_file = True
                    yield
                    continue
                else:
                    print("已经是第一张了")
                    print("当前:", self.tmp_img_path, '\n')
                    yield
                    continue
            self.image_name = random_item = random.choice(current_files)  # konachan 217778 black.jpg
            self.image_path = os.path.join(self.path, self.image_name)
            if not os.path.isfile(self.image_path): continue
            self.commands = []
            self.add_running_path()
            self.modes(self.mode, self.width)
            # print("切换模式:", "随机选择")
            # print("工作文件夹:", self.plath)
            # print("临时文件夹:", self.tmp_path)

            image_name, ext = random_item.rsplit('.', 1)  # konachan 217778 black , jpg
            if ext in img_ext:
                prefix = re.match(r'\w+ \d+', random_item)  # konachan 217778
                if prefix:
                    self.tmp_img_name = prefix.group() + '.' + ext  # konachan 217778.jpg
                else:
                    self.tmp_img_name = image_name + '_tmp' + '.' + ext  # 123_tmp.jpg

                self.add_input_file()
                self.add_output_file()

                self.get_image_attr(self.image_path)

                if os.path.exists(self.tmp_img_path):
                    print('存在同名临时文件')
                    self.same_file = True
                    self.set_wallpaper()
                    yield
                else:
                    self.same_file = False
                    yield

    def apply(self):
        self.now_time = time.perf_counter()

        # 获取当前内存剩余量
        mem_available = psutil.virtual_memory().available

        if not self.same_file:
            if mem_available < 1514237184:
                mem_parsed = 0
                for x in ['bytes', 'KB', 'MB', 'GB']:
                    if mem_available < 1024.0:
                        mem_parsed = "%3.3f%s" % (mem_available, x)
                    mem_available /= 1024.0
                print("内存不足, 只有", mem_parsed)
            else:
                self.show_image_attr()
                self.run_command()
                self.set_wallpaper()
        self.now_time -= time.perf_counter()
        print("执行时间: ", -self.now_time)
        print()
        # pause()

    def next(self):
        next(self.get_next_file())
        self.apply()

    def get_image_attr(self, img):
        """获取当前图片的 长 宽 宽高比"""
        image = Image.open(img)
        self.img_width, self.img_height = image.size
        self.aspect_ratio = self.img_width / self.img_height

    def show_image_attr(self):
        """显示当前图片的 长 宽 宽高比"""
        # image = Image.open(self.tmp_img_path)
        print("图片属性: {} x {} @ {:.2}".format(self.img_width, self.img_height, self.aspect_ratio))

    def show_image(self):
        """打开当前壁纸的原始文件"""
        os.startfile(self.used_orig[self.tmp_img_path])


def check_input(timer, cls):
    """timer = Time(paper.next, TIME_INTERVAL) cls = Command(path, tmp_path)"""
    print("\n输入q退出 输入b返回上一张 输入w打开原图 ww打开来源\n"
          "输入l显示处理过的壁纸 输入a暂停 输入s继续\n")
    assert isinstance(timer, Time) and isinstance(cls, Command) == True

    timer.start_timer()
    while True:
        # print("时间:", time.ctime())
        com = input()
        if com == 'q':  # 终止
            print("结束")
            timer.stop()
            cls.pause()
            break
        if com == 'b':  # 返回上一张
            timer.stop()
            cls.revert += 1
            try:
                next(cls.get_next_file())
            except StopIteration:
                cls.pause()
            cls.set_wallpaper()
            timer.start_timer()
            cls.revert -= 1
            continue
        if com == 'l':  # 列出列表
            print("最新10张: ")
            for index, item in enumerate(cls.used):
                if index >= len(cls.used) - 10:
                    print('No.' + str(index + 1), item)
            continue
        if com == 'a':  # 暂停
            timer.pause()
        if com == 's':  # 下一张
            timer.stop()
            timer.start()
        if com == 'ww':  # 打开来源
            url = r"http://{}.com/post/show/{}"
            file_name = cls.tmp_img_name.split('.')[0].split()
            webbrowser.open(url.format(file_name[0], file_name[1]))
        if com == 'w':  # 显示原图
            cls.show_image()
        if com == 't':  # 显示剩余时间
            timer.show()
