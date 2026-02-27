# AI-Powered Audit Evidence Review Assistant Backend

This repository contains a FastAPI backend for the MVP of an audit evidence review assistant. The system accepts document uploads, extracts structured text, applies deterministic risk rules, and generates draft working papers using Amazon Bedrock.

## Features

- JWT authentication (register/login)
- Engagement management (create, list, retrieve)
- Document upload (PDF/DOCX/CSV) with S3 storage
- Text extraction and field parsing
- Rule-based risk engine
- Amazon Bedrock integration for working paper summaries
- PostgreSQL (async SQLAlchemy) persistence
- Docker and Docker Compose ready
- Health check endpoint

## Setup

1. Copy `.env` and customize your configuration.
2. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Apply migrations:
   ```bash
   docker exec -it <backend_container> alembic upgrade head
   ```

## Endpoints

- `POST /auth/register` - register new user
- `POST /auth/login` - obtain JWT token
- `POST /engagements` - create engagement
- `GET /engagements` - list user's engagements
- `GET /engagements/{id}` - retrieve specific engagement
- `POST /engagements/{id}/upload` - upload document
- `POST /engagements/{id}/generate-summary` - generate working paper
- `GET /health` - health check

## Notes

- AWS credentials should be provided via environment or IAM role.
- The risk engine rules are modular and extendable.

## Dependencies

See `requirements.txt` for a full list of Python packages.
