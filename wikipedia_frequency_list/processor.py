import bz2
import os
# import MeCab

from .downloader import FILE_NAME, FINAL_FILE_NAME


def extract():
    if os.path.exists(FINAL_FILE_NAME) and os.path.getsize(FINAL_FILE_NAME) > 0:
        return

    print('extracing data')
    decomp = bz2.BZ2Decompressor()

    # This doesnt work
    with open(FILE_NAME, 'rb') as compressed_file_handle:
        with open(FINAL_FILE_NAME, 'wb') as output_file_handle:
            while True:
                raw_data = compressed_file_handle.read(16384)

                if len(raw_data) == 0:
                    break

                data = decomp.decompress(raw_data)
                output_file_handle.write(data)


def process():
    return []
