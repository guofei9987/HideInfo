import math
import numpy as np
from PIL import Image


def encode(data: bytes, filename: str):
    # 前4个字节用来存放整个 data 的大小，可以存放 4G 以下的数据
    data_to_write = len(data).to_bytes(length=4, byteorder="big") + data
    len_data = len(data_to_write)
    width = math.ceil((len_data / 3) ** 0.5)
    data_img = np.zeros((width, width, 3), dtype=np.uint8)
    for i, u8 in enumerate(data_to_write):
        data_img[(i // 3) // width, (i // 3) % width, i % 3] = u8

    image = Image.new(mode='RGB', size=(width, width))
    for x in range(width):
        for y in range(width):
            pixel = tuple(data_img[y][x])
            image.putpixel((x, y), pixel)

    # 保存图像
    image.save(filename)


def decode(filename: str) -> bytes:
    img = Image.open(filename)

    width, height = img.size
    lst = []

    for y in range(height):
        for x in range(width):
            rgb = img.getpixel((x, y))
            lst.extend(rgb)

    decode_bytes = bytes(lst)
    len_data = int.from_bytes(decode_bytes[:4], byteorder="big")
    return decode_bytes[4:len_data + 4]
