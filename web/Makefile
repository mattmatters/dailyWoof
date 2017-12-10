.PHONY: dep build doc fmt lint dev

build: vet test
	go build -v -o ./bin/app


# https://github.com/golang/lint
# go get github.com/golang/lint/golint
lint:
	golint ./...

dev:
#	go get && go install && PORT=7000 DEBUG=* gin -p 9000 -a 7000 -i run
	echo "something"
test:
	go test ./...

vet:
	go vet ./...

dep:
	dep ensure
