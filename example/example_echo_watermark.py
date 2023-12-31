from hide_info.echo_watermark import EchoWatermark
from hide_info import utils, evaluate
from scipy.io import wavfile

ori_file = "./ori_file/sounds.wav"  # 载体
embedded_file = "./output/sounds_with_watermark.wav"  # 嵌入水印后的文件名
wm_str = "回声水印算法，欢迎 star!"  # 水印

wm_bits = utils.bytes2bin(wm_str.encode('utf-8'))
len_wm_bits = len(wm_bits)

# embed:
echo_wm = EchoWatermark(pwd=111001)
echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)

# extract：
echo_wm = EchoWatermark(pwd=111001)
wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)

wm_str_extract = utils.bin2bytes(wm_extract).decode('utf-8', errors='replace')
print("extract watermark: ", wm_str_extract)
# error rate：
evaluate.get_error_rate(wm_extract, wm_bits)

# %% There are 3 algorithms：
import numpy as np

wm_bits = np.random.randint(2, size=200).tolist()
len_wm_bits = len(wm_bits)

for algo_type in [1, 2, 3]:
    echo_wm = EchoWatermark(pwd=111001, algo_type=algo_type)
    echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)
    wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)
    error_rate = evaluate.get_error_rate(wm_extract, wm_bits)
    assert error_rate <= 0.03

    _, ori_signal = wavfile.read(ori_file)
    _, wm_signal = wavfile.read(embedded_file)
    evaluate.get_snr(ori_signal, wm_signal)
