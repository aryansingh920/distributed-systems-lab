# cd services/api-express
# npm i
npm run dev



docker build -t api-express:dev ./services/api-express
docker run --rm -p 4000:4000 api-express:dev
