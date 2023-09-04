# cloakware
CryptoCloak: Advanced Info Hiding Library

一些主流（但是原理简单）的信息隐藏方法。


## hide_as_img:转物为图

功能：文件/文本/bytes 类数据，转换为图片  
原理：图片1个通道上的1个像素，可以存放 0-255 的数字，也就是一个字节。因此可以用来存放数据。  

说明
- RGB 3个通道都用来存放数据
- 使用前4个字节存放数据的大小，因此要求总的数据量小于 4G
- 可以存放文件、文本、bytes 类数据，把它转化为一张图片
- 代码：[example_hide_as_img.py](example/example_hide_as_img.py)

## hide_in_img：藏物于图

功能：文件/文本/bytes 类数据，藏进一个 PNG 图片中，并且用肉眼无法看出区别  

说明
- 使用 LSB 算法
- 解原始数据时，无需原图参与，只看最低位
- 使用前4个字节存放数据的大小
- 使用位运算，提高一定的性能
- LSB算法对压缩、转格式等攻击脆弱
- 例子：[example_hide_in_img.py](example/example_hide_in_img.py)


## 幻影坦克

功能：把两个图片合并，使其在黑色背景下显示图片A，在白色背景下显示图片B

说明
- 目前只支持黑白图片
- 一般情况下，手机/浏览器的预览和点击大图分别使黑色背景和白色背景，因此有"预览和点击是两张不通的图"的效果
- 未来：支持彩色图片
- 例子：[example/example_mirage_tank.py](example/example_mirage_tank.py)

## hide_in_music: 藏物于音

功能：把一段信息（文件/文本/bytes），藏进一个音乐文件中

例子：
-[example_hide_in_music.py](example/example_hide_in_music.py)

## 转物为音

功能：把一段信息（文件/文本/bytes），转为声音

说明
- 选择 16 种音表示四进制
- 每个音持续 0.05 秒，因此每秒对应 10 字节
- 例子：[hide_as_music.py](clockware/hide_as_music.py)


## 其他算法

缩放藏图：提前计算用近邻法缩放时使用的时哪些像素点，然后把这些像素点变成另一个图。

