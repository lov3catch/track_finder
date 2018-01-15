from flask import Flask, request
from flask import jsonify

# from handlers.zaycev_net.finder import parse_result, normalize_song_name, normalize_download_url
from handlers.mail_ru.finder import parse_result, normalize_song_name, normalize_download_url

app = Flask(__name__)


@app.route('/search')
def search():
    limit = int(request.args.get('page[limit]', 100))
    offset = int(request.args.get('page[offset]', 0))

    song_name = request.args.get('query')
    search_result = parse_result(normalize_song_name(song_name), limit, offset)

    result = {}
    result['data'] = search_result
    result['meta'] = {
        'limit': limit,
        'offset': offset,
        'total': len(search_result)
    }
    return jsonify(result)


@app.route('/download')
def download():
    download_url = request.args.get('url')

    result = {}
    result['data'] = {'download_url': normalize_download_url(download_url)}

    return jsonify(result)


if __name__ == '__main__':
    app.run()
# "/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json",
# "http://zaycev.net/pages/39469/3946953.shtml?autoplay=1"