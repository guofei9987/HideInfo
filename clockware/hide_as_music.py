import numpy as np
import wave
from scipy import fftpack

SAMPLE_RATE = 44100  # 音频采样率
SAMPLE_TIME = 0.05  # 采样时间
SAMPLE_NUM = int(SAMPLE_RATE * SAMPLE_TIME)  # 采样点数量

FREQUENCY_LIST = [i * 100 + 40 for i in range(16)]  # 选择 16 个音（单位Hz）表示一个四进制
QUA_LIST = '0123456789abcdef'
FREQUENCY_DICT = dict(zip(QUA_LIST, FREQUENCY_LIST))

X = np.arange(0, SAMPLE_TIME, 1 / SAMPLE_RATE)  # 用于生成波形


def encode1(qua):
    # 一位四进制数 -> 波形
    return np.sin(2 * np.pi * FREQUENCY_DICT[qua] * X)


def encode_all(bytes_data: bytes):
    return np.concatenate([encode1(c) for c in bytes_data.hex()])


def encode(bytes_data: bytes, wav_filename: str):
    wav_data = encode_all(bytes_data)
    with wave.open(wav_filename, mode='wb') as f:
        f.setparams((1, 2, SAMPLE_RATE, len(wav_data), "NONE", "NOT COMPRESSED"))  # 单通道
        f.writeframes((wav_data * 32768).astype(np.int16))  # wav_data原幅值为[-1,1]，乘32768可以提高音量


def fft(data):
    N = len(data)
    fft_data = fftpack.fft(data)
    abs_fft = np.abs(fft_data)
    abs_fft = abs_fft / (N / 2)  # fft后弦波分量的振幅放大了N/2倍，除一下以归一化
    half_fft = abs_fft[range(N // 2)]  # 取单边频谱
    return half_fft


def decode1(wav_slice):
    fft_ret = fft(wav_slice)
    for idx, freq in enumerate(FREQUENCY_LIST):
        if np.max(fft_ret[int(freq * SAMPLE_TIME) - 2: int(freq * SAMPLE_TIME) + 2]) > 0.8:
            return QUA_LIST[idx]


def decode(wav_filename: str):
    with wave.open(wav_filename, 'rb') as f:
        wav_data = np.frombuffer(f.readframes(-1), dtype=np.int16) / 32768

    len_data = len(wav_data) // SAMPLE_NUM  # 音频片段个数
    hex_data = ''.join(decode1(wav_data[i * SAMPLE_NUM: (i + 1) * SAMPLE_NUM]) for i in range(len_data))
    return bytes.fromhex(hex_data)


def file_encode(filename: str, wav_filename: str):
    with open(file=filename, mode='rb') as f:
        encode(bytes_data=f.read(), wav_filename=wav_filename)


def file_decode(filename: str, wav_filename: str):
    with open(file=filename, mode='wb') as f:
        f.write(decode(wav_filename=wav_filename))
