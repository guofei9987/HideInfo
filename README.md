# cloakware
CryptoCloak: Advanced Info Hiding Library



## file_as_img

功能：文件/文本/bytes 类数据，转换为图片  
原理：图片1个通道上的1个像素，可以存放 0-255 的数字，也就是一个字节。因此可以用来存放数据。  

算法
- RGB 3个通道都用来存放数据
- 使用前4个字节存放整个数据的大小，因此要求总的数据量小于 4G
- 可以存放文件、文本、bytes 类数据，把它转化为一张图片
- 例子：[example/example_bytes2img.py](example/example_bytes2img.py)

## file_in_img

功能：文件/文本/bytes 类数据，嵌入到一个图片中，并且用肉眼看出区别  

算法
- 使用 LSB 算法
- 