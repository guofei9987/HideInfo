from .utils import serialization, deserialization
import struct


def encode(bytes_data: bytes, text: str):
    data_to_write = serialization(bytes_data)

    data_to_write_bin = ''.join([format(i, '08b') for i in data_to_write])
    assert len(data_to_write_bin) > len(bytes_data) + 1, "要隐藏的数据太大"

    text_new = ''

    for idx, word in enumerate(text):
        text_new += word
        if idx < len(data_to_write_bin) and data_to_write_bin[idx] == '1':
            text_new += chr(127)
    return text_new


def decode(text_new: str) -> bytes:
    bytes_data_bin_extract = ''
    idx = 1
    while idx < len(text_new):
        if text_new[idx] != chr(127):
            idx += 1
            bytes_data_bin_extract += '0'
        else:
            idx += 2
            bytes_data_bin_extract += '1'

    s_bin = bytes_data_bin_extract
    s_out = b''.join([struct.pack('>B', int(s_bin[i * 8:i * 8 + 8], base=2)) for i in range(len(s_bin) // 8)])

    return deserialization(s_out)


def file_encode(filename: str, text_filename: str, text_filename_new: str):
    with open(file=filename, mode='rb') as f1 \
            , open(file=text_filename, mode='r') as f2 \
            , open(file=text_filename_new, mode='w') as f3:
        text_new = encode(bytes_data=f1.read(), text=f2.read())
        f3.write(text_new)


def file_decode(filename: str, text_filename: str):
    with open(file=filename, mode='wb') as f, open(file=text_filename, mode='r') as f2:
        f.write(decode(text_new=f2.read()))
