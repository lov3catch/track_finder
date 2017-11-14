from flask import Flask, request
from flask import jsonify

from handlers.finder import parse_result, normalize_song_name, normalize_download_url

app = Flask(__name__)


@app.route('/search')
def search():
    limit = 100
    offset = 0

    song_name = request.args.get('query')
    search_result = parse_result(normalize_song_name(song_name))

    result = {}
    result['data'] = search_result[offset:limit]
    result['meta'] = {
        'limit': 100,
        'offset': 100,
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
