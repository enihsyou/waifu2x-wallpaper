import os, subprocess, time, ctypes

# Path
drive = "D:\\"
folder = "test"
image = "001.jpg"
out_image = "tmp.jpg"
image_path = os.path.join(drive, folder, image)
out_path = os.path.join(drive, folder, out_image)

running_path = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"

mode = 'auto_scale'
if mode == 'auto_scale':
    scale_ratio = 2.0

command = r"{} -i {} -o {} -m {} -s {} -w 3840 -p cudnn".format(
    running_path, image_path, out_path, mode, scale_ratio)
print(command)

command_return = subprocess.Popen(command,
                                  shell = True, stdout = subprocess.PIPE).stdout.read()
re_value = command_return.decode('shift-jis')
# re_value = command_return.encode('gbk').decode('shift-jis')

print(re_value)

# Set Windows desktop wallpaper
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0
SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, out_path, SPIF_UPDATEINIFILE)

# Pause or Hold 1s
# time.sleep(1)
os.system("pause")
