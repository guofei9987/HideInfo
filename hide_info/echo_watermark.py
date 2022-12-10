# 回声音频水印
import numpy as np
from scipy.io import wavfile
from scipy.signal import windows
from numpy.fft import ifft


class EchoWatermark:
    def __init__(self, pwd, algo_type=2, verbose=False):
        self.pwd = pwd
        self.algo_type = algo_type
        self.verbose = verbose

        self.frame_len = 2048  # 帧长度
        self.echo_amplitude = 0.2  # 回声幅度
        self.overlap = 0.5  # 帧分析的重叠率
        self.neg_delay = 4  # negative delay, for negative echo

        # 回声参数
        # pwd[i] = 1
        self.delay11, self.delay10 = 100, 110
        # pwd[i] = 0
        self.delay01, self.delay00 = 120, 130

    def embed(self, origin_filename, wm_bits, embed_filename):
        frame_len = self.frame_len
        echo_amplitude = self.echo_amplitude
        overlap = self.overlap
        neg_delay = self.neg_delay

        delay_matrix = [[self.delay00, self.delay01], [self.delay10, self.delay11]]

        sr, ori_signal = wavfile.read(origin_filename)
        signal_len = len(ori_signal)

        # 帧的移动量
        frame_shift = int(frame_len * (1 - overlap))

        # 和相邻帧的重叠长度
        overlap_length = int(frame_len * overlap)

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
        wm_repeat = np.repeat(wm_bits, n_repeat)

        # 生成密钥
        np.random.seed(self.pwd)
        secret_key = np.random.randint(2, size=int(len_wm_bits))
        secret_key_extended = np.repeat(secret_key, n_repeat)

        pointer = 0
        echoed_signal = np.zeros((frame_shift * embed_nbit))
        prev1 = np.zeros(frame_len)

        for i in range(embed_nbit):
            frame = ori_signal[pointer: (pointer + frame_len)]

            delay = delay_matrix[secret_key_extended[i]][wm_repeat[i]]

            echo_positive = echo_amplitude \
                            * np.concatenate(
                (np.zeros(delay), frame[0:frame_len - delay]))

            echo_negative = - echo_amplitude \
                            * np.concatenate((np.zeros(delay + neg_delay),
                                              frame[0:frame_len - delay - neg_delay]))

            echo_forward = echo_amplitude \
                           * np.concatenate((frame[delay:frame_len], np.zeros(delay)))

            if self.algo_type == 1:
                echoed_frame = frame + echo_positive
            elif self.algo_type == 2:
                echoed_frame = frame + echo_positive + echo_negative
            else:  # algo_type == 3
                echoed_frame = frame + echo_positive + echo_forward

            echoed_frame = echoed_frame * windows.hann(frame_len)
            echoed_signal[frame_shift * i: frame_shift * (i + 1)] = \
                np.concatenate((prev1[frame_shift:frame_len] +
                                echoed_frame[0:overlap_length],
                                echoed_frame[overlap_length:frame_shift]))

            prev1 = echoed_frame
            pointer += frame_shift

        echoed_signal = np.concatenate((echoed_signal, ori_signal[len(echoed_signal):])).astype(np.int16)
        # 将保存为wav格式
        wavfile.write(embed_filename, sr, echoed_signal)

    def extract(self, embed_filename, len_wm_bits):
        frame_len = self.frame_len
        overlap = self.overlap
        neg_delay = self.neg_delay
        delay11, delay10, delay01, delay00 = self.delay11, self.delay10, self.delay01, self.delay00
        log_floor = 0.00001  # 取对数时的最小值

        # 打开已嵌入水印的音频文件
        _, wm_signal = wavfile.read(embed_filename)
        signal_len = len(wm_signal)

        frame_shift = int(frame_len * (1 - overlap))
        embed_nbit_ = (signal_len - int(frame_len * overlap)) // frame_shift

        # 重复次数
        n_repeat = embed_nbit_ // len_wm_bits

        # 实际可嵌入的有效比特数
        embed_nbit = len_wm_bits * n_repeat

        if self.verbose:
            print(
                f"可以嵌入的总比特数为: {embed_nbit_}，水印长度为{len_wm_bits},重复嵌入 {n_repeat} 次, 实际嵌入{embed_nbit}")

        # 加载密钥
        np.random.seed(self.pwd)
        secret_key = np.random.randint(2, size=int(len_wm_bits))
        secret_key = np.repeat(secret_key, n_repeat)

        pointer = 0
        detected_bit1 = np.zeros(embed_nbit)
        for i in range(embed_nbit):
            wmarked_frame1 = wm_signal[pointer: pointer + frame_len]
            ceps1 = ifft(
                np.log(np.square(np.fft.fft(wmarked_frame1)) + log_floor)).real

            if secret_key[i] == 1:
                delay0, delay1 = delay10, delay11
            else:
                delay0, delay1 = delay00, delay01

            if self.algo_type == 1:
                if ceps1[delay1] > ceps1[delay0]:
                    detected_bit1[i] = 1
            elif self.algo_type == 2:
                if (ceps1[delay1] - ceps1[delay1 + neg_delay]) > \
                        (ceps1[delay0] - ceps1[delay0 + neg_delay]):
                    detected_bit1[i] = 1
            else:  # algo_type == 3
                if ceps1[delay1] > ceps1[delay0]:
                    detected_bit1[i] = 1

            pointer = pointer + frame_shift

        count = 0
        wm_extract = np.zeros(len_wm_bits)

        for i in range(len_wm_bits):
            # 汇总比特值（按平均值）
            ave = np.sum(detected_bit1[count:count + n_repeat]) / n_repeat
            if ave >= 0.5:
                wm_extract[i] = 1
            else:
                wm_extract[i] = 0

            count = count + n_repeat

        return wm_extract


def get_error_rate(wm_extract, wm_bits):
    # 计算错误率
    len_wm_bits = len(wm_bits)
    error_num = np.sum(np.abs(wm_extract - wm_bits))
    error_rate = error_num / len_wm_bits
    print(f'bit error rate = {error_rate:.2%} ({error_num} / {len_wm_bits})')
    return error_rate


def get_snr(file_with_wm, orig_file):
    sr, ori_signal = wavfile.read(orig_file)
    _, wm_signal = wavfile.read(file_with_wm)

    SNR = 10 * np.log10(
        np.sum(np.square(ori_signal.astype(np.float32)))
        / np.sum(np.square(ori_signal.astype(np.float32)
                           - wm_signal.astype(np.float32))))
    print(f'SNR = {SNR:.2f} dB')
    return SNR
