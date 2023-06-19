# ITS Backend

## Setup Dev Environment
- Install [Docker Compose](https://docs.docker.com/compose/)
- Install [dotnet](https://dotnet.microsoft.com/en-us/download/dotnet/7.0)
- Install database tools `dotnet tool install --global dotnet-ef`

## Run Backend
Start the database (it needs to be running for the EF Core):
```bash
docker-compose up
```
Build the app:
```bash
dotnet build
```
Configure database:
```bash
dotnet ef database update
```
Run the app:
```bash
dotnet run
```