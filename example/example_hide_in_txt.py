from hide_info import hide_in_txt

bytes_data = "待嵌入的句子".encode('utf-8')

text = '一段文本，下面的代码中，这段文本会被嵌入隐藏信息。隐藏后的文本在一些操作系统上是看不到差别的，但是在另一些上操作系统上能看到很多空格' * 50
text_new = hide_in_txt.encode(bytes_data, text)
text_extract = hide_in_txt.decode(text_new)
print(text_extract.decode('utf-8'))

# %%把一个文件隐藏到文本中
hide_in_txt.file_encode(filename='要隐藏的文件2.zip', text_filename='一段文本.txt', text_filename_new='藏物于文.txt')

hide_in_txt.file_decode(filename='解出的文件.zip', text_filename='藏物于文.txt')

# 验证一致
import hashlib

with open('要隐藏的文件2.zip', 'rb') as f1, open("解出的文件.zip", 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
