from tqdm import tqdm
import requests
import os


FILE_NAME = 'data.xml.bz2'
FINAL_FILE_NAME = 'data.xml'


def needs_to_download():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        return False

    if os.path.exists(FINAL_FILE_NAME) and os.path.getsize(FINAL_FILE_NAME) > 0:
        return False

    return True


def download():
    if not needs_to_download(): return

    print('downloading')

    url = 'https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles-multistream.xml.bz2'

    session = requests.Session()
    download_handle = session.get(url, stream=True)
    download_handle.raise_for_status()

    progress_bar_iterator = tqdm(
        download_handle.iter_content(chunk_size=1024 * 1024),
        mininterval=0.1,
        unit='MB',
        unit_scale=True,
        unit_divisor=1024
    )

    with open(FILE_NAME, 'wb') as file_handle:
        for data in progress_bar_iterator:
            file_handle.write(data)

    print('download finished')
