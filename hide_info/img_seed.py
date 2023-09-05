"""
# Linux:
cat 1.jpg 1.zip > output.jpg

# Windows:
copy/b 1.jpg+1.zip=output.jpg
"""


def encode(bytes_data: bytes, img_filename: str, img_filename_new: str):
    assert img_filename.endswith('.jpg'), "图种目前只支持 jpg 图片"
    assert img_filename_new.endswith('.jpg'), "图种目前只支持 jpg 图片"

    with open(img_filename, 'rb') as f1:
        img = f1.read()

    with open(img_filename_new, 'wb') as f2:
        f2.write(img + bytes_data)


def decode(img_filename: str) -> bytes:
    with open(img_filename, 'rb') as f:
        bytes3 = f.read()
    idx = bytes3.find(b'\xff\xd9')
    return bytes3[idx + 2:]


def file_encode(filename: str, img_filename: str, img_filename_new: str):
    with open(filename, 'rb') as f:
        encode(f.read(), img_filename, img_filename_new)


def file_decode(filename: str, img_filename: str):
    with open(filename, 'wb') as f:
        f.write(decode(img_filename))
