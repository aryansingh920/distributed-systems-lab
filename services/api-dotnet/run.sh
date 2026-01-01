cd ApiDotnet
dotnet restore
dotnet run



docker build -t api-dotnet:dev ./services/api-dotnet
docker run --rm -p 4004:4004 api-dotnet:dev
