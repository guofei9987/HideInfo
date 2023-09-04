from clockware import hide_in_img

text = "待转变为图片的文本，下面的代码中，会使用LSB算法把这段文本以二进制形式嵌入到一个图片中"

hide_in_img.encode(text.encode('utf-8'), img_filename='图片.png', img_filename_new='LSB算法嵌入后的图片.png')

text_encode = hide_in_img.decode(img_filename='LSB算法嵌入后的图片.png')

print(text_encode.decode('utf-8'))

# %% 或者把一个文件嵌入到图片中


hide_in_img.file_encode(filename='要隐藏的文件.zip', img_filename='图片.png', img_filename_new='LSB算法嵌入后的图片.png')

text_encode = hide_in_img.file_decode('lsb解出的文件.zip', img_filename='LSB算法嵌入后的图片.png')

# 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('lsb解出的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
