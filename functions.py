import os
import random
import re
import subprocess
import threading
import time


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

# def check_input(timer): TODO: 将check_input包装成类
#     global revert
#     print("\n输入q退出 输入b返回上一张\n"
#           "输入l显示处理过的壁纸 输入a暂停 输入s继续\n")
#     while True:
#         # print("时间:", time.ctime())
#         com = input()
#         if com == 'q':
#             print("结束")
#             timer.cancel()
#             pause()
#             break
#         if com == 'b':
#             timer.cancel()
#             revert += 1
#             try:
#                 next(files)
#             except StopIteration:
#                 pause()
#             set_wallpaper()
#             timer.pause()
#             revert -= 1
#             continue
#         if com == 'l':
#             for item in used:
#                 print(item)
#             continue
#         if com == 'a':
#             timer.cancel()
#         if com == 's':
#             timer.cancel()
#             timer.run()


class GetCommand:
    def __init__(self, path, tmp_path, *args):
        self.path = path  # D:\test
        self.tmp_path = tmp_path  # D:\test\tmp
        self.args = args
        self.commands = []
        self.command = r''
        self.image_path = r''  # D:\test\konachan 217778 black.jpg
        self.tmp_img_path = r''  # D:\test\tmp\konachan 217778.jpg
        self.tmp_img_name = r''  # konachan 217778.jpg
        self.image_name = r''
        self.used = []
        self.interval = 2
        # self.used_original = {}

    def add_running_path(self):
        running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
        print("waifu2x-caffe-cui.exe所在文件夹:", running)
        self.commands.append(running)

    def add_input_file(self):
        # re.sub(self.tmp_img_name, r'[A-Z]\:(.*)[^\\]', r'\:\\\\')
        self.image_path = os.path.join(self.path, self.image_name)
        self.commands.append("-i " + '\"' + self.image_path + '\"')

    def add_output_file(self):
        self.tmp_img_path = os.path.join(self.tmp_path, self.tmp_img_name)
        self.commands.append("-o " + '\"' + self.tmp_img_path + '\"')

        print("原始文件:", self.image_path)
        print("输出文件:", self.tmp_img_path)

    def mode(self, mode, weight = None, height = None, scale = 2.0, noise = 1):
        modes = {'auto': '-m auto_scale',
                 'noise': '-m noise',
                 'noise_scale': '-m noise_scale',
                 'scale': '-m scale'}
        self.commands.append(modes[mode])
        if scale != 2.0:
            self.commands.append("-s " + str(scale))
        if 'noise' in mode:
            self.commands.append("-n " + str(noise))
        if weight:
            self.commands.append("-w " + str(weight))
        if height:
            self.commands.append("-h " + str(height))

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
        processes = {'cpu': "-p cpu",
                     'gpu': "-p gpu",
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
        # command_return = subprocess.Popen(" ".join(self.commands),
        #                                   shell = True, stdout = subprocess.PIPE).stdout.read()
        # 获取命令显示的文字
        command_return = b'abc'
        re_value = command_return.decode('shift-jis')
        print(re_value)
        # return re_value

    def set_wallpaper(self):
        """Set Windows desktop wallpaper"""
        print("设置壁纸", self.tmp_img_path)
        # ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

    def pause(self, sec = 0):
        # Pause or Hold 1s
        if sec: self.interval = sec
        time.sleep(self.interval)
        # os.system("pause")

    def get_next_file(self, path = r'', tmp_path = r''):
        if path:
            self.path = path
        if tmp_path:
            self.tmp_path = tmp_path
        img_ext = ['.bmp', '.jpeg', '.jpg', '.png']
        current_files = set(os.listdir(self.path))
        # for item in current_files: # 迭代全部
        while current_files:  # 随机选择 TODO: 添加文件尺寸的检测
            # if revert:
            #     global out_img_path
            #     # used.append(used.pop(-2))
            #     if revert < len(used):
            #         out_img_path = used[-(revert + 1)]
            #         print("切换回上一张:", out_img_path, '\n')
            #         yield
            #         continue
            #     else:
            #         print("已经是第一张了")
            #         print("当前:", out_img_path, '\n')
            #         yield
            #         continue

            self.image_name = random_item = random.sample(current_files, 1)[0]  # konachan 217778 black.jpg

            print("切换模式:", "随机选择")
            print("工作文件夹:", self.path)
            print("临时文件夹:", self.tmp_path)

            image_name = random_item.rsplit('.', 1)[0]  # konachan 217778 black
            img_names = os.path.splitext(random_item)  # ('D:\\test\\tmp\\001', '.jpg')
            if img_names[-1] in img_ext:
                prefix = re.match(r'\w+ \d+', random_item)  # konachan 217778
                if prefix:
                    self.tmp_img_name = prefix.group() + img_names[1]  # konachan 217778.jpg
                else:
                    self.tmp_img_name = image_name + '_tmp' + img_names[1]  # 123_tmp.jpg

                if os.path.exists(self.tmp_img_path):
                    self.set_wallpaper()
                    continue
                self.add_input_file()
                self.add_output_file()
                self.used.append(self.tmp_img_path)  # 输出文件名
                yield

    def get_command(self):  # 切换下一个壁纸
        self.command = " ".join(self.commands)
        print("执行命令:", self.command)

    def apply(self):
        print("时间:", time.ctime())
        now_time = time.perf_counter()

        self.get_command()
        self.run_command()
        self.set_wallpaper()
        self.commands = []

        now_time -= time.perf_counter()
        print("执行时间: ", -now_time)
        print()
        # pause()
