#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import time
from pathlib import Path
import librosa
import tablib
from tqdm import tqdm
import os

from metrics import compute_STOI, compute_SNR
from utils import find_aligned_wav_files, find_wav_files


def comp(
        noisy_dir="./noisy",  # input of the network
        clean_dir="./clean",  # target of the network
        denoised_dir="./denoised", # output of the network
        purenoise_dir = "./purenoise", # the pure noise...
        sr=8000, 
        limit=0, 
        offset=0, 
        output_path="./output.xls"):
    print("diaoyongle cal()")
    noisy_dir = Path(noisy_dir)
    clean_dir = Path(clean_dir)
    denoised_dir = Path(denoised_dir)
    purenoise_dir = Path(purenoise_dir)
    print(noisy_dir)
    # input -- pure noise
    # output -- pure noise

    # noise = mix input
    # clean = 

    noisy_wav_paths = find_wav_files(noisy_dir.as_posix(), limit=limit, offset=offset)
    clean_wav_paths = find_wav_files(clean_dir.as_posix(),limit=limit, offset=offset)
    denoised_wav_paths = find_wav_files(denoised_dir.as_posix(), limit=limit, offset=offset)
    purenoise_wav_paths = find_wav_files(purenoise_dir.as_posix(), limit=limit, offset=offset)


    # noisy_wav_paths, clean_wav_paths, shorter_length = find_aligned_wav_files(
    #     noisy_dir.as_posix(), clean_dir.as_posix(), limit=limit, offset=offset
    # )

    # denoisy_wavs_paths, _, shorter_length = find_aligned_wav_files(
    #     denoisy_dir.as_posix(), clean_dir.as_posix(), limit=limit, offset=offset
    # )

    noisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(noisy_wav_paths, desc="Loading noisy wavs..")]
    clean_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(clean_wav_paths, desc="Loading clean wavs..")]
    denoised_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(denoised_wav_paths, desc="Loading denoised wavs..")]
    purenoise_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(purenoise_wav_paths, desc="Loading purenoise wavs..")]
    
    assert (len(noisy_wavs) == len(clean_wavs) == len(denoised_wavs) == len(purenoise_wavs)), f"{noisy_wavs} or {clean_wavs} or {denoised_wavs} or {purenoise_wavs} are not equal in length"

    headers = (
        "Filename", # "语音编号",
        "type of noise", # 噪声类型",
        "SNR clean vs noisy", # 信噪比",
        "SNR clean vs denoised",
        "STOI clean vs noisy", # STOI 纯净与带噪",
        "STOI clean vs denoised", #STOI 纯净与降噪 ",
        # "PESQ 纯净与带噪",
        # "PESQ 纯净与降噪",
        "STOI Improvement", # "STOI 提升",
        "STOI Improvement alt", # just subtracting the two STOIs
        # "PESQ 提升",
    )  # 定义导出为 Excel 文件的格式
    metrics_seq = []

    for i, (noisy_wav, clean_wav, denoised_wav, purenoise_wav) in tqdm(
            enumerate(zip(noisy_wavs, clean_wavs, denoised_wavs, purenoise_wavs)), desc="正在计算评价指标："
    ):
        lengths = [len(noisy_wav), len(clean_wav), len(denoised_wav), len(purenoise_wav)]
        lengths.sort()
        shorter_length = lengths[0]
        stoi_c_n = compute_STOI(clean_wav, noisy_wav)
        stoi_c_d = compute_STOI(clean_wav, denoised_wav)
        snr_noisysignal_purenoise = compute_SNR(noisy_wav, purenoise_wav)
        snr_denoisedsignal_purenoise = compute_SNR(denoised_wav, purenoise_wav)
        # pesq_c_n = compute_PESQ(clean_wav[:shorter_length], noisy_wav[:shorter_length])
        # pesq_c_d = compute_PESQ(clean_wav[:shorter_length], denoisy_wav[:shorter_length])
        
        print("---")
        print(os.path.splitext(os.path.basename(noisy_wav_paths[i])))
        print("---")
        num, noise = os.path.splitext(os.path.basename(noisy_wav_paths[i]))[
            0
        ].split("_")
        snr = "todo"
        noise = "todo"
        metrics_seq.append(
            (
                num,
                noise,
                snr_noisysignal_purenoise,
                snr_denoisedsignal_purenoise,
                stoi_c_n,
                stoi_c_d,
                # pesq_c_n,
                # pesq_c_d,
                round((stoi_c_d - stoi_c_n) / stoi_c_n, 4),
                round((stoi_c_d - stoi_c_n), 4)
                # (pesq_c_d - pesq_c_n) / pesq_c_n,
            )
        )

    data = tablib.Dataset(*metrics_seq, headers=headers)
    print(f"Done, output path : {output_path}.")
    with open(output_path, "wb") as f:
        f.write(data.export("xls"))