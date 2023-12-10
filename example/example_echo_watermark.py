import numpy as np
from hide_info.echo_watermark import EchoWatermark, get_error_rate, get_snr
from hide_info import utils

ori_file = "sounds.wav"
embedded_file = "sounds_with_watermark.wav"
wm_str = "回声水印算法，欢迎 star!"

wm_bits = utils.bytes2bin(wm_str.encode('utf-8'))

len_wm_bits = len(wm_bits)

# embed:
echo_wm = EchoWatermark(pwd=111001)
echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)

# extract：
echo_wm = EchoWatermark(pwd=111001)
wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)

wm_str_extract = utils.bin2bytes(wm_extract).decode('utf-8', errors='replace')
print("解出水印：", wm_str_extract)
get_error_rate(wm_extract, wm_bits)

# %% There are 3 algorithms：
wm_bits = np.random.randint(2, size=200).tolist()
len_wm_bits = len(wm_bits)

for algo_type in [1, 2, 3]:
    echo_wm = EchoWatermark(pwd=111001, algo_type=algo_type)
    echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)
    wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)
    error_rate = get_error_rate(wm_extract, wm_bits)
    get_snr(embedded_file, ori_file)
    assert error_rate <= 0.03
