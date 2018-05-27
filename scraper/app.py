"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""

# Libraries
import random
import json
import time
import os

# 3rd party
import pika
from redis import Redis
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Project specific
from scraper import get_story, get_links
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

# Utility functions
def connect_browser():
    capabilities = webdriver.DesiredCapabilities().FIREFOX
    options = Options()
    options.add_argument("--headless")

    return webdriver.Firefox(firefox_options=options, executable_path="/usr/bin/geckodriver", capabilities=capabilities)

def setup_mq(queue):
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    chan = connection.channel()
    chan.exchange_declare(exchange=queue, exchange_type='fanout')

    return chan

def publish_story(chan, queue, content):
    chan.basic_publish(
        exchange=queue,
        routing_key='',
        body=json.dumps(content),
        properties=MESSAGE_PROPERTIES)

def main():
    browser = connect_browser()
    db = Redis(host=REDIS_HOST, port=REDIS_PORT)

    # Pick any of the predefined sites or roll your own
    work = {
        'bbc': sites['bbc'],
        'cnn': sites['cnn'],
        'fox': sites['fox'],
        'nbc': sites['nbc'],
        'cbs': sites['cbs'],
        'npr': sites['npr'],
        'nola': sites['nola'],
        'metro': sites['metro'],
        'verge': sites['verge'],
        'guardian': sites['guardian'],
    }


        # We want to not look like a bot, I found that initially get all the links to possible scrape
        # then shuffling them looks much less like a bot.
    links = []
    for name, job in work.items():
        new_links = []

        try:
            print(job['url'])
            new_links = get_links(browser, job['url'], job['link_regex'])
        except Exception as e:
            print(e)
            # Browser sessions get a little funky, in this case refresh the connection
            browser = connect_browser()


        links += [(name, link) for link in new_links]

    random.shuffle(links)

    channel = setup_mq(QUEUE_NAME)
    for link in list(set(links)):
        # Avoid doing unnessary duplicate work
        if db.exists(link):
            continue

        # Just in case
        time.sleep(random.randint(1, 8))

        try:
            print(link)
            story = get_story(browser, link[1], work[link[0]]['story_xpath'])
        except Exception as e:
            print(e)
            browser = connect_browser()
            continue

        # Quick filtering to avoid invalid stories
        if len(story['story']) == 0:
            continue

        # Often connections are lost, reconnect in those cases
        try:
            publish_story(channel, QUEUE_NAME, story)
        except Exception:
            channel = setup_mq(QUEUE_NAME) # Refresh the connection

if __name__ == '__main__':
    main()
