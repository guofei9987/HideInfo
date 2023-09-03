from clockware import lsb

text = "待转变为图片的文本，下面的代码中，会使用LSB算法把这段文本以二进制形式嵌入到一个图片中"

lsb.lsb_encode(text.encode('utf-8'), img_filename='图片.png', img_filename_new='LSB算法嵌入后的图片.png')

text_encode = lsb.lsb_decode(img_filename='LSB算法嵌入后的图片.png')

print(text_encode.decode('utf-8'))

# %% 或者把一个文件嵌入到图片中


lsb.file_lsb_encode(filename='要隐藏的文件.zip', img_filename='图片.png', img_filename_new='LSB算法嵌入后的图片.png')

text_encode = lsb.file_lsb_decode('lsb解出的文件.zip', img_filename='LSB算法嵌入后的图片.png')

import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('lsb解出的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
