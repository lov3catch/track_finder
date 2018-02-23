# -*-coding: utf-8;-*-
from urllib.parse import urljoin

import requests

from handlers.mail_ru.async_page_checker import get_total_track_count
from handlers.mail_ru.audio_parsers import prepare_result, make_query, get_download_url

SEARCH_URL = 'http://go.mail.ru/zaycev?{query}'
DOWNLOAD_URL = 'http://zaycev.net'


def normalize_song_name(song_name):
    return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name, limit, offset):
    page = offset2page(offset)
    search_page_url = SEARCH_URL.format(query=make_query(normalized_song_name, page))
    print(search_page_url)
    search_page = requests.get(search_page_url)

    result = prepare_result(search_page.content.decode())
    print(result)

    offset = offset - (page -1) * 20
    print(offset)
    return result[offset:][:limit], get_total_track_count(normalized_song_name, SEARCH_URL)


def normalize_download_url(data_url):
    url = get_download_url(requests.get(data_url).content)
    if url:
        json_url = urljoin(DOWNLOAD_URL, url)
    else:
        return None
    result = requests.get(json_url).json()
    url = dict(result).get('url')
    if url:
        url = str.split(url, '?')
    if url:
        return url[0]
    return None


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