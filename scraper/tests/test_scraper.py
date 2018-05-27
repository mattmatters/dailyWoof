from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scraper import scraper, get_story
from scraper.sites import sites

def make_browser():
    capabilities = webdriver.DesiredCapabilities().FIREFOX
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(firefox_options=options, executable_path="/usr/bin/geckodriver", capabilities=capabilities)

# Tests that our regex works
def test_bbc_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['bbc']['url'], sites['bbc']['link_regex'])
    assert len(stories) > 0


def test_bbc_story():
    browser = make_browser()
    story = get_story(browser,
                      'http://www.bbc.com/news/world-us-canada-41973952',
                      sites['bbc']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0


# Tests that our regex works
def test_nyTimes_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['nyTimes']['url'],
                                sites['nyTimes']['link_regex'])
    assert len(stories) > 0


def test_nyTimes_story():
    browser = make_browser()
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
    browser = make_browser()
    stories = scraper.get_links(browser, sites['guardian']['url'],
                                sites['guardian']['link_regex'])
    assert len(stories) > 0


def test_guardian_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.theguardian.com/us-news/2017/nov/09/one-year-later-trump-takes-a-grand-tour-of-asia-as-clinton-visits-wisconsin-finally',
        sites['guardian']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_usa_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['usa']['url'],
                                sites['usa']['link_regex'])
    assert len(stories) > 0


def test_usa_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.usatoday.com/story/money/nation-now/2018/02/26/trump-just-claimed-u-s-makes-better-solar-panels-than-china-thats-not-quite-right/375307002/',
        sites['usa']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_eOnline_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['eOnline']['url'], sites['eOnline']['link_regex'])
    assert len(stories) > 0

def test_eOnline_story():
    browser = make_browser()
    story = get_story(
        browser,
        'http://www.eonline.com/news/893550/did-kylie-jenner-have-a-private-baby-shower-all-the-details-on-her-pink-filled-celebration',
        sites['eOnline']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_fox_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['fox']['url'], sites['fox']['link_regex'])
    assert len(stories) > 0

def test_fox_story():
    browser = make_browser()
    story = get_story(
        browser,
        'http://www.foxnews.com/politics/2018/02/27/supreme-court-rules-that-detained-immigrants-dont-get-automatic-bond-hearings.html',
        sites['fox']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_verge_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['verge']['url'], sites['verge']['link_regex'])
    assert len(stories) > 0

def test_verge_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.theverge.com/2018/2/27/17060092/blackberry-world-app-store-paid-apps-discontinuation-removal-april-1',
        sites['verge']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_metro_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['metro']['url'], sites['metro']['link_regex'])
    assert len(stories) > 0

def test_metro_story():
    browser = make_browser()
    story = get_story(
        browser,
        'http://metro.co.uk/2018/02/27/kevin-spacey-foundation-shut-uk-actor-faces-sexual-assault-allegations-7347287/',
        sites['metro']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_nola_regex():
    stories = scraper.get_links(make_browser(), sites['nola']['url'], sites['nola']['link_regex'])
    assert len(stories) > 0

def test_nola_story():
    story = get_story(
        make_browser(),
        'http://www.nola.com/northshore/index.ssf/2018/02/three_st_tammany_students_accu.html#incart_2box_nola_river_orleans_news',
        sites['nola']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_cbs_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['cbs']['url'], sites['cbs']['link_regex'])
    assert len(stories) > 0

def test_cbs_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.cbsnews.com/news/brad-parscale-trump-2020-campagin-manager-announced-today-2018-02-27/',
        sites['cbs']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_la_times_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['la_times']['url'], sites['la_times']['link_regex'])
    assert len(stories) > 0

def test_la_times_story():
    browser = make_browser()
    story = get_story(
        browser,
        'http://www.latimes.com/politics/la-na-pol-jared-kushner-20180227-story.html',
        sites['la_times']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_nbc_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['nbc']['url'], sites['nbc']['link_regex'])
    assert len(stories) > 0

def test_nbc_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.nbcnews.com/news/us-news/parkland-school-shooting-stoneman-douglas-students-prepare-confront-memories-they-n851656',
        sites['nbc']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0

def test_npr_regex():
    browser = make_browser()
    stories = scraper.get_links(browser, sites['npr']['url'], sites['npr']['link_regex'])
    assert len(stories) > 0

def test_npr_story():
    browser = make_browser()
    story = get_story(
        browser,
        'https://www.npr.org/2018/02/27/585133064/lawmakers-agree-on-paid-family-leave-but-not-the-details',
        sites['npr']['story_xpath'])
    assert len(story['title']) > 0
    assert len(story['desc']) > 0
    assert len(story['story']) > 0
    assert len(story['image']) > 0
