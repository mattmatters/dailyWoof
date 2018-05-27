FROM python:3.6.5-alpine
WORKDIR /usr/src/natlang

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
