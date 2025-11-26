FROM node:18.19.0 AS FRONT
WORKDIR /web
COPY ./web .
RUN yarn install --frozen-lockfile --network-timeout 1000000 && yarn run build

FROM golang:1.20.12 AS BACK
WORKDIR /go/src/caswaf
COPY . .

COPY ./ip ./ip

# RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o server . \
#    && apt update && apt install wait-for-it && chmod +x /usr/bin/wait-for-it

RUN apt update && apt install -y curl ca-certificates \
    && curl -o /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o server .

FROM alpine:latest AS STANDARD
LABEL MAINTAINER="https://caswaf.org/"

#COPY --from=BACK /go/src/caswaf/ ./
#COPY --from=BACK /usr/bin/wait-for-it ./
COPY --from=BACK /go/src/caswaf/server .
COPY --from=BACK /usr/local/bin/wait-for-it .
COPY --from=BACK /go/src/caswaf/ip ./ip

RUN mkdir -p web/build && apk add --no-cache bash coreutils
RUN apk add --no-cache tzdata
COPY --from=FRONT /web/build /web/build
ENTRYPOINT ["./wait-for-it", "db:3306", "--", "./server"]

