from hide_info import hide_in_img

text = "待转变为图片的文本，下面的代码中，会使把这段文本转化为比特类数据，然后隐藏到一个图片中"

hide_in_img.encode(text.encode('utf-8'), img_filename='图片.png', img_filename_new='藏文于图.png')

text_encode = hide_in_img.decode(img_filename='藏文于图.png')

print(text_encode.decode('utf-8'))

# %% 或者把一个文件嵌入到图片中


hide_in_img.file_encode(filename='要隐藏的文件.zip', img_filename='图片.png', img_filename_new='藏物于图.png')

text_encode = hide_in_img.file_decode('藏物于图-解出的文件.zip', img_filename='藏物于图.png')

# 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('lsb解出的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
