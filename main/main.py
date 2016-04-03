# -*- coding: UTF-8 -*-
import subprocess, time, ctypes, os, re

# ARGUMENTS
command = []
# waifu2x-caffe所在位置
running_path = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
command.append(running_path)


# Functions
def input_files(folder, image):
    re.sub(folder, r'[A-Z]\:(.*)[^\\]', r'\:\\\\')
    image_path = '\"' + os.path.join(folder, image) + '\"'
    command.append("-i " + image_path)


def output_files(folder, image):
    out_path = '\"' + os.path.join(folder, image) + '\"'
    command.append("-o " + out_path)


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


path = r'D:\test'

out_path = ''


def file_names(path):
    img_ext = ['.bmp', '.jpeg', '.jpg', '.png']
    os.chdir(path)
    files = os.listdir(path)
    for item in files:
        if os.path.splitext(item)[-1] in img_ext:  # TODO: 这里有一个临时文件需要排除的需求
            img_name = os.path.basename(item)
            in_name = img_name
            prefix = re.match(r'\w+ \d+', img_name)
            if prefix:
                out_name = prefix.group() + os.path.splitext(item)[1]
            else:
                out_name = os.path.splitext(item)[0] + 'tmp' + os.path.splitext(item)[1]
            input_files(path, in_name)
            output_files(path, out_name)
            global out_path
            out_path = os.path.join(path, out_name)
            yield


next(file_names(path))
mode('auto', 3840)
process('cudnn')

# 所要执行的命令
print(command)
command = " ".join(command)
# command = r"{} -i {} -o {} -m {} -s {} -w 3840 -p cudnn".format(
#     running_path, image_path, out_path, mode, scale_ratio)
print(command)
print(out_path)
# 执行命令
command_return = subprocess.Popen(command,
                                  shell = True, stdout = subprocess.PIPE).stdout.read()
# 获取命令显示的文字
re_value = command_return.decode('shift-jis')

print(re_value)

# Set Windows desktop wallpaper
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0
SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, out_path, SPIF_UPDATEINIFILE)

# Pause or Hold 1s
# time.sleep(1)
os.system("pause")
