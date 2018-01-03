# The Daily Woof Natural Language Processor
All news stories are fed into a natural language processor.

This service has been written in Python. The choice was due to the copious amounts of libraries that already existed, turning this into a trivial task.

## Natural Language Processing
Currently the app is using [TextBlob](https://textblob.readthedocs.io/en/dev/) and [NLTK](http://www.nltk.org/).

These libraries are mostly used for obtaining a list of the trending names and nouns in each article. These will later be used by the web app to randomly substitute trending words with dog releated ones.

