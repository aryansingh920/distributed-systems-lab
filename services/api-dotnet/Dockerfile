# Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ApiDotnet/ApiDotnet.csproj ApiDotnet/
RUN dotnet restore ApiDotnet/ApiDotnet.csproj

COPY ApiDotnet/ ApiDotnet/
WORKDIR /src/ApiDotnet
RUN dotnet publish -c Release -o /app/publish --no-restore

# Run
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://0.0.0.0:4004
EXPOSE 4004

ENTRYPOINT ["dotnet", "ApiDotnet.dll"]
