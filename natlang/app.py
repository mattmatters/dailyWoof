"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""
import random
from time import sleep

import pika
from redis import Redis
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper.scraper import get_story, get_links
from scraper.sites import sites
from scraper.utility import append_nlp, set_story

# Config

# RabbitMQ
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(
        'messager', retry_delay=5, connection_attempts=5))
CHANNEL = CONNECTION.channel()
CHANNEL.queue_declare(queue='images')

# Pick any of the predefined sites or roll your own
WORK = [sites['cnn'], sites['bbc'], sites['nyTimes'], sites['guardian']]

# Basic enivronment configuration
REDIS = Redis(host='redis', port=6379)
BROWSER = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)

# Application
BROWSER.implicitly_wait(2)


def publish_image(image_url):
    has_published = False
    retries = 0

    # http://www.itmaybeahack.com/homepage/iblog/architecture/C551260341/E20081031204203/index.html
    while not has_published and retries < 5:
        try:
            CHANNEL.basic_publish(
                exchange='',
                routing_key='images',
                body=image_url,
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


while True:
    random.shuffle(WORK)
    for job in WORK:
        links = get_links(BROWSER, job['url'], job['link_regex'])

        for link in links:
            if not REDIS.exists(link):
                try:
                    story = get_story(BROWSER, link, job['story_xpath'])
                except Exception:
                    continue

                if len(story['story']):
                    story = append_nlp(story)
                    set_story(REDIS, story)
                    publish_image(story['image'])
