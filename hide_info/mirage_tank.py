'''
原理：https://www.guofei.site/2023/08/26/hide_info.html
'''

import cv2
import numpy as np


def mirage_tank(img_filename1: str, img_filename2: str, output_img_filename: str, a=0.5, b=None):
    img1_rgb = cv2.imread(img_filename1)
    img2_grey = cv2.imread(img_filename2, cv2.IMREAD_GRAYSCALE)

    # a 越大，img2 越清晰，但是 img1 越可能出现偏差
    assert 0.1 < a < 0.95, "0.1 < a < 0.95"
    if b is None:
        b = max(img1_rgb.mean() - 255 * a, 10)

    img2_grey = a * img2_grey + b

    height, width, _ = img1_rgb.shape
    # 保证两个图片的大小一致
    img2_grey = cv2.resize(img2_grey, (width, height))

    # 计算 alpha 通道

    img1_avg = img1_rgb.mean(axis=2)

    alpha = 255 - img1_avg.astype('int') + img2_grey.astype('int')
    alpha = np.clip(alpha, 0, 255).reshape(height, width, 1)

    rgb = (img1_rgb - (255 - alpha)) / (alpha / 255)

    alpha = alpha.astype('u8')
    rgb = np.clip(rgb, 0, 255)

    # 带有透明度通道的图像
    image_with_alpha = np.concatenate([rgb, alpha], axis=2)

    cv2.imwrite(output_img_filename, image_with_alpha)
