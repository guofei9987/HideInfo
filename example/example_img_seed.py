from hide_info import img_seed

text = "待嵌入到图片的文本，下面的代码中，会使用“图种”算法把这段文本隐藏到一个图片中"

img_seed.encode(bytes_data=text.encode('utf-8'), img_filename='图片.jpg', img_filename_new='图种.jpg')
text_encode = img_seed.decode(img_filename='图种.jpg')
print(text_encode.decode('utf-8'))

# %%用图种算法把文件隐藏到图片中
img_seed.file_encode(filename='要隐藏的文件.zip', img_filename='图片.jpg', img_filename_new='图种.jpg')

img_seed.file_decode(filename='解出的文件.zip', img_filename='图种.jpg')

import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open("解出的文件.zip", 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
