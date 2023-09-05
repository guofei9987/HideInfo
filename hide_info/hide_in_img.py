import struct
from clockware.clockware_utils import serialization, deserialization
import numpy as np
from PIL import Image


def encode(bytes_data: bytes, img_filename: str, img_filename_new: str):
    data_to_write = serialization(bytes_data)
    img = np.array(Image.open(img_filename))
    height, width = img.shape[:2]

    # 二进制
    data_to_write_bin = ''.join([format(i, '08b') for i in data_to_write])
    assert len(data_to_write_bin) < height * width * 3, "要隐藏的数据太大"

    for i, binary in enumerate(data_to_write_bin):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        tmp = img[x, y, c]
        if binary == '0':
            img[x, y, c] = tmp & 0b11111110
        if binary == '1':
            img[x, y, c] = tmp | 0b00000001

    Image.fromarray(img).save(img_filename_new)
    return img


def decode(img_filename: str) -> bytes:
    img = np.array(Image.open(img_filename))
    height, width = img.shape[:2]

    #  前4个字节，也就32个二进制存放长度
    lst = []
    for i in range(32):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        lst.append(img[x, y, c] & 0b00000001)

    # 得到实际隐藏的数据长度（二进制位数）
    len_data = int(''.join(str(i) for i in lst), base=2) * 8
    lst = []
    for i in range(len_data + 32):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        lst.append(img[x, y, c] & 0b00000001)

    s_bin = ''.join(str(i) for i in lst)

    s_out = b''.join([struct.pack('>B', int(s_bin[i * 8:i * 8 + 8], base=2)) for i in range(len(s_bin) // 8)])

    return deserialization(s_out)


def file_encode(filename: str, img_filename: str, img_filename_new: str):
    with open(file=filename, mode='rb') as f:
        encode(bytes_data=f.read(), img_filename=img_filename, img_filename_new=img_filename_new)


def file_decode(filename: str, img_filename: str):
    with open(file=filename, mode='wb') as f:
        f.write(decode(img_filename=img_filename))
