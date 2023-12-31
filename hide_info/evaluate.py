import numpy as np


def get_error_rate(wm_extract, wm_bits):
    len_wm_bits = len(wm_bits)
    error_num = np.sum(np.abs(wm_extract - wm_bits))
    error_rate = error_num / len_wm_bits
    print(f'bit error rate = {error_rate:.2%} ({error_num} / {len_wm_bits})')
    return error_rate


def get_snr(ori_signal, wm_signal):
    snr = 10 * np.log10(
        np.sum(np.square(ori_signal.astype(np.float32)))
        / np.sum(np.square(ori_signal.astype(np.float32)
                           - wm_signal.astype(np.float32))))
    print(f'SNR = {snr:.2f} dB')
    return snr
