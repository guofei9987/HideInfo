'''
原理如下：
- 目标是使得一张PNG图片（带透明涂层），在白色背景下显示图A，在黑色背景下显示图B
- 这样的要求下，可以列出以下方程

aP +(1-a)白 = A
aP + (1-a)黑 = B

已知 白色 = 255，黑色 = 0，代入方程，得到：
a = 1- (A-B)
P = B/a

因为 a 的取值范围为 [0, 1]，因此需要 B 图较暗，A图较亮
'''

import cv2
import numpy as np


# 这个只能输出黑白图
def mirage_tank2(img_filename1: str, img_filename2: str, output_img_filename: str):
    A = cv2.imread(img_filename1, flags=cv2.IMREAD_GRAYSCALE) / 255
    B = cv2.imread(img_filename2, flags=cv2.IMREAD_GRAYSCALE) / 255

    # 保证两个图片的大小一致
    B = cv2.resize(B, A.shape[::-1])
    a = 1 - (A - B)
    a = np.clip(a, 0, 1)
    P = B / a
    P = np.clip(P, 0, 1)

    # 创建一个带有透明度通道的图像
    image_with_alpha = np.zeros((A.shape[0], A.shape[1], 4), dtype=np.uint8)
    image_with_alpha[:, :, 0] = P * 255
    image_with_alpha[:, :, 1] = P * 255
    image_with_alpha[:, :, 2] = P * 255
    image_with_alpha[:, :, 3] = a * 255

    # 保存带有透明度通道的图像
    cv2.imwrite(output_img_filename, image_with_alpha)


def mirage_tank(img_filename1: str, img_filename2: str, output_img_filename: str, a=0.5, b=20):
    A = cv2.imread(img_filename1)
    B = cv2.imread(img_filename2)

    height, width, _ = A.shape
    # 保证两个图片的大小一致
    B = cv2.resize(B, (width, height))

    # 计算 alpha 通道
    A_gray = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    B_gray = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    B_gray = a * B_gray + b  # 适当调暗图片B
    alpha = 255 - A_gray.astype('int') + B_gray.astype('int')
    alpha = np.clip(alpha, 1, 255).reshape(height, width, 1)

    # 使用 A 或者 B，决定了彩图来自哪个图
    # P = B / (a / 255)
    P = (A - (255 - alpha)) / (alpha / 255)

    alpha = alpha.astype('u8')
    P = np.clip(P, 0, 255)

    # 带有透明度通道的图像
    image_with_alpha = np.concatenate([P, alpha], axis=2)

    cv2.imwrite(output_img_filename, image_with_alpha)
