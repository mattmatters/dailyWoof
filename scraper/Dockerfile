FROM python:3.6.3
WORKDIR /usr/src/scraper

# Install runtime dependencies
# Install deps + add Chrome Stable + purge all the things
RUN apt-get update && apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        xvfb \
        --no-install-recommends \
        && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
        && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
        && apt-get update && apt-get install -y \
        google-chrome-stable \
        --no-install-recommends

RUN apt-get install -y unzip \
        && wget -N http://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip \
        && unzip chromedriver_linux64.zip \
        && chmod +x chromedriver \
        && mv -f chromedriver /usr/local/share/chromedriver \
        && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
        && ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

# Add Chrome as a user
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
        && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

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

USER chrome

ENV NAME scraper
