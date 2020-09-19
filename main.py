import json

from wikipedia_frequency_list.downloader import download
from wikipedia_frequency_list.processor import process, extract, sort_and_normalize


if __name__ == '__main__':
    download()
    extract()
    frequency_list = process()
    sorted_frequency_list = sort_and_normalize(frequency_list)

    with open('frequency.json', 'wt', encoding='utf8') as f:
        json.dump(sorted_frequency_list, f, ensure_ascii=False, indent=2)
