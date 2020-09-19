import json

from wikipedia_frequency_list.downloader import download
from wikipedia_frequency_list.processor import process, extract


if __name__ == '__main__':
    download()
    extract()
    frequency_list = process()

    sorted_frequency_list = {
        k: v for k, v in sorted(
            frequency_list.items(),
            key=lambda item: item[1],
            reverse=True
        )
    }

    with open('frequency.json', 'wt', encoding='utf8') as f:
        json.dump(sorted_frequency_list, f, ensure_ascii=False, indent=2)
