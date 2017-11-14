from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import scraper
from scraper.sites import sites

browser = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)

browser.implicitly_wait(2)

# Tests that we can get a tags off the home page
def test_cnn_scrape():
    stories = scraper.get_links(browser, sites['cnn']['url'])
    assert len(stories) > 0

# Tests that our regex works
def test_cnn_regex():
    stories = scraper.get_links(browser, sites['cnn']['url'])
    stories = scraper.extract_links(stories, sites['cnn']['link_regex'])
    assert len(stories) > 0

# Tests that we can get a tags off the home page
def test_bbc_scrape():
    stories = scraper.get_links(browser, sites['bbc']['url'])
    assert len(stories) > 0

# Tests that our regex works
def test_bbc_regex():
    stories = scraper.get_links(browser, sites['bbc']['url'])
    stories = scraper.extract_links(stories, sites['bbc']['link_regex'])
    assert len(stories) > 0

# Tests that we can get a tags off the home page
def test_nyTimes_scrape():
    stories = scraper.get_links(browser, sites['nyTimes']['url'])
    assert len(stories) > 0

# Tests that our regex works
def test_nyTimes_regex():
    stories = scraper.get_links(browser, sites['nyTimes']['url'])
    stories = scraper.extract_links(stories, sites['nyTimes']['link_regex'])
    assert len(stories) > 0

# Tests that we can get a tags off the home page
def test_guardian_scrape():
    stories = scraper.get_links(browser, sites['guardian']['url'])
    assert len(stories) > 0

# Tests that our regex works
def test_guardian_regex():
    stories = scraper.get_links(browser, sites['guardian']['url'])
    stories = scraper.extract_links(stories, sites['guardian']['link_regex'])
    assert len(stories) > 0
