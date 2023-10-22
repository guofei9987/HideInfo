from hide_info import img_watermark

# 嵌入隐式水印
img_watermark.file_encode(img_filename="图片.png", watermark_filename="watermark.png", img_filename_new="图片_打入水印.png")

# 提取隐式水印
img_watermark.file_decode(img_filename="图片_打入水印.png", wm_extract="解出的水印.png")
