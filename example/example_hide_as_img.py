from hide_info import hide_as_img

text = "待转变为图片的文本，下面的代码中，会先把把这段文本转为比特类数据，然后以图片形式存放起来"

# 把文本保存为图片
hide_as_img.encode(text.encode('utf-8'), img_filename='化文为图.png')

# 从图片中解出文本
text_encode = hide_as_img.decode(img_filename='化文为图.png')

print(text_encode.decode('utf-8'))

# %% 也可以把任意类型的文件转为图片
# 文件转为图片并存下来
hide_as_img.file_encode(filename='要隐藏的文件.zip', img_filename='化物为图.png')
# 把图片再转会文件
hide_as_img.file_decode(filename='化物为图-解出来的文件.zip', img_filename='化物为图.png')

# 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('解出来的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
