from wikipedia_frequency_list.downloader import download
from wikipedia_frequency_list.processor import parse, extract
from wikipedia_frequency_list.store import store


if __name__ == '__main__':
    download()
    extract()
    frequency_list = parse()
    store(frequency_list)
