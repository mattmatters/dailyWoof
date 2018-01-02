FROM python:3.6.3
WORKDIR /usr/src/scraper

# Intstall this stuff for caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Codebase
COPY setup.py ./
COPY scraper/ ./scraper/.

COPY Makefile ./
RUN make init

# Tests and everything else
COPY . .

ENV NAME scraper
