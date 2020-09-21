import json

def store(frequency_list):
    sorted_frequency_list = sort_and_normalize(frequency_list)

    with open('frequency.json', 'wt', encoding='utf8') as f_handle:
        json.dump(sorted_frequency_list, f_handle, ensure_ascii=False, indent=2)


def sort_and_normalize(frequency_list):
    sorted_frequency_list = {
        # pylint: disable=unnecessary-comprehension
        k: v for k, v in sorted(
            frequency_list.items(),
            key=lambda item: item[1],
            reverse=True
        )
    }

    return sorted_frequency_list
