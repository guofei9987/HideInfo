from hide_info import hide_as_music

bytes_data = '下面的代码中，会把这段文本以声音文件的形式存放起来'.encode('utf-8')

hide_as_music.encode(bytes_data=bytes_data, wav_filename='结果.wav')

data_bytes = hide_as_music.decode(wav_filename='结果.wav')

print(data_bytes.decode('utf-8'))

# %%也可以把任意类型的文件转为声音
# 文件转为声音并存下来
hide_as_music.file_encode(filename='要隐藏的文件2.zip', wav_filename='化物为音.wav')
# 把声音再转回文件
hide_as_music.file_decode(filename='化物为音-解出来的文件.zip', wav_filename='化物为音.wav')

# 要隐藏的文件和解出的文件一模一样
import hashlib

with open('要隐藏的文件2.zip', 'rb') as f1, open('化物为音-解出来的文件.zip', 'rb') as f2:
    assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
