"""
Natural Language Processor

Receives scraped news and identifies common nouns, adjectives, and proper nouns
"""
import re
import json
import logging
from time import sleep
import pika
from natlang.nlp import process_txt

# Set up logging
WORKER_INFO = {'clientip': '298', 'user': 'nlp'}
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('nlp_worker')


QUEUE_NAME = 'text'
NEXT_QUEUE_NAME = 'images'
CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('messager', retry_delay=5, connection_attempts=5))
CHANNEL = CONNECTION.channel()

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
    LOGGER.info('Processing: %s', body['url'], extra=WORKER_INFO)
    body = append_nlp(body)

    ch.basic_publish(exchange='',
                     routing_key=NEXT_QUEUE_NAME,
                     body=json.dumps(body))

def main():
    """Subscribe to queue and story processed stories"""
    # Create a queue and bind it to the stories exchange
    CHANNEL.exchange_declare(exchange='stories', exchange_type='fanout')
    CHANNEL.queue_declare(queue=NEXT_QUEUE_NAME)
    queue = CHANNEL.queue_declare(queue=QUEUE_NAME)
    CHANNEL.queue_bind(exchange='stories', queue=queue.method.queue)

    # Start consuming
    CHANNEL.basic_qos(prefetch_count=1)
    CHANNEL.basic_consume(callback, queue=QUEUE_NAME, no_ack=True)
    CHANNEL.start_consuming()


if __name__ == '__main__':
    sleep(10)
    main()
