"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""
import random
import json
import logging
from time import sleep

import pika
from redis import Redis
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scraper import get_story, get_links
from scraper.sites import sites


# Logging
WORKER_INFO = {'clientip': '298', 'user': 'crawler'}
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('nlp_worker')

# Config
CONNECTION_PARAMETERS = pika.ConnectionParameters('messager', port=5672, retry_delay=5, connection_attempts=10)
MESSAGE_PROPERTIES = pika.BasicProperties(delivery_mode=2, content_type='text/plain')
QUEUE_NAME = 'stories'

# Basic enivronment configuration
REDIS = Redis(host='redis', port=6379)

print("BEGIN")

def connect_browser():
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=options, executable_path="/usr/bin/geckodriver")
    return browser

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
    # Connect to browser
    browser = connect_browser()

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    channel = connection.channel()
    channel.exchange_declare(exchange=QUEUE_NAME, exchange_type='fanout')

    # Pick any of the predefined sites or roll your own
    work = {
        'bbc': sites['bbc'],
        # 'usa': sites['usa'],
        'cnn': sites['cnn'],
        'fox': sites['fox'],
        'nbc': sites['nbc'],
        'cbs': sites['cbs'],
        'npr': sites['npr'],
        'nola': sites['nola'],
        'metro': sites['metro'],
        'verge': sites['verge'],
        # 'eOnline': sites['eOnline'],
        'guardian': sites['guardian'],
        # 'la_times': sites['la_times'],
    }

    while True:
        # sleep(30)
        # We want to not look like a bot, I found that initially get all the links to possible scrape
        # then shuffling them looks much less like a bot.
        links = []
        for name, job in work.items():
            new_links = []
            LOGGER.info("Getting links for %s", name, extra=WORKER_INFO)
            print(name)
            try:
                new_links = get_links(browser, job['url'], job['link_regex'])
            except Exception:
                # Browser sessions get a little funky, in this case refresh the connection
                browser.quit()
                browser = connect_browser()

            links += [(name, link) for link in new_links]

        random.shuffle(links)

        for link in list(set(links)):
            # Avoid doing unnessary duplicate work
            if not REDIS.exists(link):
                # Just in case
                sleep(random.randint(1, 8))
                print(link)
                try:
                    LOGGER.info("Scraping %s", link, extra=WORKER_INFO)
                    story = get_story(browser, link[1], work[link[0]]['story_xpath'])
                except Exception as e:
                    LOGGER.error("Unsuccessfully got %s", link, extra=WORKER_INFO)
                    print(e)
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
    main()
