"""
News Scraper App

Scrape news sites and recieve trending names, nouns, and adjectives.
"""
from redis import Redis
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import scraper
from scraper.sites import sites
from scraper.utility import have_story, set_story, append_nlp

# Config
WORK = [
    sites['cnn'],
    sites['wallStreetJournal']
]
REDIS = Redis(host='redis', port=6379)
BROWSER = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)


# Application
BROWSER.implicitly_wait(2)

while True:
    for job in WORK:
        stories = [append_nlp(x) for x in scraper.scrape_site(BROWSER, job) if not have_story(REDIS, x['url'])]
        for x in stories:
            set_story(REDIS, x)