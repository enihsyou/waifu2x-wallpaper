# -*- coding: UTF-8 -*-
import subprocess, time, ctypes, os, re

# ARGUMENTS
command = []
path = r'D:\test'  # 文件所在的文件夹
tmp_path = r'D:\test\tmp'  # 文件所在的文件夹
out_img_path = ''  # 输出的文件夹 初始化
if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

# Functions
def running_path():
    running = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
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
    print(out_img_path)


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


def file_names(path,tmp_path):
    img_ext = ['.bmp', '.jpeg', '.jpg', '.png']
    os.chdir(path)
    current_files = os.listdir(path)

    for item in current_files:

        if os.path.splitext(item)[-1] in img_ext:  # TODO: 这里有一个临时文件需要排除的需求
            img_name = os.path.basename(item)
            in_name = img_name
            prefix = re.match(r'\w+ \d+', img_name)
            if prefix:
                out_name = prefix.group() + os.path.splitext(item)[1]
            else:
                out_name = os.path.splitext(item)[0] + 'tmp' + os.path.splitext(item)[1]

            input_files(path, in_name)  # 输入文件名
            output_files(tmp_path, out_name)  # 输出文件名
            print(command[-1])
            yield


files = file_names(path,tmp_path)  # 迭代器 当前文件夹的文件


def print_dec(command):
    def deco(func):
        def _deco():
            func()
            print(command)
            print()
            print(" ".join(command))

        return _deco

    return deco


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

    ctypes.windll.user32.SystemParametersInfoW(20, 0, out_img_path, 0)


def pause():
    # Pause or Hold 1s
    # time.sleep(3)
    os.system("pause")




@print_dec(command)  # 调试用
def get_command():  # 切换下一个壁纸
    running_path()
    next(files)
    mode('auto', 1280)
    process('cudnn')


def apply_wallpaper():
    get_command()
    run_command()
    set_wallpaper()
    global command
    command = []
    pause()

while input() != 'q':
    apply_wallpaper()

