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

from metrics import compute_STOI #, compute_PESQ
from utils import find_aligned_wav_files
from comp import comp

def call():

    parser = argparse.ArgumentParser(
        description="Speech Enhancement Evaluation Metrics"
    )
    parser.add_argument("--noisy_dir", required=True, type=str, help="noisy wav files directory")
    parser.add_argument("--denoised_dir", required=True, type=str, help="denoised wav files directory")
    parser.add_argument("--clean_dir", required=True, type=str, help="clean wav files directory")
    parser.add_argument("--purenoise_dir", required=True, type=str, help="pure noise wav files location")
    parser.add_argument("--predicted_noise_dir", required=True, type=str, help =" predicted noise wav files location")
    parser.add_argument("--output_path", default="./output.xls", type=str, help="output dir, filename should end on .xls")
    parser.add_argument("--limit", default=0, type=int, help="file limit, 0 means no limit")
    parser.add_argument("--offset", default=0, type=int, help="start from file with index nr")
    parser.add_argument("--sr", default=8000, type=int, help="sample rate ")

    args = parser.parse_args()
    print(args.noisy_dir)
    print("hhhh")
    comp(
        noisy_dir=args.noisy_dir,
        clean_dir=args.clean_dir,
        denoised_dir=args.denoised_dir,
        purenoise_dir = args.purenoise_dir,
        predicted_noise_dir = args.predicted_noise_dir,
        sr=args.sr,
        limit=args.limit,
        offset=args.offset,
        output_path=args.output_path,
    )

call()