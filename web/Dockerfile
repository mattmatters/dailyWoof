FROM golang:1.9.2

WORKDIR /go/src/app

# Install Golang dependencies
RUN go get -u github.com/golang/dep/cmd/dep
RUN go get github.com/gin-gonic/gin
RUN go get github.com/go-redis/redis

# Install Node, npm, and other related stuff to get all of npm's stuff to work
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
        apt-get update && apt-get install -y nodejs tar bzip2 libfontconfig && \
        npm install npm@latest -g

# Install npm dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Build the source code
COPY . .
RUN npm run build
RUN go-wrapper download   # "go get -d -v ./..."
RUN go-wrapper install    # "go install -v ./..."

CMD ["go-wrapper", "run"] # ["app"]