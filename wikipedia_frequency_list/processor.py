import bz2
import os
import re
import time

from multiprocessing import Process, Queue, cpu_count
from tqdm import tqdm

# pylint: disable=import-error
import MeCab

from .downloader import FILE_NAME, FINAL_FILE_NAME
from .store import store


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


def parse():
    print('parsing')

    frequency_list = {}
    bytes_read = 0


    progress_bar = tqdm(
        total=os.path.getsize(FINAL_FILE_NAME),
        mininterval=0.1,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    )

    input_queue = Queue(maxsize=100)
    output_queue = Queue()

    processes = [
        Process(target=p_processor, args=(input_queue, output_queue))
        for i in range(cpu_count())
    ]

    for process in processes:
        process.start()

    with open(FINAL_FILE_NAME, 'rt') as file_handle:
        reader_buffer = ''
        last_disk_save = time.time()

        while True:
            chunk = file_handle.read(1024 * 64)
            lines = (reader_buffer + chunk).split('\n')

            reader_buffer = lines.pop()

            input_queue.put(lines)

            bytes_read = len(chunk.encode('utf-8'))
            progress_bar.update(bytes_read)

            if not output_queue.empty():
                partial_frequency_list = output_queue.get()
                update_frequency_list(frequency_list, partial_frequency_list)

            if (time.time() - last_disk_save) > 60 * 5:
                last_disk_save = time.time()
                store(frequency_list)

    for _ in processes:
        input_queue.put('die')

    for _ in processes:
        partial_frequency_list = output_queue.get()
        update_frequency_list(frequency_list, partial_frequency_list)

    for process in processes:
        process.join()

    return frequency_list


def update_frequency_list(frequency_list, delta):
    for key, value in delta.items():
        try:
            frequency_list[key] += value
        except KeyError:
            frequency_list[key] = value


def p_processor(input_queue, output_queue):
    frequency_list = {}

    while True:
        lines = input_queue.get()

        if lines == 'die':
            break

        for line in lines:
            parse_line(frequency_list, line)

        if len(frequency_list) > 10000:
            output_queue.put(frequency_list)
            frequency_list = {}

    output_queue.put(frequency_list)


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
