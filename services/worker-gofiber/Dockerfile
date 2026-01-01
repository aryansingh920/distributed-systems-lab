# Build
FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server ./cmd/server

# Run
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/server ./server

ENV PORT=4003
EXPOSE 4003

CMD ["./server"]
