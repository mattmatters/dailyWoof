"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""

# Libraries
import random
import json
import time
from redis import Redis
from scraper import get_story, get_links
import config

def publish_story(chan, queue, content):
    chan.basic_publish(
        exchange=queue,
        routing_key='',
        body=json.dumps(content),
        properties=config.MESSAGE_PROPERTIES)

def main():
    browser = config.connect_browser()
    db = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    # We want to not look like a bot, I found that initially get all the links to possible scrape
    # then shuffling them looks much less like a bot.
    links = []
    for name, job in config.WORK.items():
        new_links = []

        try:
            print(job['url'])
            new_links = get_links(browser, job['url'], job['link_regex'])
        except Exception as e:
            # Browser sessions get a little funky, in this case refresh the connection
            browser = config.connect_browser()
            print(e)

        links += [(name, link) for link in new_links]

    random.shuffle(links)

    channel = config.setup_mq(config.QUEUE_NAME)
    for link in list(set(links)):
        # Avoid doing unnessary duplicate work
        if db.exists(link):
            continue

        # Just in case
        time.sleep(random.randint(1, 8))

        try:
            print(link)
            story = get_story(browser, link[1], config.WORK[link[0]]['story_xpath'])
        except Exception as e:
            print(e)
            browser = config.connect_browser()
            continue

        # Quick filtering to avoid invalid stories
        if len(story['story']) == 0:
            continue

        # Often connections are lost, reconnect in those cases
        try:
            publish_story(channel, config.QUEUE_NAME, story)
        except Exception:
            channel = config.setup_mq(config.QUEUE_NAME) # Refresh the connection

if __name__ == '__main__':
    main()
