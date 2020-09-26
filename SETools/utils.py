import os

import librosa
import numpy as np


# use this if files are already aligned
def find_wav_files(wav_files_dir, limit=0, offset=0):
    """
       finds all wav files in specified dir.
       returns a list with the filenames.
    """

    if limit == 0 :
        limit = None
    print(wav_files_dir)

    wav_files_paths = librosa.util.find_files(wav_files_dir, ext="wav", limit = limit, offset = offset)

    # Assert that there are actually files in the folder...
    cwd = os.getcwd()
    print(cwd)

    assert len(wav_files_paths) > 0, "Specified directory {} is empty".format(wav_files_dir)


    return wav_files_paths

def find_aligned_wav_files(wav_files_dir_A, wav_files_dir_B, limit=0, offset=0):
    """
    搜索目录中的 wav 文件，并要求两个目录中的 wav *文件数量相等*且*文件名一一对应*
    Args:
        wav_files_dir_A:
        wav_files_dir_B:
        limit: 加载文件的数量限制

    Returns:
        length:
            1. limit == None时，length = 实际数量
            2. limit <= len(wav_file_paths_A) 时，length = limit
            2. limit > len(wav_file_paths_A) 时，length = 实际数量
    """
    if limit == 0:
        limit = None  
    wav_file_paths_A = librosa.util.find_files(wav_files_dir_A, ext="wav", limit=limit, offset=offset)
    wav_file_paths_B = librosa.util.find_files(wav_files_dir_B, ext="wav", limit=limit, offset=offset)
    cwd = os.getcwd()

    assert len(wav_file_paths_A) == len(wav_file_paths_B) > 0, \
        "目录 {} 和目录 {} 文件数量不同或目录为空".format(wav_files_dir_A, wav_files_dir_B)

    length = len(wav_file_paths_A)

    return wav_file_paths_A, wav_file_paths_B, length

