docker compose -f infra/docker/docker-compose.yml up --build


# docker ps
# docker stop api-express validator-fastapi orchestrator-spring worker-gofiber api-dotnet


docker compose -f infra/docker/docker-compose.yml down
docker compose -f infra/docker/docker-compose.yml up --build
