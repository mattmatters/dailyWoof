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
from scraper.scraper import get_story, get_links
from scraper.sites import sites

# Config

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters('messager', retry_delay=5, connection_attempts=5))
CHANNEL = CONNECTION.channel()
CHANNEL.exchange_declare(exchange='stories', exchange_type='fanout')

# Basic enivronment configuration
REDIS = Redis(host='redis', port=6379)
BROWSER = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)


def publish_story(story):
    has_published = False
    retries = 0

    # http://www.itmaybeahack.com/homepage/iblog/architecture/C551260341/E20081031204203/index.html
    while not has_published and retries < 5:
        try:
            CHANNEL.basic_publish(
                exchange='stories',
                routing_key='',
                body=json.dumps(story),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type='text/plain'))
            has_published = True
        except Exception:
            has_published = False
            retries += 1
            sleep(5)
            if retries == 5:
                raise Exception('Maximum amount of retries reached')

def main():
    # Pick any of the predefined sites or roll your own
    work = [sites['cnn'], sites['bbc'], sites['nyTimes'], sites['guardian']]

    while True:
        random.shuffle(work)
        for job in work:
            links = get_links(BROWSER, job['url'], job['link_regex'])

            for link in links:

                # Avoid doing unnessary duplicate work
                if not REDIS.exists(link):
                    try:
                        story = get_story(BROWSER, link, job['story_xpath'])
                    except Exception:
                        continue

                    # Quick filtering to avoid invalid stories
                    if len(story['story']):
                        publish_story(story)

if __name__ == '__main__':

    BROWSER.implicitly_wait(2)
    main()
