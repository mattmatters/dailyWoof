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
    'usa': {
        'url': 'https://www.usatoday.com/',
        'link_regex': r'https?:\/\/(www.)?usatoday.com/story/.*',
        'story_xpath': "//*[contains(@class, 'p-text')]"
    },
    'fox': {
        'url': 'https://www.foxnews.com/',
        'link_regex': r'https?:\/\/(www.)?foxnews.com\/.*\/20.*',
        'story_xpath': "//*[contains(@class, 'article-body')]/p"
    },
    'la_times': {
        'url': 'http://www.latimes.com/',
        'link_regex': r'https?:\/\/(www.)?latimes.com\/(politics|business).*',
        'story_xpath': "//*[contains(@class, 'card-content')]/p",
    },
    'nbc': {
        'url': 'https://www.nbcnews.com/',
        'link_regex': r'https?:\/\/(www.)?nbcnews.com\/news.*',
        'story_xpath': "//*[contains(@class, 'article-body')]/p",
    },
    'npr': {
        'url': 'https://www.npr.org/',
        'link_regex': r'https?:\/\/(www.)?npr.org\/(sections\/)?(therecord\/)?20.*',
        'story_xpath': "//*[contains(@class, 'storytext')]/p",
    },
    'reuters': {
        'url': 'https://www.reuters.com/',
        'link_regex': r'',
        'story_xpath': "",
    },
    'time': {
        'url': 'http://time.com/',
        'link_regex': r'',
        'story_xpath': "",
    },
    'chicago_tribune': {
        'url': 'http://www.chicagotribune.com/',
        'link_regex': r'',
        'story_xpath': "",
    },
    'forbes': {
        'url': 'https://www.forbes.com/',
        'link_regex': r'',
        'story_xpath': "",
    },
    'verge': {
        'url': 'https://www.theverge.com/',
        'link_regex': r'https?:\/\/(www.)?theverge.com\/20.*',
        'story_xpath': "//*[contains(@class, 'c-entry-content')]/p",
    },
    'metro': {
        'url': 'http://metro.co.uk/',
        'link_regex': r'https?:\/\/(www.)?metro.co.uk\/20.*',
        'story_xpath': "//*[contains(@class, 'article-body')]/p"
    },
    'nola': {
        'url': 'http://www.nola.com/',
        'link_regex': r'https?:\/\/(www.)?nola.com\/.*\/20.*',
        'story_xpath': "//*[contains(@class, 'entry-content')]/p",
    },
    'cbs': {
        'url': 'https://www.cbsnews.com/',
        'link_regex': r'https?:\/\/(www.)?cbsnews.com\/news\/.*',
        'story_xpath': "//*[contains(@class, 'entry')]/div/p",
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
