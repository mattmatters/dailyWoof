FROM ubuntu:17.10
WORKDIR /usr/src/scraper

RUN apt-get -y update \
         && apt-get install -y -q software-properties-common wget \
         && add-apt-repository -y ppa:mozillateam/firefox-next \
         && apt-get update -y \
         && apt-get install -y -q \
                python3.6 \
                python3-pip \
                python-dev \
                build-essential \
                firefox \
                openjdk-8-jre-headless \
                xvfb \
                xfonts-100dpi \
                xfonts-75dpi \
                xfonts-scalable \
                xfonts-cyrillic

RUN pip3 install --upgrade pip

## Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz \
        && tar -x geckodriver -zf geckodriver-v0.16.1-linux64.tar.gz -O > /usr/bin/geckodriver \
        && chmod +x /usr/bin/geckodriver

# # Install runtime dependencies
# # Install deps + add Chrome Stable + purge all the things
# RUN apt-get update && apt-get install -y \
#         apt-transport-https \
#         ca-certificates \
#         curl \
#         gnupg \
#         xvfb \
#         --no-install-recommends \
#         && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#         && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#         && apt-get update && apt-get install -y \
#         google-chrome-stable \
#         --no-install-recommends

# RUN apt-get install -y unzip \
#         && wget -N http://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip \
#         && unzip chromedriver_linux64.zip \
#         && chmod +x chromedriver \
#         && mv -f chromedriver /usr/local/share/chromedriver \
#         && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
#         && ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

# # Add Chrome as a user
# RUN groupadd -r chrome && useradd -r -g chrome -G audio,video,root chrome \
#         && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

# Intstall this stuff for caching
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Codebase
COPY setup.py ./
COPY scraper/ ./scraper/.
RUN python3.6 setup.py install

# Tests and everything else
COPY . .

ENV NAME scraper
