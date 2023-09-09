from hide_info import hide_in_music

text = "待嵌入到音乐文件的文本，下面的代码中，会把这段文本以二进制形式隐藏到一个音乐文件中"

hide_in_music.encode(text.encode('utf-8'), music_filename="音乐.wav", music_filename_new="藏文于音.wav")

text_encode = hide_in_music.decode(music_filename="藏文于音.wav")

print(text_encode.decode('utf-8'))

# %%
hide_in_music.file_encode(filename='要隐藏的文件.zip', music_filename="音乐.wav", music_filename_new="藏物于音.wav")

hide_in_music.file_decode(filename="解出的文件.zip", music_filename="藏物于音.wav")

# %% 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件.zip', 'rb') as f1, open("解出的文件.zip", 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
