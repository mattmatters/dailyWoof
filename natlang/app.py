"""
Natural Language Processor

Receives scraped news and identifies common nouns, adjectives, and proper nouns
"""
import os
import re
import json
import logging
import time
import pika
from natlang.nlp import process_txt

START_TIME = time.time()

MQ_HOST = os.environ['MQ_HOST'] or 'rabbitmq-service'
MQ_PORT = os.environ['MQ_PORT'] or 5672
QUEUE_NAME = 'text'
NEXT_QUEUE_NAME = 'images'
MESSAGE_PROPERTIES = pika.BasicProperties(content_type='application/json')
CONNECTION_PARAMETERS = pika.ConnectionParameters(MQ_HOST,
                                                  retry_delay=5,
                                                  connection_attempts=20)

def append_nlp(result):
    """Runs the nlp pipeline and adds to result"""
    combined_txt = "\n".join(
        [result['title'], result['desc'], result['story']])

    return {**result, **process_txt(combined_txt)}


def extract_name(url):
    """Takes the a url and exracts the images name"""
    return re.search(r"[^\/]*\.(png|jpg|jpeg)", url)


def callback(ch, method, properties, body):
    """RabbitMQ callback"""
    body = json.loads(body.decode('utf-8'))
    logging.info('Processing: %s', body['url'])
    body = append_nlp(body)

    ch.basic_publish(exchange='',
                     routing_key=NEXT_QUEUE_NAME,
                     body=json.dumps(body),
                     properties=MESSAGE_PROPERTIES)

    # Should sub this out with a more graceful solution
    if time.time() - START_TIME > 3600:
        exit()

def setup_mq():
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    channel = connection.channel()

    channel.exchange_declare(exchange='stories', exchange_type='fanout')
    channel.queue_declare(queue=NEXT_QUEUE_NAME)
    queue = channel.queue_declare(queue=QUEUE_NAME)

    channel.queue_bind(exchange='stories', queue=queue.method.queue)
    channel.basic_qos(prefetch_count=1)
    return channel


def main():
    """Subscribe to queue and story processed stories"""
    channel = setup_mq()
    channel.basic_consume(callback, queue=QUEUE_NAME, no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()
