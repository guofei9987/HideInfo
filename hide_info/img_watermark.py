import numpy
import numpy as np
from PIL import Image


def encode(img: numpy.ndarray, watermark: numpy.ndarray, n: int):
    height, width = img.shape[:2]
    height0, width0 = watermark.shape

    a1 = np.uint8(1 << n)
    a2 = ~(np.uint8(a1))

    for i in range(height):
        for j in range(width):
            if watermark[i % height0, j % width0]:
                for channel in range(3):
                    img[i, j, channel] |= a1
            else:
                for channel in range(3):
                    img[i, j, channel] &= a2


def decode(img, n):
    height, width = img.shape[:2]
    a1 = np.uint8(1 << n)
    watermark_extract = np.zeros(shape=(height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            tmp = sum(img[i, j, channel] & a1 for channel in range(3))
            watermark_extract[i, j] = int(tmp * 85)  # 85 = 255 / 3

    return watermark_extract


def file_encode(img_filename: str, watermark_filename: str, img_filename_new: str, n: int = 0):
    # n：0～3，越大水印强度越高
    watermark = np.array(Image.open(watermark_filename).convert('1'))
    img = np.array(Image.open(img_filename))
    encode(img, watermark, n)
    Image.fromarray(img).save(img_filename_new)


def file_decode(img_filename: str, wm_extract: str, n: int = 0):
    img = np.array(Image.open(img_filename))
    watermark_extract = decode(img, n)
    Image.fromarray(watermark_extract).save(wm_extract)

