#!/bin/bash

# Unit tests
docker-compose build
docker-compose run scraper python setup.py lint
docker-compose run scraper python setup.py test
docker-compose run web go test
docker-compose run frontend npm test
docker-compose down
