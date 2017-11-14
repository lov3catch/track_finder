from bs4 import BeautifulSoup


def prepare_result(html):
    result = []

    try:
        result_div_html = find_result_div(html)
        result_items_html = find_result_items(result_div_html)

        for result_item in result_items_html:
            artist = find_artist_name(result_item)
            song = find_song_title(result_item)
            data_url = find_data_url(result_item)
            result.append(('{} - {}'.format(artist, song), data_url))
    except Exception as ex:
        print(ex)

    return result


def find_result_div(html):
    parser = BeautifulSoup(html, "html.parser")
    return parser.find('div', {'class': 'musicset-track-list__items'})


def find_result_items(bs_tag):
    return bs_tag.findAll('div', {'class': 'musicset-track clearfix'})


def find_artist_name(bs_tag):
    return bs_tag.find('div', {'class': 'musicset-track__artist'}).find('a', {'class': 'musicset-track__link'}).text


def find_song_title(bs_tag):
    return bs_tag.find('div', {'class': 'musicset-track__track-name'}).find('a', {'class': 'musicset-track__link'}).text


def find_data_url(bs_tag):
    return bs_tag.get('data-url')


if __name__ == '__main__':
    import requests

    url = 'http://zaycev.net/search.html?query_search=kasabian'
    html = requests.get(url).content.decode()
    result_div_html = find_result_div(html)
    result_items_html = find_result_items(result_div_html)

    for result_item in result_items_html:
        artist = find_artist_name(result_item)
        song = find_song_title(result_item)
        data_url = find_data_url(result_item)

        print('{} - {} :: {}'.format(artist, song, data_url))
