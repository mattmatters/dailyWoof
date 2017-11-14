"""
Main library functions.

Give it a valid Selenium Driver connected to a browser as the browser argument.
"""
from re import search

# Selenium and automating a real web browser on the web is a bit finicky
# So a lot of the try catch statements are protecting errors

def get_links(browser, url):
    """
    Main scraping method of obtaining links.

    Scrapes sites for all href's on the given url
    """
    try:
        browser.get(url)
    except Exception:
        return []

    return browser.find_elements_by_xpath("//a[@href]")

def extract_links(tags, regex):
    """
    Takes a list of a tags and extracts all urls that match the given regex
    """
    href = []

    for a_tag in tags:
        try:
            href.append(a_tag.get_attribute('href'))
        except Exception as e:
            continue

    return [link for link in href if search(regex, link)]

def get_story_body(body, xpath):
    """Uses xpath to get all story text matching it"""
    story = body.find_elements_by_css_selector(xpath)
    return "\n".join([x.text for x in story if len(x.text) > 0])

def getOgDetails(header):
    """
    Extracts the search engine crawler information

    This is incredibly useful as just about every website has them
    """
    date = header.find_element_by_xpath('//meta[contains(@name, "pubdate")]')
    title = header.find_element_by_xpath('//meta[contains(@property, "og:title")]')
    desc = header.find_element_by_xpath('//meta[contains(@name, "description")]')

    return {
        'date': date.get_attribute('content') if date else '2017-01-01',
        'title': title.get_attribute('content') if title else 'Unknown',
        'description': desc.get_attribute('content') if desc else 'description'
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
    details = getOgDetails(browser.find_element_by_css_selector('head'))
    story = get_story_body(browser.find_element_by_css_selector('body'), xpath)

    return {
        'url': story_url,
        'date': details['date'],
        'title': details['title'],
        'desc': details['description'],
        'story': story
    }

def scrape_site(browser, details):
    a_tags = get_links(browser, details['url'])
    links = extract_links(a_tags, details['link_regex'])
    stories = []

    for link in links:
        try:
            stories.append(get_story(browser, link, details['story_xpath']))
        except Exception as e:
            continue

    return stories