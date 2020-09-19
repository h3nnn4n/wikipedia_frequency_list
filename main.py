from wikipedia_frequency_list.downloader import download
from wikipedia_frequency_list.processor import process, extract


if __name__ == '__main__':
    download()
    extract()
    process()

    # with open('frequency.json', 'wt') as f:
        # f.write(data)
