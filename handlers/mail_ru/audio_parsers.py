from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

TRACKS_COUNT_IN_PAGE = 20
SEARCH_URL = 'http://go.mail.ru/zaycev?{}'


def get_result_div(html):
    parser = BeautifulSoup(html, "html.parser")
    return parser.find('ul', {'class': 'result js-result'})


def get_track_list(result_html):
    return result_html.findAll('li', {'class': 'result__li'})


def make_query(track_name, page):
    url_params = {'q': track_name, 'page': page}
    return urlencode(url_params)

def prepare_result(html):
    result = []

    try:
        result_div_html = get_result_div(html)
        result_items_html = get_track_list(result_div_html)

        for result_item in result_items_html:
            url = result_item.find('div', {'class': 'zaycev__play'}).find('a')['href']
            title = result_item.find('div', {'class': 'zaycev__block'}).find('h3', {'class': 'result__title'}).find('a',
                                                                                                                    {
                                                                                                                        'class': 'light-link'}).text
            result.append((title, url.split('?')[0], 'mail_ru'))
    except Exception as ex:
        print(ex)

    return result

def get_download_url(html):
    parser = BeautifulSoup(html, "html.parser")
    result_div_html = parser.find('div', {'class': 'musicset-track-list__items'})
    result_items_html = result_div_html.findAll('div', {'class': 'musicset-track clearfix'})

    for result_item in result_items_html:
        return result_item.get('data-url')


    # find_result_items = parser.find('div', {'class': 'audiotrack-button audiotrack-button_download'})
    # if (find_result_items):
    #     return find_result_items[0].get('data-url')
        # return download_div.find('a', {'class': 'audiotrack-button__label track-geo__button track-geo__link hover-bound'})['href']



if __name__ == '__main__':
    # track_list_url = SEARCH_URL.format(make_query('The Hardkiss', 1))
    #
    # html = requests.get(track_list_url).content
    #
    # result = get_result_div(html)
    #
    # track_list_html = get_track_list(result)
    #
    # for track_block in track_list_html:
    #     url = track_block.find('div', {'class': 'zaycev__play'}).find('a')['href']
    #     title = track_block.find('div', {'class': 'zaycev__block'}).find('h3', {'class': 'result__title'}).find('a', {
    #         'class': 'light-link'}).text
    #     print('{} :: {}'.format(title, url))

    url = 'http://zaycev.net/pages/39469/3946953.shtml?autoplay=1'
    print(get_download_url(requests.get(url).content))

