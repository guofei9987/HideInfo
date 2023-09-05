from hide_info import img_exif

text = "待嵌入到图片的文本，下面的代码中，会把这段文本隐藏到图片 EXIF 中"

img_exif.encode(bytes_data=text.encode('utf-8'), img_filename='图片.jpg', img_filename_new='隐藏后的图片.jpg')
text_encode = img_exif.decode(img_filename='隐藏后的图片.jpg')
print(text_encode.decode('utf-8'))