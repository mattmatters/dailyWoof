"""
Natural Language Processor

Receives scraped news and identifies common nouns, adjectives, and proper nouns
"""
import random
import json
from time import sleep

import pika
from redis import Redis
from natlang.utility import append_nlp, set_story

REDIS = Redis(host='redis', port=6379)
QUEUE_NAME = 'text'
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(
        'messager', retry_delay=5, connection_attempts=5))
CHANNEL = CONNECTION.channel()


def create_queue(channel, name):
    queue = channel.queue_declare(queue=name)
    channel.queue_bind(exchange='stories', queue=queue.method.queue)

def callback(ch, method, properties, body):
    body = json.loads(body.decode('utf-8'))
    set_story(REDIS, append_nlp(body))


def main():
    """Subscribe to queue and story processed stories"""

    # Create a queue and bind it to the stories exchange
    create_queue(CHANNEL, QUEUE_NAME)

    # Start consuming
    CHANNEL.basic_qos(prefetch_count=1)
    CHANNEL.basic_consume(callback, queue=QUEUE_NAME, no_ack=True)
    CHANNEL.start_consuming()


if __name__ == '__main__':
    sleep(10)
    main()
