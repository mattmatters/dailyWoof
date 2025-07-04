# The Daily Woof

## Archival Notice

I was a junior engineer frustrated with my work situation and made this. It mostly served as a test bed for various stuff that later
showed up in my career.

I am particularly proud of the face replacement tech which would be expanded on [here](https://github.com/mattmatters/faceitize). I
thought being one of the earliest people to compile a lot of these libraries to Webassembly would make job offers come swarming in.
However it mostly was met with _"Neat, we do not feel you are qualified for email styling"_. Strangely enough I ended up getting pinged
pretty frequently on that lib years later.

This is mostly being left up as an archive of what a junior engineer thought a largescale monorepo looked like in an era where K8s and
WASM was the fancy new tech.

Enjoy! I think this is still neat for what it was.

## About

Dogs have taken over the news.

Text and image parser for deciphering front page news stories into a format easily parsed by :dog:.

Also DMX.

## Running

_For a development build._

To get a sense for the structure of the application, check out the compose file. The entire app can be spun up locally with this command.

```bash
docker-compose up --build
```

Supply a .env file in the root directory to store processed images in a AWS S3 Bucket.


## Directory Structure
The entire app takes a very _microservice-esque_ approach.

Every directory is its own service/container with one purpose. The docker-compose.yml
ties everything together.

Here's a quick overview to get anyone started.

```bash
.
├── LICENSE        # Don't use logos and stuff
├── README.md      # Hi
├── config         # Configuration for words to replace
├── docker-compose.yml
├── frontend       # Vue frontend, dist directory ends up in web/static
├── images         # Facial recognition and replacer, stores results in an S3 Bucket
├── natlang        # Natural Language Processor for scraped stories
├── redis.conf     # Custom config for only storing the newest stories
├── scraper        # Headless browser scraping news sites
├── test.sh        # Bad test script for CI
└── web            # API Endpoint
```
