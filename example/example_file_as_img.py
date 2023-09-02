from clockware import file_as_img
text = "待转变为图片的文本"

# 把文本保存为图片
file_as_img.bytes2img(text.encode('utf-8'), img_filename='output1.png')

# 从图片中解出文本
text_encode = file_as_img.img2bytes(img_filename='output1.png')

print(text_encode.decode('utf-8'))

file_as_img.file2img(filename='要隐藏的文件.zip', img_filename='output1.png')

file_as_img.img2file(filename='解出来的文件.zip', img_filename='output1.png')

# %% 也可以对任意文件使用
import hashlib

with open('要隐藏的文件.zip', 'rb') as f:
    print(hashlib.md5(f.read()).hexdigest())

with open('解出来的文件.zip', 'rb') as f:
    print(hashlib.md5(f.read()).hexdigest())
