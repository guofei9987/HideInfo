from base64 import b85encode, b85decode





def encode(bytes_data: bytes, txt_filename: str):
    with open(txt_filename, 'w') as f:
        f.write(b85encode(bytes_data).decode('utf-8'))


def decode(txt_filename: str) -> bytes:
    with open(txt_filename, 'r') as f:
        return b85decode(f.read().encode('utf-8'))


def file_encode(filename: str, txt_filename: str):
    with open(file=filename, mode='rb') as f:
        encode(bytes_data=f.read(), txt_filename=txt_filename)


def file_decode(filename: str, txt_filename: str):
    with open(file=filename, mode='wb') as f:
        f.write(decode(txt_filename=txt_filename))

