"""
展示 hide_info.img_watermark 添加水印时的抗攻击性
"""


from hide_info import img_watermark
import cv2

# 嵌入隐式水印
img_watermark.file_encode(img_filename="图片.png", watermark_filename="watermark.png",
                          img_filename_new="output/图片_打入水印.png")

# 提取隐式水印
img_watermark.file_decode(img_filename="output/图片_打入水印.png", wm_extract="output/解出的水印.png")


# %%截屏攻击
from blind_watermark import att

h, w = cv2.imread('图片.png').shape[:2]

loc_r = ((0.1, 0.1), (0.7, 0.5))
scale = 1

x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

print(f'Crop attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')
att.cut_att3(input_filename='图片_打入水印.png', output_file_name='output/截屏攻击.png',
             loc=(x1, y1, x2, y2), scale=scale)

# 提取隐式水印
img_watermark.file_decode(img_filename="output/截屏攻击.png", wm_extract="output/解出的水印_截屏攻击.png")

# %%
ratio = 0.05
att.salt_pepper_att(input_filename='output/图片_打入水印.png', output_file_name='output/椒盐攻击.png', ratio=ratio)
# ratio是椒盐概率

# 提取隐式水印
img_watermark.file_decode(img_filename="output/椒盐攻击.png", wm_extract="output/解出的水印_椒盐攻击.png")

# %%旋转攻击
angle = 60
att.rot_att(input_filename='output/图片_打入水印.png', output_file_name='output/旋转攻击.png', angle=angle)

# 提取隐式水印
img_watermark.file_decode(img_filename="output/旋转攻击.png", wm_extract="output/解出的水印_旋转攻击.png")

# %%遮挡攻击
n = 60
att.shelter_att(input_filename='output/图片_打入水印.png', output_file_name='output/多遮挡攻击.png', ratio=0.1, n=n)

# 提取隐式水印
img_watermark.file_decode(img_filename="output/多遮挡攻击.png", wm_extract="output/解出的水印_多遮挡攻击.png")
