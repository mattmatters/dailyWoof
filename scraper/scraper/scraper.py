"""
Main library functions.
Give it a valid Selenium Driver connected to a browser as the browser argument.
"""
from re import search
from scraper.utility import set_story

# Selenium and automating a real web browser on the web is a bit finicky
# So a lot of the try catch statements are protecting errors

DEFAULT_TITLE = ''
DEFAULT_DESC = ''
DEFAULT_IMAGE_URL = ''

def get_links(browser, url, regex):
    """Get all front page news links"""
    try:
        browser.get(url)
    except Exception:
        return []

    tags = browser.find_elements_by_xpath("//a[@href]")
    links = []

    for a_tag in tags:
        try:
            links.append(a_tag.get_attribute('href'))
        except Exception:
            continue

    return [link for link in links if search(regex, link)]


def get_story_body(body, xpath):
    """Uses xpath to get all story text matching it"""
    story = body.find_elements_by_css_selector(xpath)
    return "\n".join([x.text for x in story if len(x.text) > 0])


def get_details(header):
    """
    Extracts the search engine crawler information
    This is incredibly useful as just about every website has them
    """
    title = header.find_element_by_xpath(
        '//meta[contains(@property, "og:title")]')
    desc = header.find_element_by_xpath(
        '//meta[contains(@name, "description")]')
    img = header.find_element_by_xpath(
        '//meta[contains(@property, "og:image")]')

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
    browser.implicitly_wait(2)
    details = get_details(browser.find_element_by_css_selector('head'))
    story = get_story_body(browser.find_element_by_css_selector('body'), xpath)

    return {
        'url': story_url,
        'title': details['title'],
        'desc': details['description'],
        'image': details['image'],
        'story': story
    }


def scrape_site(browser, db_client, details):
    links = get_links(browser, details['url'], details['link_regex'])

    for link in links:
        if not db_client.exists(link):
            try:
                story = get_story(browser, link, details['story_xpath'])
            except Exception:
                continue

            if len(story['story']):
                set_story(db_client, story)

    return
