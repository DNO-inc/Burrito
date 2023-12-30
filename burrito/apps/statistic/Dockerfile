FROM golang:alpine AS builder

ENV APP_PATH=burrito/apps/statistic

WORKDIR /app

COPY $APP_PATH/go.mod $APP_PATH/go.sum ./

RUN go mod download

COPY $APP_PATH .

RUN go build -o main .

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
