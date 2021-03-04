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

from .metrics import compute_STOI, compute_SNR
from .utils import find_aligned_wav_files, find_wav_files


def comp(
        noisy_dir="./noisy",  # input of the network
        clean_dir="./clean",  # target of the network
        denoised_dir="./denoised", # output of the network
        purenoise_dir = "./purenoise", # the pure noise...
        sr=8000, 
        limit=0, 
        offset=0, 
        output_path="./output.xls"):
    noisy_dir = Path(noisy_dir)
    clean_dir = Path(clean_dir)
    denoised_dir = Path(denoised_dir)
    purenoise_dir = Path(purenoise_dir)

    noisy_wav_paths = find_wav_files(noisy_dir.as_posix(), limit=limit, offset=offset)
    clean_wav_paths = find_wav_files(clean_dir.as_posix(),limit=limit, offset=offset)
    denoised_wav_paths = find_wav_files(denoised_dir.as_posix(), limit=limit, offset=offset)
    purenoise_wav_paths = find_wav_files(purenoise_dir.as_posix(), limit=limit, offset=offset)

    noisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(noisy_wav_paths, desc="Loading noisy wavs..")]
    clean_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(clean_wav_paths, desc="Loading clean wavs..")]
    denoised_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(denoised_wav_paths, desc="Loading denoised wavs..")]
    purenoise_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(purenoise_wav_paths, desc="Loading purenoise wavs..")]
    
    assert (len(noisy_wavs) == len(clean_wavs) == len(denoised_wavs) == len(purenoise_wavs)), f"{noisy_wavs} or {clean_wavs} or {denoised_wavs} or {purenoise_wavs} are not equal in length"

    headers = (
        "Filename", 
        "type of noise", 
        "SNR clean vs noisy",
        "SNR clean vs denoised",
        "STOI clean vs noisy", 
        "STOI clean vs denoised", 
        "STOI Improvement",
        "STOI Improvement alternative", # just subtracting the two STOIs
    )  
    metrics_seq = []

    for i, (noisy_wav, clean_wav, denoised_wav, purenoise_wav) in tqdm(
            enumerate(zip(noisy_wavs, clean_wavs, denoised_wavs, purenoise_wavs)), desc="Calculate the evaluation metrices"
    ):
        lengths = [len(noisy_wav), len(clean_wav), len(denoised_wav), len(purenoise_wav)]
        lengths.sort()
        shorter_length = lengths[0]
        stoi_c_n = compute_STOI(clean_wav, noisy_wav)
        stoi_c_d = compute_STOI(clean_wav, denoised_wav)
        snr_noisysignal_purenoise = compute_SNR(noisy_wav, purenoise_wav)
        snr_denoisedsignal_purenoise = compute_SNR(denoised_wav, purenoise_wav)

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
                round((stoi_c_d - stoi_c_n) / stoi_c_n, 4),
                round((stoi_c_d - stoi_c_n), 4)
            )
        )

    data = tablib.Dataset(*metrics_seq, headers=headers)
    print(f"Done, output path : {output_path}.")
    with open(output_path, "wb") as f:
        f.write(data.export("xls"))