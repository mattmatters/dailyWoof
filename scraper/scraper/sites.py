"""
This is the configuration for all sites to be scraped.

The scraper will only get the front page, we are only looking for trending news.

The link_regex will be the regex to match all links on the home page for.

The story_xpath is a bit more driver specific, but it's  a css selector to get the story text.
"""

sites = {
    'cnn': {
        'url': 'https://www.cnn.com',
        'link_regex': r'https?:\/\/(www.)?cnn.com\/20\d*',
        'story_xpath': "//*[contains(@class, 'zn-body__paragraph')]",
    },
    'bbc': {
        'url': 'http://www.bbc.com/',
        'link_regex': r'https?:\/\/(www.)?bbc.com\/news\/.*-\d*',
        'story_xpath': "//*[contains(@class, 'story-body__inner')]/p",
    },
    'nyTimes': {
        'url': 'https://www.nytimes.com/',
        'link_regex': r'https?:\/\/(www.)?nytimes.com\/20*',
        'story_xpath': "//*[contains(@class, 'story-body-text')]",
    },
    'guardian': {
        'url': 'https://www.theguardian.com',
        'link_regex': r'https?:\/\/(www.)?theguardian.com\/us-news\/*',
        'story_xpath': "//*[contains(@class, 'content__article-body')]",
    },
    'eOnline': {
        'url': 'http://www.eonline.com',
        'link_regex': r'https?:\/\/(www.)?eonline.com\/news\/.*',
        'story_xpath': "//*[contains(@class, 'post-content')]"
    },
    'yahoo': {
        'url': 'https://www.yahoo.com/news/',
        'link_regex': r'https?:\/\/(www.)?yahoo.com\/news\/.*',
        'story_xpath': "//*[contains(@class, 'canvas-text')]",
    },
    'wp': {
        'url': 'https://www.washingtonpost.com/?reload=false',
        'link_regex': r'https?:\/\/(www.)?washingtonpost.com/news/.*',
        'story_xpath': '//article/p'
    },
    'usa': {
        'url': 'https://www.usatoday.com/',
        'link_regex': r'https?:\/\/(www.)?usatoday.com/story/.*',
        'story_xpath': "//*[contains(@class, 'p-text')]"
    },
    'newsbud': {
        'url': 'https://www.newsbud.com/',
        'link_regex': r'https?:\/\/(www.)?newsbud.com/20.*',
        'story_xpath': "//*[contains(@class, 'entry-content')]/p",
    }
}
"""
Ones that have been ruled out

+ NBC: infinite scroll
+ Wall Street Journal: paywall
+ USA Today: frequent pop ups
+ Washington Post: There scrape version is more trouble then it's worth
+ Yahoo: Images suck
"""
