# Unit tests
docker-compose build
docker-compose run scraper pytest
docker-compose run web go test
docker-compose run frontend npm test
docker-compose down
