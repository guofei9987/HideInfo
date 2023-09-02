import math
import numpy as np
from PIL import Image
from .clockware_utils import serialization, deserialization


def bytes2img(bytes_data: bytes, img_filename: str):
    data_to_write = serialization(bytes_data)

    len_data = len(data_to_write)
    width = math.ceil((len_data / 3) ** 0.5)
    data_img = np.zeros((width, width, 3), dtype=np.uint8)
    for i, u8 in enumerate(data_to_write):
        data_img[(i // 3) // width, (i // 3) % width, i % 3] = u8

    Image.fromarray(data_img).save(img_filename)


def img2bytes(img_filename: str) -> bytes:
    img = Image.open(img_filename)

    width, height = img.size
    lst = []

    for y in range(height):
        for x in range(width):
            rgb = img.getpixel((x, y))
            lst.extend(rgb)

    return deserialization(bytes(lst))


def file2img(filename: str, img_filename: str):
    with open(file=filename, mode='rb') as f:
        bytes2img(bytes_data=f.read(), img_filename=img_filename)


def img2file(filename: str, img_filename: str):
    with open(file=filename, mode='wb') as f:
        f.write(img2bytes(img_filename=img_filename))
