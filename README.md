# HideInfo

Info Hiding Library  
一些原理简洁的信息隐藏方法  



[![PyPI](https://img.shields.io/pypi/v/HideInfo)](https://pypi.org/project/HideInfo/)
[![License](https://img.shields.io/pypi/l/HideInfo.svg)](https://github.com/guofei9987/HideInfo/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)
[![stars](https://img.shields.io/github/stars/guofei9987/HideInfo.svg?style=social)](https://github.com/guofei9987/HideInfo/)
[![fork](https://img.shields.io/github/forks/guofei9987/HideInfo?style=social)](https://github.com/guofei9987/HideInfo/fork)
[![Downloads](https://pepy.tech/badge/HideInfo)](https://pepy.tech/project/HideInfo)




| 算法   | 说明                |
|------|-------------------|
| [幻影坦克](https://github.com/guofei9987/HideInfo/blob/main/example/example_mirage_tank.py) | 使图片在不同的背景下显示不同的图片 |
| [化物为图](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_as_img.py) | 把数据以图片形式存放        |
| [藏物于图](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_in_img.py) | 把数据藏在一个图片中          |
| [图种](https://github.com/guofei9987/HideInfo/blob/main/example/example_img_seed.py)   | 把图片和文件黏在一起，并存为图片  |
| [EXIF](https://github.com/guofei9987/HideInfo/blob/main/example/example_img_exif.py) | 把一段信息放到图片的EXIF中   |
| [化物为音](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_as_music.py) | 把数据以音频的形式存放       |
| [藏物于音](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_in_music.py) | 把数据隐藏在一个音频中       |
| [化物为文](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_as_txt.py) | 把数据以文本文件的形式存放 |
| [藏物于文](https://github.com/guofei9987/HideInfo/blob/main/example/example_hide_in_txt.py) | 把数据隐藏在一段文本中 |



安装
```
pip install HideInfo
```


## 幻影坦克

功能：把两个图片合并，使其在黑色背景下显示图片A，在白色背景下显示图片B

说明
- 目前只支持黑白图片
- 一般情况下，手机/浏览器的预览和点击大图分别使黑色背景和白色背景，因此有"预览和点击是两张不通的图"的效果
- 未来：支持彩色图片
- 例子：[example/example_mirage_tank.py](example/example_mirage_tank.py)

```python
from hide_info import mirage_tank

mirage_tank.mirage_tank('图片.png', 'img2.jpeg', '幻影坦克.png')
```

## hide_as_img:化物为图

功能：文件/文本/字节 类数据，转换为图片  
原理：图片1个通道上的1个像素，可以存放 0-255 的数字，也就是一个字节。因此可以用来存放数据。
使用场景：
    - 信息隐藏
    - 在只能发送图片的场景下（如某社交软件），发送任意文件


说明
- RGB 3个通道都用来存放数据
- 使用前4个字节存放数据的大小，因此要求总的数据量小于 4G
- 可以存放文件、文本、bytes 类数据，把它转化为一张图片
- 代码：[example_hide_as_img.py](example/example_hide_as_img.py)

```python
from hide_info import hide_as_img

# 文件转为图片并存下来
hide_as_img.file_encode(filename='要隐藏的文件.zip', img_filename='化物为图.png')
# 把图片再转回文件
hide_as_img.file_decode(filename='化物为图-解出来的文件.zip', img_filename='化物为图.png')
```

## hide_in_img：藏物于图

功能：文件/文本/bytes 类数据，藏进一个 PNG 图片中，并且用肉眼无法看出区别
原理：（LSB算法）根据信息的二进制，改变像素数据的最低位，肉眼是无法察觉这种改变
使用场景：
    - 信息隐藏、隐蔽传输
    - 在只能发送图片的场景下（例如某社交软件），发送任意信息
    - 盲水印、图片溯源、版权保护


说明
- 解原始数据时，无需原图参与，只看最低位
- 使用前4个字节存放数据的大小
- 使用位运算，提高一定的性能
- LSB算法对压缩、转格式等攻击脆弱
- 例子：[example_hide_in_img.py](example/example_hide_in_img.py)

```python
from hide_info import hide_in_img

# 把文件隐藏到图片中
hide_in_img.file_encode(filename='要隐藏的文件.zip', img_filename='图片.png', img_filename_new='藏物于图.png')
# 从图片中提取文件
text_encode = hide_in_img.file_decode('藏物于图-解出的文件.zip', img_filename='藏物于图.png')
```


## img_seed:图种

功能：把图片和文件连接起来，以图片的形式存下来（目前还不完善）

- 例子：[example/example_img_seed.py](example/example_img_seed.py)

## img_exif:把信息隐藏在图片的EXIF中

功能：把信息隐藏在图片的 EXIF 中，从而获得隐蔽信息、传输隐蔽信息的能力

- 例子：[example/example_img_exif.py](example/example_img_exif.py)

## hide_in_music: 藏物于音

功能：把一段信息（文件/文本/bytes），藏进一个音乐文件中

例子：
- [example_hide_in_music.py](example/example_hide_in_music.py)

```python
from hide_info import hide_in_music

# 把文件隐藏到某个音乐中
hide_in_music.file_encode(filename='要隐藏的文件.zip', music_filename="音乐.wav", music_filename_new="藏物于音.wav")
# 从音乐中提取文件
hide_in_music.file_decode(filename="藏物于音-解出的文件.zip", music_filename="藏物于音.wav")
```

## hide_as_music：化物为音

功能：把一段信息（文件/文本/bytes），转为声音
原理：用 16 种音可以表示一个四进制。如果每个音持续 0.05 秒，那么每秒声音可以存放 10 字节
使用场景：
    - 信息隐藏、隐蔽传输
    - 在只能发送图片的场景下（例如某社交软件），发送任意信息
    

说明
- 例子：[hide_as_music.py](example/example_hide_as_music.py)

```python
from hide_info import hide_as_music

# 文件转为声音并存下来
hide_as_music.file_encode(filename='要隐藏的文件2.zip', wav_filename='化物为音.wav')
# 把声音再转回文件
hide_as_music.file_decode(filename='化物为音-解出来的文件.zip', wav_filename='化物为音.wav')

```

## hide_in_text：藏物于文

功能：把一段信息（文件/文本/bytes），藏进一段文本中

说明
- 实测在苹果设备 Macbook、IOS 上，隐藏前后的文本看不出区别。但是 Windows 和某些安卓系统上，会有空格
- 例子：[hide_in_txt.py](example/example_hide_in_txt.py)

```python
from hide_info import hide_in_txt

# 把一个文件隐藏在一段已有的文本中
hide_in_txt.file_encode(filename='要隐藏的文件2.zip', text_filename='一段文本.txt', text_filename_new='藏物于文.txt')
# 从文本中提取文件
hide_in_txt.file_decode(filename='藏物于文-解出的文件.zip', text_filename='藏物于文.txt')
```

## hide_as_txt: 化物为文

功能：把一段信息（文件/文本/bytes），以文本的形式存放下来

说明
- 使用的是 base85 算法
- 例子：[hide_as_txt.py](example/example_hide_as_txt.py)

```python
from hide_info import hide_as_txt

# 把一个文件转化为一段文本，并存下走
hide_as_txt.file_encode(filename='要隐藏的文件.zip', txt_filename='化物为文.txt')
# 从文本中提取文件
hide_as_txt.file_decode(filename='化物为文-解出的文件.zip', txt_filename='化物为文.txt')
```

## 其他算法

缩放藏图：提前计算用近邻法缩放时使用的时哪些像素点，然后把这些像素点变成另一个图。
