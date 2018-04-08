"""
Main library functions.
Give it a valid Selenium Driver connected to a browser as the browser argument.

Selenium and automating a real web browser on the web is a bit finicky.
It prefers to throw errors if elements can not be located So there is a lot of
the try catch statements mainly to protect against errors.
"""
from time import sleep
import re

DEFAULT_TITLE = ''
DEFAULT_DESC = ''
DEFAULT_IMAGE_URL = ''

def get_links(browser, url, regex):
    """Get all front page news links"""
    browser.get(url)

    # @TODO use Selenium's kinda crappy timeout feature
    # The implicit wait feature fails on headless Firefox
    sleep(2)

    tags = browser.find_elements_by_xpath("//a[@href]")
    links = []

    for a_tag in tags:
        try:
            links.append(a_tag.get_attribute('href'))
        except Exception:
            continue

    return [link for link in links if re.search(regex, link)]

def get_details(header):
    """
    Extracts the search engine crawler information
    This is incredibly useful as just about every website has them
    """
    title = header.find_element_by_xpath('//meta[contains(@property, "og:title")]')
    desc = header.find_element_by_xpath('//meta[contains(@name, "description")]')
    img = header.find_element_by_xpath('//meta[contains(@property, "og:image")]')

    return {
        'title': title.get_attribute('content') if title else DEFAULT_TITLE,
        'description': desc.get_attribute('content') if desc else DEFAULT_DESC,
        'image': img.get_attribute('content') if img else DEFAULT_IMAGE_URL
    }


def get_story(browser, story_url, xpath):
    """
    Pings url and extracts all necessary information

    It often fails due to sites not having a consistent format
    or misconfiguration, so it's reccomended that all uses of this
    function wrap itself in a try catch block.
    """
    browser.get(story_url)
    sleep(10) # @TODO use Selenium's kinda crappy timeout feature

    details = get_details(browser.find_element_by_css_selector('head'))
    story = "\n".join([x.text for x in browser.find_elements_by_xpath(xpath) if len(x.text) > 0])

    return {
        'url': story_url,
        'title': details['title'],
        'desc': details['description'],
        'image': details['image'],
        'story': story
    }
