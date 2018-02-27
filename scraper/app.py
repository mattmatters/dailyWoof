"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""
import random
import json
from time import sleep

import pika
from redis import Redis
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import get_story
from scraper.scraper import get_links
from scraper.sites import sites

# Config
CONNECTION_PARAMETERS = pika.ConnectionParameters('messager', retry_delay=5, connection_attempts=5)
MESSAGE_PROPERTIES = pika.BasicProperties(delivery_mode=2, content_type='text/plain')
QUEUE_NAME = 'stories'

# Basic enivronment configuration
REDIS = Redis(host='redis', port=6379)
BROWSER = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)


def publish_story(channel, story):
    has_published = False
    retries = 0

    # http://www.itmaybeahack.com/homepage/iblog/architecture/C551260341/E20081031204203/index.html
    while not has_published and retries < 5:
        try:
            channel.basic_publish(
                exchange=QUEUE_NAME,
                routing_key='',
                body=json.dumps(story),
                properties=MESSAGE_PROPERTIES)
            has_published = True
        except Exception:
            has_published = False
            retries += 1
            sleep(5)
            # Refresh connection
            if retries == 5:
                raise Exception('Maximum amount of retries reached')

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    channel = connection.channel()
    channel.exchange_declare(exchange=QUEUE_NAME, exchange_type='fanout')

    # Pick any of the predefined sites or roll your own
    work = [sites['bbc'], sites['wp'], sites['cnn'], sites['guardian']]

    while True:
        random.shuffle(work)
        for job in work:
            links = get_links(BROWSER, job['url'], job['link_regex'])

            for link in list(set(links)):

                # Avoid doing unnessary duplicate work
                if not REDIS.exists(link):
                    try:
                        print(link)
                        story = get_story(BROWSER, link, job['story_xpath'])
                    except Exception:
                        continue

                    # Quick filtering to avoid invalid stories
                    if len(story['story']) > 0:
                        try:
                            publish_story(channel, story)
                        except Exception:
                            # Refresh the connection
                            connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
                            channel = connection.channel()

                            # If it doesn't succeed this time, it will crash the application
                            publish_story(channel, story)


if __name__ == '__main__':
    BROWSER.implicitly_wait(2)
    main()
