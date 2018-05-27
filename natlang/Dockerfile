FROM python:3.6.5-alpine
WORKDIR /usr/src/natlang

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Intstall this stuff for caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Codebase
COPY setup.py ./
COPY natlang/ ./natlang/.

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m textblob.download_corpora && \
    python setup.py install

# Tests and everything else
COPY . .

ENV NAME natlang
