from pystoi.stoi import stoi
import os
import multiprocessing
import math
import numpy as np
import mir_eval

def compute_STOI(clean_signal, noisy_signal, sr=8000):
    stoi_val = stoi(clean_signal, noisy_signal, sr, extended=False)
    compute_SDR(clean_signal, noisy_signal)
    return round(stoi_val,4)

def compute_POWER(input_signal):
    print(input_signal.shape)
    N = len(input_signal)
    power = 1/N * np.sum(input_signal ** 2, axis=0)
    return power

def compute_SNR(clean_signal, noisy_signal):
    p_signal = compute_POWER(clean_signal)
    p_noise = compute_POWER(noisy_signal)
    snr = 10 *  math.log10(p_signal/p_noise)
    snr_nolog = p_signal/p_noise
    return round(snr,4)

def compute_SDR(clean_signal, noisy_signal, framerate = 8000):
    sdr, _, _, _, _ = mir_eval.separation.bss_eval_images(clean_signal,noisy_signal)
    return sdr