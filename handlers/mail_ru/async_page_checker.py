# -*-coding: utf-8;-*-
import asyncio
import time
from urllib.parse import urlencode

import grequests
from bs4 import BeautifulSoup

MIN_DEPTH = 1
MAX_DEPTH = 5


async def get_count_on_page(request_result):
    parser = BeautifulSoup(request_result.content, 'html.parser')
    result = parser.find('ul', {'class': 'result js-result'})
    if (result):
        return len(result.findAll('li', {'class': 'result__li'}))
    return 0


def scraping_pages_by_urls(urls):
    return grequests.map([grequests.get(url) for url in urls])


def get_total_track_count(track_name, base_url, min_depth=MIN_DEPTH, max_depth=MAX_DEPTH):
    urls = [base_url.format(query=urlencode({'q': track_name, 'page': page_number})) for page_number in
            range(min_depth, max_depth)]
    request_results = scraping_pages_by_urls(urls)

    tasks = [get_count_on_page(request_result) for request_result in request_results]

    loop = asyncio.get_event_loop()
    results, _ = loop.run_until_complete(asyncio.wait(tasks))

    return sum([result.result() for result in results])


if __name__ == '__main__':
    track_name = 'hardkiss'
    base_url = 'https://go.mail.ru/zaycev?{query}'

    start = time.time()
    total_count = get_total_track_count(track_name, base_url)
    finish = time.time()

    print('Total {}'.format(total_count))
    print('Time: {}'.format(finish - start))
