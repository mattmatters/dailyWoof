<h1 align="center">The Daily Woof</h1>
<p align="center">
    <a href="https://gitlab.com/mattmatters/dailyWoof/commits/master"><img alt="pipeline status" src="https://gitlab.com/mattmatters/dailyWoof/badges/master/pipeline.svg" /></a>
    <a href="https://codeclimate.com/github/mattmatters/dailyWoof/maintainability"><img src="https://api.codeclimate.com/v1/badges/6d419e6fb14f95b76067/maintainability" /></a>
</p>

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
