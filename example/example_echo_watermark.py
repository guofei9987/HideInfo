import numpy as np
from hide_info.echo_watermark import EchoWatermark, get_error_rate, get_snr
from hide_info import utils

ori_file = "音乐.wav"
embedded_file = "打入水印_音乐.wav"  # 嵌入了水印的文件
wm_str = "回声水印算法测试用水印"

wm_bits = [int(i) for i in utils.bytes2bin(wm_str.encode('utf-8'))]

len_wm_bits = len(wm_bits)

# embed:
echo_wm = EchoWatermark(pwd=111001, algo_type=2)
echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)

# extract：
echo_wm = EchoWatermark(pwd=111001, algo_type=2)
wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)

wm_str_extract = utils.bin2bytes(''.join([str(int(i)) for i in wm_extract])).decode('utf-8')
print("解出水印：", wm_str_extract)
get_error_rate(wm_extract, wm_bits)

# %%
wm_bits = np.random.randint(2, size=200).tolist()
len_wm_bits = len(wm_bits)

for algo_type in [1, 2, 3]:
    echo_wm = EchoWatermark(pwd=111001, algo_type=algo_type)
    echo_wm.embed(origin_filename=ori_file, wm_bits=wm_bits, embed_filename=embedded_file)
    wm_extract = echo_wm.extract(embed_filename=embedded_file, len_wm_bits=len_wm_bits)
    get_error_rate(wm_extract, wm_bits)
    get_snr(embedded_file, ori_file)
