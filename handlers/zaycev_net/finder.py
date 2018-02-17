# -*-coding: utf-8;-*-
from urllib.parse import urljoin

import requests

from handlers.zaycev_net.audio_parsers import prepare_result

SEARCH_URL = 'http://zaycev.net/search.html?query_search={song_name}'
DOWNLOAD_URL = 'http://zaycev.net'


def normalize_song_name(song_name):
    return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name, limit, offset):
    search_page_url = SEARCH_URL.format(song_name=normalized_song_name)
    search_page = requests.get(search_page_url)

    result = prepare_result(search_page.content.decode())
    return result[offset:][:limit]


def normalize_download_url(data_url):
    url = urljoin(DOWNLOAD_URL, data_url)
    result = requests.get(url).json()
    url = dict(result).get('url')
    if url:
        url = str.split(url, '?')
    if url:
        return url[0]
    return None


if __name__ == '__main__':
    data_urls = parse_result(normalize_song_name('The Hardkiss'), 100, 0)
    print(normalize_download_url(data_urls[0][1]))
