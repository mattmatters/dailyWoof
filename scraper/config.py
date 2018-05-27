"""Basic configuration for file"""
import os
import pika
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scraper.sites import sites

# Check environmental variables for config info
REDIS_HOST = os.getenv('REDIS_HOST', default='redis-service')
REDIS_PORT = os.getenv('REDIS_PORT', default=6379)
MQ_HOST = os.getenv('MQ_HOST', default='rabbitmq-service')
MQ_PORT = os.getenv('MQ_PORT', default=5672)

CONNECTION_PARAMETERS = pika.ConnectionParameters(
    MQ_HOST,
    port=MQ_PORT,
    retry_delay=5,
    connection_attempts=20,
    heartbeat=360)

MESSAGE_PROPERTIES = pika.BasicProperties(delivery_mode=2, content_type='application/json')
QUEUE_NAME = 'stories'

WORK = {
    'bbc': sites['bbc'],
    'fox': sites['fox'],
    'nbc': sites['nbc'],
    'cbs': sites['cbs'],
    'npr': sites['npr'],
    'nola': sites['nola'],
    'metro': sites['metro'],
    'verge': sites['verge'],
    'guardian': sites['guardian'],
}

def setup_mq(queue):
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    chan = connection.channel()
    chan.exchange_declare(exchange=queue, exchange_type='fanout')

    return chan

def connect_browser():
    capabilities = webdriver.DesiredCapabilities().FIREFOX
    options = Options()
    options.add_argument("--headless")

    return webdriver.Firefox(firefox_options=options, executable_path="/usr/bin/geckodriver", capabilities=capabilities)
