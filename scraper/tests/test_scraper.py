from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import scraper, get_story
from scraper.sites import sites

browser = webdriver.Remote(
    command_executor='http://browser:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)

browser.implicitly_wait(2)


# Tests that our regex works
def test_cnn_regex():
    stories = scraper.get_links(browser, sites['cnn']['url'],
                                sites['cnn']['link_regex'])
    assert len(stories) > 0


def test_cnn_story():
    story = get_story(
        browser,
        'http://www.cnn.com/2017/11/13/politics/george-hw-bush-groping-allegation/index.html',
        sites['cnn']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


# Tests that our regex works
def test_bbc_regex():
    stories = scraper.get_links(browser, sites['bbc']['url'],
                                sites['bbc']['link_regex'])
    assert len(stories) > 0


def test_bbc_story():
    story = get_story(browser,
                      'http://www.bbc.com/news/world-us-canada-41973952',
                      sites['bbc']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


# Tests that our regex works
def test_nyTimes_regex():
    stories = scraper.get_links(browser, sites['nyTimes']['url'],
                                sites['nyTimes']['link_regex'])
    assert len(stories) > 0


def test_nyTimes_story():
    story = get_story(
        browser,
        'https://www.nytimes.com/2017/11/09/opinion/nuisance-ordinances-eviction-violence.html?action=click&pgtype=Homepage&clickSource=story-heading&module=opinion-c-col-left-region&region=opinion-c-col-left-region&WT.nav=opinion-c-col-left-region',
        sites['nyTimes']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


# Tests that our regex works
def test_guardian_regex():
    stories = scraper.get_links(browser, sites['guardian']['url'],
                                sites['guardian']['link_regex'])
    assert len(stories) > 0


def test_guardian_story():
    story = get_story(
        browser,
        'https://www.theguardian.com/us-news/2017/nov/09/one-year-later-trump-takes-a-grand-tour-of-asia-as-clinton-visits-wisconsin-finally',
        sites['guardian']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


def test_wp_regex():
    stories = scraper.get_links(browser, sites['wp']['url'],
                                sites['wp']['link_regex'])
    assert len(stories) > 0


def test_wp_story():
    story = get_story(
        browser,
        'https://www.washingtonpost.com/politics/more-governors-willing-to-consider-gun-law-changes-after-florida-shooting/2018/02/25/eac08ec0-1a33-11e8-b2d9-08e748f892c0_story.html?hpid=hp_hp-top-table-main_gun-sunday-12pm%3Ahomepage%2Fstory&utm_term=.d00bad371da1',
        sites['wp']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


def test_usa_regex():
    stories = scraper.get_links(browser, sites['usa']['url'],
                                sites['usa']['link_regex'])
    assert len(stories) > 0


def test_usa_story():
    story = get_story(
        browser,
        'https://www.usatoday.com/story/money/nation-now/2018/02/26/trump-just-claimed-u-s-makes-better-solar-panels-than-china-thats-not-quite-right/375307002/',
        sites['usa']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


# Tests that our regex works
def test_eOnline_regex():
    stories = scraper.get_links(browser, sites['eOnline']['url'], sites['eOnline']['link_regex'])
    assert len(stories) > 0

def test_eOnline_story():
    story = get_story(
        browser,
        'http://www.eonline.com/news/893550/did-kylie-jenner-have-a-private-baby-shower-all-the-details-on-her-pink-filled-celebration',
        sites['eOnline']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0
