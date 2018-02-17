# -*-coding: utf-8;-*-
from urllib.parse import urljoin

import requests

from handlers.mail_ru.audio_parsers import prepare_result, make_query, get_download_url

SEARCH_URL = 'http://go.mail.ru/zaycev?{song_name}'
DOWNLOAD_URL = 'http://zaycev.net'


def normalize_song_name(song_name):
    return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name, limit, offset):
    page = offset2page(offset)
    search_page_url = SEARCH_URL.format(song_name=make_query(normalized_song_name, page))
    print(search_page_url)
    search_page = requests.get(search_page_url)

    result = prepare_result(search_page.content.decode())
    print(result)

    offset = offset - (page -1) * 20
    print(offset)
    return result[offset:][:limit]


def normalize_download_url(data_url):
    return get_download_url(requests.get(data_url).content)

def offset2page(offset):
    track_per_page = 20

    if (offset == 0):
        return 1

    available_offsets = list(range(0, 1000, 5))
    print(available_offsets)

    if (offset in available_offsets):
        return offset // track_per_page + 1

    return  1

    # page = offset / track_per_page


if __name__ == '__main__':
    data_urls = parse_result(normalize_song_name('The Hardkiss'), 100, 0)
    print(normalize_download_url(data_urls[0][1]))