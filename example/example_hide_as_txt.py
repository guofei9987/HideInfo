from hide_info import hide_as_txt

text = "待转变为文本的文本，下面的代码中，会把这段文本以另一种文本的形式存下来"

hide_as_txt.encode(text.encode('utf-8'), txt_filename='化物为文.txt')
text_decode = hide_as_txt.decode('化物为文.txt').decode('utf-8')

# %%
# 把一个文件转化为一段文本，并存下走
hide_as_txt.file_encode(filename='要隐藏的文件.zip', txt_filename='化物为文.txt')
# 从文本中提取文件
hide_as_txt.file_decode(filename='化物为文-解出的文件.zip', txt_filename='化物为文.txt')

# 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open('化物为文-解出的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
