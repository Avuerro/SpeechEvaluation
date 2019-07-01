from pystoi.stoi import stoi
import os
import multiprocessing
import math
import numpy as np
import mir_eval
# from pypesq import pesq

def compute_STOI(clean_signal, noisy_signal, sr=8000): # changed framerate from 16000 to 8000
    min_length = min(len(clean_signal),len(noisy_signal))
    stoi_val = stoi(clean_signal[:min_length], noisy_signal[:min_length], sr, extended=False)
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

def compute_SDR(clean_signal,clean_predicted, noisy_signal,noisy_predicted, framerate = 8000):
    references = [clean_signal,noisy_signal]
    estimations = [clean_predicted,noisy_predicted]

    min_length = min(len(clean_signal), len(noisy_signal), len(clean_predicted), len(noisy_predicted))
    print(min_length)
    sdr, _, _, _, _ = mir_eval.separation.bss_eval_images([clean_signal[:min_length],noisy_signal[:min_length]],[clean_predicted[:min_length],noisy_predicted[:min_length]]) # clean predicted = noisy_output... # noisy_signal is pure noise
    print(sdr)
    return sdr[0],sdr[1]

def compute_SDR_single(references, estimates, framerate=8000):
    min_length = min(len(references), len(estimates))

    sdr, _, _, _, _ = mir_eval.separation.bss_eval_images(references, estimates)
    return sdr

# def _compute_PESQ_sub_task(clean_signal, noisy_siganl, sr=16000):
#     return pesq(clean_signal, noisy_siganl, sr)

# def compute_PESQ(clean_signal, noisy_signal, sr=16000):
#     """
#     使用 pypesq 计算 pesq 评价指标。
#     Notes：
#         pypesq 是 PESQ 官方代码（C 语言）的 wrapper。官方代码在某些语音上会报错，而其报错时直接调用了 exit() 函数，直接导致 Python 脚本停止运行，亦无法捕获异常，实在过于粗鲁。
#         为了防止 Python 脚本被打断，这里使用子进程执行 PESQ 评价指标的计算，设置子进程的超时。
#         设置子进程超时的方法：https://stackoverflow.com/a/29378611
#     Returns:
#         当语音可以计算 pesq score 时，返回 pesq score，否则返回 -1
#     """
#     return pesq(clean_signal, noisy_signal, sr)
    # pool = multiprocessing.Pool(1)`
    # rslt = pool.apply_async(_compute_PESQ_sub_task, args = (clean_signal, noisy_signal, sr))
    # pool.close() # 关闭进程池，不运行再向内添加进程
    # rslt.wait(timeout=1) # 子进程的处理时间上限为 1 秒钟，到时未返回结果，则终止子进程
    #
    # if rslt.ready(): # 在 1 秒钟内子进程处理完毕
    #     return rslt.get()
    # else: # 过了 1 秒了，但仍未处理完，返回 -1
    #     return -1