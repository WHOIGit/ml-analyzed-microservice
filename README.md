# Ml-analyzed Microservice

A microservice for obtaining the ml_analyzed metric for a specified IFCB bin. 

- `POST /echo` — Echoes the request content back to the user.

## Run with Docker Compose

```bash
docker compose up --build
```

## Request Example

```bash
curl -X POST http://localhost:8051/echo \
  -H "Content-Type: application/json" \
  -d '{
        "content": "hello service!"
      }'
```
