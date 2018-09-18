# -*-coding:utf-8;-*-

import json
import os


import gevent.monkey
gevent.monkey.patch_all()
import pika
import requests

from run import do_download, do_search

cloud_amqp_url = os.getenv('CLOUDAMQP_URL', 'amqp://pbiolrgp:QhFRfvRmEczAM_ASOSWyBOJW0lbK-nGN@hornet.rmq.cloudamqp.com/pbiolrgp')
# callback_url = os.getenv('CALLBACK_URL')


def handle_search_action(payload):
    print('Handle search action')

    query = payload['query']
    limit = payload['limit']
    offset = payload['offset']

    search_data = do_search(query, limit, offset)

    print(payload)
    result = {
        "content": {
            "meta": {
                "total": search_data['meta']['total'],
                "limit": search_data['meta']['limit'],
                "offset": search_data['meta']['offset']
            },
            "data": search_data['data']
        },
        "meta": {
            "token": payload['token'],
            "query": payload['query'],
            "chat_id": payload['channel_id'],
            "parent_message_id": payload['parent_message_id']
        }
    }

    # check code (200 - success)
    requests.post(payload['postback_url'], json=result)

    return True


def handle_download_action(payload):
    print('Handle download action')

    url = payload['url']
    provider = payload['provider']

    result = {
        'content': do_download(url, provider),
        'meta':    {
            'token':    payload['token'],
            'chat_id':  payload['channel_id']
        }
    }

    # check code (200 - success)
    requests.post(payload['postback_url'], json=result)

    return True


def on_message(channel, method_frame, header_frame, body):
    payload = json.loads(body)['payload']
    handler = handle_download_action if 'download' == payload['action_type'] else handle_search_action

    is_success = handler(payload)

    if is_success:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


parameters = pika.URLParameters(cloud_amqp_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.basic_consume(on_message, 'user_request')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

# if __name__ == '__main__':
#     import json
#     print('---------------------')
    # download_data = json.loads('{"payload": {"channel_id": "292198768", "action_type": "download", "token": "412602481:AAGSwyStgWSzQhwmCr-PbodfKlfvg98aYVQ", "language": "RU", "url": "/musicset/play/073fc2d7c71cdec0b80f4196155f5855/1682418.json", "provider": "zaycev_net", "postback_url": "https://music-dealer-stage.herokuapp.com/telegram/download/result"}}')
    # handle_download_action(download_data['payload'])

    # search_data = json.loads('{"payload": {"channel_id": 292198768, "action_type": "search", "token": "412602481:AAGSwyStgWSzQhwmCr-PbodfKlfvg98aYVQ", "language": "RU", "query": "\u0440\u043e\u0442\u0430\u0440\u0443", "parent_message_id": null, "limit": 5, "offset": 0, "postback_url": "https://music-dealer-stage.herokuapp.com/telegram/search/result"}}')
    # handle_search_action(search_data['payload'])