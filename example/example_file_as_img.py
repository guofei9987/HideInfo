from clockware import file_as_img

text = "待转变为图片的文本，下面的代码中，会把这段文本以图片形式存放起来"

# 把文本保存为图片
file_as_img.bytes2img(text.encode('utf-8'), img_filename='output1.png')

# 从图片中解出文本
text_encode = file_as_img.img2bytes(img_filename='output1.png')

print(text_encode.decode('utf-8'))

# %% 也可以把任意类型的文件转为图片
# 文件转为图片并存下来
file_as_img.file2img(filename='要隐藏的文件.zip', img_filename='文件转到图片.png')
# 把图片再转会文件
file_as_img.img2file(filename='解出来的文件.zip', img_filename='文件转到图片.png')

# 验证两个文件是一模一样的
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('解出来的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
