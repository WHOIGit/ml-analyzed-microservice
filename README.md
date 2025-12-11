# Ml-analyzed Microservice

A microservice for obtaining the ml_analyzed metric for a specified IFCB bin.

- `GET /ml_analyzed/{bin_id}` — Computes and returns the ml_analyzed value (volume analyzed in mL) for the specified IFCB bin.

## Run with Docker Compose

```bash
docker compose up --build
```

## Configuration

Create a `.env` file from the template:

```bash
cp dotenv.template .env
```

Edit `.env` to set your IFCB data directory:

```
DATA_DIR=/path/to/your/ifcb-data
PORT=8001
```

## Request Example

```bash
curl http://localhost:8001/ml_analyzed/D20120101_T120000
```

Response:
```
0.245
```
