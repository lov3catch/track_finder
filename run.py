from flask import Flask, request
from flask import jsonify

from handlers.mail_ru.finder import normalize_download_url as mr_normalize_download_url
from handlers.zaycev_net.finder import normalize_download_url as zn_normalize_download_url


class DRIVERS:
    ZAYCEV_NET = 'zaycev_net'
    MAIL_RU = 'mail_ru'

    @classmethod
    def get_url_normalizer(cls, alias):
        normalizers = {
            cls.ZAYCEV_NET: zn_normalize_download_url,
            cls.MAIL_RU:    mr_normalize_download_url
        }
        return normalizers.get(alias)


DEFAULT_DRIVER = DRIVERS.MAIL_RU

if DEFAULT_DRIVER == DRIVERS.ZAYCEV_NET:
    from handlers.zaycev_net.finder import parse_result, normalize_song_name
else:
    from handlers.mail_ru.finder import parse_result, normalize_song_name

app = Flask(__name__)


def do_search(query, limit, offset):
    search_result, total = parse_result(normalize_song_name(query), limit, offset)

    result = {}
    result['data'] = search_result
    result['meta'] = {
        'limit':  limit,
        'offset': offset,
        'total':  total
    }

    return result


def do_download(url, provider):
    normalizer = DRIVERS.get_url_normalizer(provider)

    result = {}
    result['data'] = {'download_url': normalizer(url)}

    return result


@app.route('/search')
def search():
    limit = int(request.args.get('page[limit]', 100))
    offset = int(request.args.get('page[offset]', 0))
    query = request.args.get('query')

    return jsonify(do_search(query, limit, offset))


@app.route('/download')
def download():
    download_url = request.args.get('url')
    provider_alias = request.args.get('provider')

    return jsonify(do_download(download_url, provider_alias))


if __name__ == '__main__':
    app.run()
    # "/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json",
    # "http://zaycev.net/pages/39469/3946953.shtml?autoplay=1"
