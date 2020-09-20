import bz2
import os
import re
import MeCab

from tqdm import tqdm
from multiprocessing import Process, Lock, Queue, cpu_count

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
    chunk_size = 1024 * 64
    bytes_read = 0
    filesize = os.path.getsize(FINAL_FILE_NAME)

    progress_bar = tqdm(
        total=filesize,
        mininterval=0.1,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    )

    total_bytes_read = 0
    n_processes = cpu_count()
    lock = Lock()
    queue = Queue(maxsize=10)

    processes = [
        Process(target=p_processor, args=(lock, queue, frequency_list))
        for i in range(n_processes)
    ]

    for process in processes:
        process.start()

    with open(FINAL_FILE_NAME, 'rt') as file_handle:
        reader_buffer = ''

        while True:
            chunk = file_handle.read(chunk_size)
            lines = (reader_buffer + chunk).split('\n')

            reader_buffer = lines.pop()

            queue.put(lines)

            bytes_read = len(chunk.encode('utf-8'))
            total_bytes_read += bytes_read
            progress_bar.update(bytes_read)

            if total_bytes_read > 1024 ** 2 * 10:
                break

    for _ in processes:
        queue.put('die')

    for process in processes:
        process.join()

    return frequency_list


def p_processor(lock, queue, frequency_list):
    while True:
        lines = queue.get()

        if lines == 'die':
            break

        temp_frequency_list = {}

        for line in lines:
            parse_line(temp_frequency_list, line)

        lock.acquire()

        try:
            for key, value in temp_frequency_list.items():
                if key not in frequency_list.keys():
                    frequency_list[key] = value
                else:
                    frequency_list[key] += value
        finally:
            lock.release()


def parse_line(frequency_list, line):
    clean_line = re.sub(r'[a-zA-Z0-9]+', '', line)
    clean_line = re.sub(r'^\W+', '', clean_line)
    clean_line = re.sub(r'\W+', '', clean_line)

    if len(clean_line) == 0:
        return

    wakati = MeCab.Tagger("-Owakati")
    tokens = wakati.parse(clean_line).split()

    if len(tokens) == 0:
        return

    for token in tokens:
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
