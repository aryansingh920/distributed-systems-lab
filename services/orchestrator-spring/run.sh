# cd services/orchestrator-spring

mvn -v
mvn spring-boot:run



docker build -t orchestrator-spring:dev ./services/orchestrator-spring
docker run --rm -p 4002:4002 orchestrator-spring:dev

