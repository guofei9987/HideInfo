# 回声音频水印
import numpy as np
from scipy.io import wavfile
from scipy.signal import windows


class EchoWatermark:
    def __init__(self, pwd, algo_type=2, verbose=False):
        self.pwd = pwd
        self.algo_type = algo_type
        self.verbose = verbose

        self.FRAME_LENGTH = 2048  # 帧长度
        self.CONTROL_STRENGTH = 0.2  # 嵌入强度
        self.OVERLAP = 0.5  # 帧分析的重叠率
        self.NEGATIVE_DELAY = 4  # negative delay, for negative echo
        self.LOG_FLOOR = 0.00001

        # 回声参数
        # for key 1
        self.delay11, self.delay10 = 100, 110
        # for key 0
        self.delay01, self.delay00 = 120, 130

    def embed(self, origin_filename,wm_bits, embed_filename):
        pwd = self.pwd
        algo_type = self.algo_type
        FRAME_LENGTH = self.FRAME_LENGTH
        CONTROL_STRENGTH = self.CONTROL_STRENGTH
        OVERLAP = self.OVERLAP
        NEGATIVE_DELAY = self.NEGATIVE_DELAY
        LOG_FLOOR = self.LOG_FLOOR
        delay11, delay10, delay01, delay00 = self.delay11, self.delay10, self.delay01, self.delay00

        sr, host_signal = wavfile.read(origin_filename)
        signal_len = len(host_signal)

        # 帧的移动量
        frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))

        # 和相邻帧的重叠长度
        overlap_length = int(FRAME_LENGTH * OVERLAP)

        # 可嵌入总比特数
        embed_nbit_ = (signal_len - overlap_length) // frame_shift

        # 重复次数
        n_repeat = embed_nbit_ // len(wm_bits)

        # 实际可嵌入的有效比特数
        len_wm_bits = len(wm_bits)
        # 实际嵌入
        embed_nbit = len_wm_bits * n_repeat

        if self.verbose:
            print(
                f"可以嵌入的总比特数为: {embed_nbit_}，水印长度为{len(wm_bits)},重复嵌入 {n_repeat} 次, 实际嵌入{embed_nbit}")

        # 扩展水印信号
        wmark_extended = np.repeat(wm_bits, n_repeat)

        # 生成密钥
        np.random.seed(pwd)
        secret_key = np.random.randint(2, size=int(len_wm_bits))
        secret_key_extended = np.repeat(secret_key, n_repeat)

        pointer = 0
        echoed_signal1 = np.zeros((frame_shift * embed_nbit))
        prev1 = np.zeros((FRAME_LENGTH))
        de = NEGATIVE_DELAY  #
        for i in range(embed_nbit):
            frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

            if secret_key_extended[i] == 1:
                if wmark_extended[i] == 1:
                    delay = delay11
                else:
                    delay = delay10
            else:
                if wmark_extended[i] == 1:
                    delay = delay01
                else:
                    delay = delay00

            echo_positive = CONTROL_STRENGTH \
                            * np.concatenate((np.zeros(delay),
                                              frame[0:FRAME_LENGTH - delay]))

            echo_negative = - CONTROL_STRENGTH \
                            * np.concatenate((np.zeros(delay + de),
                                              frame[0:FRAME_LENGTH - delay - de]))

            echo_forward = CONTROL_STRENGTH \
                           * np.concatenate((frame[delay:FRAME_LENGTH], np.zeros(delay)))

            if algo_type == 1:
                echoed_frame1 = frame + echo_positive
            elif algo_type == 2:
                echoed_frame1 = frame + echo_positive + echo_negative
            else:  # algo_type == 3
                echoed_frame1 = frame + echo_positive + echo_forward

            echoed_frame1 = echoed_frame1 * windows.hann(FRAME_LENGTH)
            echoed_signal1[frame_shift * i: frame_shift * (i + 1)] = \
                np.concatenate((prev1[frame_shift:FRAME_LENGTH] +
                                echoed_frame1[0:overlap_length],
                                echoed_frame1[overlap_length:frame_shift]))

            prev1 = echoed_frame1
            pointer = pointer + frame_shift

        echoed_signal1 = np.concatenate(
            (echoed_signal1, host_signal[len(echoed_signal1): signal_len]))

        # 将保存为wav格式
        echoed_signal1 = echoed_signal1.astype(np.int16)
        wavfile.write(embed_filename, sr, echoed_signal1)

    def extract(self, embed_filename, len_wm_bits):
        pwd = self.pwd
        algo_type = self.algo_type
        FRAME_LENGTH = self.FRAME_LENGTH
        CONTROL_STRENGTH = self.CONTROL_STRENGTH
        OVERLAP = self.OVERLAP
        NEGATIVE_DELAY = self.NEGATIVE_DELAY
        LOG_FLOOR = self.LOG_FLOOR
        delay11, delay10, delay01, delay00 = self.delay11, self.delay10, self.delay01, self.delay00

        # 打开已嵌入水印的音频文件
        _, eval_signal1 = wavfile.read(embed_filename)
        signal_len = len(eval_signal1)

        frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))
        embed_nbit_ = (signal_len - int(FRAME_LENGTH * OVERLAP)) // frame_shift

        # 重复次数
        n_repeat = embed_nbit_ // len_wm_bits

        # 实际可嵌入的有效比特数
        embed_nbit = len_wm_bits * n_repeat

        if self.verbose:
            print(
                f"可以嵌入的总比特数为: {embed_nbit_}，水印长度为{len_wm_bits},重复嵌入 {n_repeat} 次, 实际嵌入{embed_nbit}")

        # 加载密钥
        np.random.seed(pwd)
        secret_key = np.random.randint(2, size=int(len_wm_bits))
        secret_key = np.repeat(secret_key, n_repeat)

        pointer = 0
        detected_bit1 = np.zeros(embed_nbit)
        for i in range(embed_nbit):
            wmarked_frame1 = eval_signal1[pointer: pointer + FRAME_LENGTH]
            ceps1 = np.fft.ifft(
                np.log(np.square(np.fft.fft(wmarked_frame1)) + LOG_FLOOR)).real

            if secret_key[i] == 1:
                if algo_type == 1:
                    if ceps1[delay11] > ceps1[delay10]:
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0
                elif algo_type == 2:
                    if (ceps1[delay11] - ceps1[delay11 + NEGATIVE_DELAY]) > \
                            (ceps1[delay10] - ceps1[delay10 + NEGATIVE_DELAY]):
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0
                else:  # algo_type == 3
                    if ceps1[delay11] > ceps1[delay10]:
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0

            else:
                if algo_type == 1:
                    if ceps1[delay01] > ceps1[delay00]:
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0
                elif algo_type == 2:
                    if (ceps1[delay01] - ceps1[delay01 + NEGATIVE_DELAY]) > \
                            (ceps1[delay00] - ceps1[delay00 + NEGATIVE_DELAY]):
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0
                else:
                    if ceps1[delay01] > ceps1[delay00]:
                        detected_bit1[i] = 1
                    else:
                        detected_bit1[i] = 0

            pointer = pointer + frame_shift

        count = 0
        wmark_recovered1 = np.zeros(len_wm_bits)
        # wmark_recovered2 = np.zeros(len_wm_bits)
        # wmark_recovered3 = np.zeros(len_wm_bits)

        for i in range(len_wm_bits):

            # 汇总比特值（平均值）
            ave = np.sum(detected_bit1[count:count + n_repeat]) / n_repeat
            if ave >= 0.5:
                wmark_recovered1[i] = 1
            else:
                wmark_recovered1[i] = 0

            count = count + n_repeat

        return wmark_recovered1


def get_error_rate(wmark_recovered, wm_bits):
    # 计算错误率
    len_wm_bits = len(wm_bits)
    denom = np.sum(np.abs(wmark_recovered - wm_bits))
    BER = np.sum(np.abs(wmark_recovered - wm_bits)) / \
          len_wm_bits * 100
    print(f'bit error rate = {BER:.2f}% ({denom} / {len_wm_bits})')
    return BER


def get_snr(wav_with_wm, orig_file):
    sr, host_signal = wavfile.read(orig_file)
    _, eval_signal1 = wavfile.read(wav_with_wm)

    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal1.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')
    return SNR

