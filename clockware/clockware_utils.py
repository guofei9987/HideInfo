DATA_TYPE_BYTES = b'__bytes__' + b'\x00' * 51
DATA_TYPE_STRING = b'__string__' + b'\00' * 50


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
