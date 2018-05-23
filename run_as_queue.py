# -*-coding:utf-8;-*-

import json
import os

import pika
import requests

from run import do_download

cloud_amqp_url = os.getenv('CLOUDAMQP_URL')
callback_url = os.getenv('CALLBACK_URL')


def handle_search_action(payload):
    print('Handle search action')


def handle_download_action(payload):
    print('Handle download action')

    url = payload['url']
    provider = payload['provider']

    result = {
        'content': do_download(url, provider),
        'meta':    {
            'token':    payload['token'],
            'chat_id':  None, # todo: add me!
            'query':    None,
            'language': payload['language']
        }
    }

    # check code (200 - success)
    requests.post(callback_url, data=result)


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
