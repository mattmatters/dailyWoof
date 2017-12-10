FROM golang:1.9.2

WORKDIR /go/src/app

# Tools
RUN go get -u github.com/golang/lint/golint
RUN go get -u github.com/golang/dep/cmd/dep

COPY . .
RUN dep ensure
RUN make
