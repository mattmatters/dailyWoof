# The Daily Woof Scraper
To keep the news fresh and up to date, various new site's front pages are scraped.

This service has been written in Python. The choice was due to the copious amounts of libraries that already existed, turning this into a trivial task.

## Scraping
Most websites are heavily reliant on Javascript, meaning the days of simply piping responses to GET requests into BeautifulSoup are over.

To counter this, an automated instance of [PhantomJS](http://phantomjs.org/)(A headless browser) via [Selenium](http://www.seleniumhq.org/) traverses the top news sites at random intervals.

The big gains are that an actual browser is now executing each site's Javascript, while still appearing like an actual visitor.

The speed tradeoff is huge, however it isn't very resource intensive and keeps a steady flow of new pages coming in.

The urls retrieved from the home pages are then filtered for legitimate links that haven't been crawled recently.

Each new url will be scraped and fed into the application's natural language processor.

## Natural Language Processing
Currently the app is using [TextBlob](https://textblob.readthedocs.io/en/dev/) and [NLTK](http://www.nltk.org/).

These libraries are mostly used for obtaining a list of the trending names and nouns in each article. These will later be used by the web app to randomly substitute trending words with dog releated ones.

