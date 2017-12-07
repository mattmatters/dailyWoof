FROM node:9.2

WORKDIR /go/src/app

# Install Node, npm, and other related stuff to get all of npm's stuff to work
RUN  apt-get update && apt-get install -y tar bzip2 libfontconfig

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . .

RUN npm run build
