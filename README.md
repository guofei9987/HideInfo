# cloakware
CryptoCloak: Advanced Info Hiding Library

一些主流（但是原理简单）的信息隐藏方法。


## file_as_img:文件转图

功能：文件/文本/bytes 类数据，转换为图片  
原理：图片1个通道上的1个像素，可以存放 0-255 的数字，也就是一个字节。因此可以用来存放数据。  

算法
- RGB 3个通道都用来存放数据
- 使用前4个字节存放数据的大小，因此要求总的数据量小于 4G
- 可以存放文件、文本、bytes 类数据，把它转化为一张图片
- 例子：[example/example_bytes2img.py](example/example_bytes2img.py)

## lsb：文件藏图

功能：文件/文本/bytes 类数据，藏进一个 PNG 图片中，并且用肉眼无法看出区别  

说明
- 使用 LSB 算法
- 解原始数据时，无需原图参与
- 使用前4个字节存放数据的大小
- 使用位运算，提高一定的性能
- LSB算法对压缩、转格式等攻击脆弱
- 例子：[example/example_lsb.py](example/example_lsb.py)


## 幻影坦克



例子：[example/example_mirage_tank.py](example/example_mirage_tank.py)



## 其他算法

缩放藏图：提前计算用近邻法缩放时使用的时哪些像素点，然后把这些像素点变成另一个图。

幻影坦克