# FastAPI Chatbot with Redis

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd chat
```

2. Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
REDIS_URL=redis://redis:6379/0
```

## Run the Application

Build and start the containers:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

## API Documentation

Open Swagger UI:

```
http://localhost:8000/docs
```

## Stop the Application

```bash
docker compose down
```

## Check Running Containers

```bash
docker ps
```

## View Logs

Application:

```bash
docker logs -f chat-app
```

Redis:

```bash
docker logs -f chat-redis
```
