docker compose -f infra/docker/docker-compose.yml up --build


# docker ps
# docker stop api-express validator-fastapi orchestrator-spring worker-gofiber api-dotnet

docker exec -it kafka bash -lc "kafka-topics --bootstrap-server kafka:9092 --list | head -n 20"                                                                                              

docker exec -it mysql mysql -uapp -papp -D orders_db \  -e "SELECT order_id,user_id,amount,currency,created_at FROM order_events ORDER BY id DESC LIMIT 5;"


docker compose -f infra/docker/docker-compose.yml down

docker compose -f infra/docker/docker-compose.yml up --build

docker compose -f infra/docker/docker-compose.yml logs -f --tail=100


docker logs -f --tail=200 api-express
docker logs -f --tail=200 validator-fastapi
