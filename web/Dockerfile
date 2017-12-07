FROM golang:1.9.2

WORKDIR /go/src/app

# Install Golang dependencies
RUN go get -u github.com/golang/dep/cmd/dep
RUN go get github.com/gin-gonic/gin
RUN go get github.com/go-redis/redis

# Build the source code
COPY . .
RUN go-wrapper download   # "go get -d -v ./..."
RUN go-wrapper install    # "go install -v ./..."

CMD ["go-wrapper", "run"] # ["app"]