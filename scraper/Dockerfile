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
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz \
        && tar -x geckodriver -zf geckodriver-v0.19.1-linux64.tar.gz -O > /usr/bin/geckodriver \
        && chmod +x /usr/bin/geckodriver

RUN rm geckodriver-v0.19.1-linux64.tar.gz

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
