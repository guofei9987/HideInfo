from clockware import bytes2img
text = "待转变为图片的文本"

# 把文本保存为图片
bytes2img.encode(text.encode('utf-8'), filename='output1.png')

# 从图片中解出文本
text_encode = bytes2img.decode(filename='output1.png')
print(text_encode.decode('utf-8'))


#%% 也可以对任意文件使用

with open('要隐藏的文件.zip', 'rb') as f:
    data = f.read()
    bytes2img.encode(data, filename='output.png')

with open('解出的数据.zip', 'wb') as f:
    data2 = bytes2img.decode(filename='output.png')
    f.write(data2)
