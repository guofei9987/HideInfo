from PIL import Image
import piexif


def encode(bytes_data: bytes, img_filename: str, img_filename_new: str):
    im = Image.open(img_filename)
    exif_data = im.info['exif']  # 二进制格式的exif

    # 借助 piexif 来修改并写入文件
    exif_dict = piexif.load(exif_data)  # 二进制格式转 dict 格式
    exif_dict['0th'][270] = bytes_data  # 写入信息
    exif_bytes = piexif.dump(exif_dict)  # dict 格式转回二进制格式
    im.save(img_filename_new, "JPEG", quality=85, exif=exif_bytes)  # 保存文件


def decode(img_filename: str) -> bytes:
    im = Image.open(img_filename)
    exif_data = im.info['exif']  # 二进制格式的exif
    exif_dict = piexif.load(exif_data)
    return exif_dict['0th'][270]
