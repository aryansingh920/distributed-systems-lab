# cd services/worker-gofiber
go mod tidy
go run ./cmd/server


docker build -t worker-gofiber:dev ./services/worker-gofiber
docker run --rm -p 4003:4003 worker-gofiber:dev
