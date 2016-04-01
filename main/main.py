import os, subprocess, time, ctypes

# Path
drive = "D:\\"
folder = "test"
image = "004.jpg"
image_path = os.path.join(drive, folder, image)
image2 = "0x.jpg"
out_path = os.path.join(drive, folder, image2)

print(image_path)  # r'D:\test\001.jpg'

running_path = r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe"
# in_path = r"D:\test\002.jpg"
in_path = image_path
command = r"{} -i {} -o {} -m auto_scale -s 2.0".format(running_path, in_path, out_path)
a = os.popen(command)

############
# 使用shift_jis编码 decode byte
# a = b'\x95\xcf\x8a\xb7\x82\xc9\x90\xac\x8c\xf7\x82\xb5\x82\xdc\x82\xb5\x82\xbd\r\n'
# print(a.decode('gbk'))
# print(a.decode('shift_jis'))  # 変換に成功しました

re_value = bytes(a.read().encode('gbk')).decode('shift-jis')
############
# 其他做法
# print(" ".join(c))
# 'D:\Download\waifu2x-caffe\waifu2x-caffe\waifu2x-caffe-cui.exe -i D:\test\001.jpg -m noise --noise_level 2'
# os.popen(r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe -i D:\test\002.jpg")

# b = subprocess.call(r"D:\waifu2x-caffe\waifu2x-caffe-cui.exe -i D:\test\003.jpg")


a.close()
print(re_value)

# Set Windows desktop wallpaper
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0
SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, out_path, SPIF_UPDATEINIFILE)

# Pause or Hold 1s
time.sleep(1)
# os.system("pause")
