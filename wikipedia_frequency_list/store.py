import json

from .processor import sort_and_normalize

def store(frequency_list):
    sorted_frequency_list = sort_and_normalize(frequency_list)

    with open('frequency.json', 'wt', encoding='utf8') as f_handle:
        json.dump(sorted_frequency_list, f_handle, ensure_ascii=False, indent=2)
