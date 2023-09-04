import wave
from clockware.clockware_utils import serialization, deserialization


def encode(bytes_data: bytes, music_filename: str, music_filename_new: str):
    bytes_data = serialization(bytes_data)
    with wave.open(music_filename, "rb") as f:
        attrib = f.getparams()
        wav_data = bytearray(f.readframes(-1))

    for index in range(len(bytes_data)):
        wav_data[index * 4] = bytes_data[index]

    with wave.open(music_filename_new, "wb") as f:
        f.setparams(attrib)
        f.writeframes(wav_data)


def decode(music_filename: str) -> bytes:
    with wave.open(music_filename, 'rb') as f:
        wav_data = f.readframes(-1)

    # 得到隐藏的数据的长度
    extract_data = bytearray()
    for idx in range(4):
        extract_data += wav_data[idx * 4].to_bytes(1, byteorder='big')
    len_data = int.from_bytes(extract_data, 'big')

    extract_data = bytearray()
    for idx in range(4, 4 + len_data):
        extract_data += (wav_data[idx * 4]).to_bytes(1, byteorder='big')
    return extract_data


def file_encode(filename: str, music_filename: str, music_filename_new: str):
    with open(filename, 'rb') as f:
        encode(bytes_data=f.read(), music_filename=music_filename, music_filename_new=music_filename_new)


def file_decode(filename: str, music_filename: str):
    bytes_data = decode(music_filename=music_filename)
    with open(filename, 'wb') as f:
        f.write(bytes_data)
