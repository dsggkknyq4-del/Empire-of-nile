# Developer Package MVP Backend

This repository contains the backend implementations for:
1. **MoneyPilot** (Finance AI)
2. **TongueForge** (Language AI)
3. **Empire of Nile** (Simulation Game)

## Structure
- `src/shared`: Core modules (Config, Logging, Security, DB, AI) used by all services.
- `src/moneypilot`: MoneyPilot service code.
- `src/tongueforge`: TongueForge service code.
- `src/empire`: Empire of Nile service code.

## Prerequisites
- Python 3.12+
- Docker & Docker Compose

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Infrastructure (PostgreSQL)**:
   ```bash
   docker-compose up -d
   ```
   *Note: This starts Postgres on port 5432 and Adminer on port 8080.*

## Running Services

You can run each service independently (e.g., in separate terminals):

### MoneyPilot (Port 8000)
```bash
uvicorn src.moneypilot.main:app --port 8000 --reload
```
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### TongueForge (Port 8001)
```bash
uvicorn src.tongueforge.main:app --port 8001 --reload
```
Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

### Empire of Nile (Port 8002)
```bash
uvicorn src.empire.main:app --port 8002 --reload
```
Docs: [http://localhost:8002/docs](http://localhost:8002/docs)

## Configuration
Copy `.env.example` (if provided) or set environment variables as defined in `src/shared/core/config.py`.
- `OPENAI_API_KEY`: Required for AI features in MoneyPilot and TongueForge.
- `DATABASE_URL`: Defaults to local docker settings.
