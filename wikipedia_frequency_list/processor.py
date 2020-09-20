import bz2
import os
import re
import MeCab

from tqdm import tqdm

from .downloader import FILE_NAME, FINAL_FILE_NAME


def extract():
    if os.path.exists(FINAL_FILE_NAME) and os.path.getsize(FINAL_FILE_NAME) > 0:
        return

    print('extracing data')

    file_size = os.path.getsize(FILE_NAME)

    progress_bar = tqdm(
        total=file_size,
        mininterval=0.5,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    )

    decomp = bz2.BZ2Decompressor()

    compressed_file_handle = open(FILE_NAME, 'rb')
    output_file_handle = open(FINAL_FILE_NAME, 'wb')

    bytes_read = 0

    while True:
        raw_data = compressed_file_handle.read(16384)
        bytes_read = len(raw_data)
        progress_bar.update(bytes_read)

        if len(raw_data) == 0:
            break

        data = decomp.decompress(raw_data)
        output_file_handle.write(data)


def process():
    print('parsing')

    frequency_list = {}
    chunk_size = 1024 * 32
    bytes_read = 0
    filesize = os.path.getsize(FINAL_FILE_NAME)

    progress_bar = tqdm(
        total=filesize,
        mininterval=0.1,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    )

    with open(FINAL_FILE_NAME, 'rt') as file_handle:
        reader_buffer = ''

        while True:
            chunk = file_handle.read(chunk_size)
            lines = (reader_buffer + chunk).split('\n')

            reader_buffer = lines.pop()

            for line in lines:
                parse_line(frequency_list, line)

            bytes_read = len(chunk.encode('utf-8'))
            progress_bar.update(bytes_read)

    return frequency_list


def parse_line(frequency_list, line):
    wakati = MeCab.Tagger("-Owakati")
    tokens = wakati.parse(line).split()

    for token in tokens:
        token = re.sub(r'[a-zA-Z0-9]+', '', token)
        token = re.sub(r'^\W+', '', token)

        if len(token) == 0 or token[0] == '_':
            continue

        if token not in frequency_list.keys():
            frequency_list[token] = 1
        else:
            frequency_list[token] += 1


def sort_and_normalize(frequency_list):
    sorted_frequency_list = {
        k: v for k, v in sorted(
            frequency_list.items(),
            key=lambda item: item[1],
            reverse=True
        )
    }

    return sorted_frequency_list
