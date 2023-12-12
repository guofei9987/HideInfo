import struct


def serialization(data: bytes) -> bytes:
    """
    功能：输入数据，输出其封装后的 bytes 类型，其封装以下内容：
    - 数据的长度（4个字节）
    - 数据本身（n个字节）
    """
    return len(data).to_bytes(length=4, byteorder='big') + data


def deserialization(serialized_data: bytes):
    """
    与 serialization 相反的操作
    """
    return serialized_data[4:4 + int.from_bytes(serialized_data[:4], byteorder="big")]


def bytes2bin_(bytes1: bytes) -> str:
    """
    把 bytes 转化为 "10110" 这种形式的二进制
    """
    return ''.join([format(i, '08b') for i in bytes1])


def bin2bytes_(bin1: str) -> bytes:
    """
    bytes2bin_ 的相反操作
    """
    return b''.join([struct.pack('>B', int(bin1[i * 8:i * 8 + 8], base=2)) for i in range(len(bin1) // 8)])


def bytes2bin(bytes1: bytes) -> list:
    """
    把 bytes 转化为 [1, 0, 1, 1, 0] 这种形式的二进制
    """
    return [int(i) for i in bytes2bin_(bytes1)]


def bin2bytes(bin1: list) -> bytes:
    """
    bytes2bin 的相反操作
    """
    return bin2bytes_(''.join([str(int(i)) for i in bin1]))
