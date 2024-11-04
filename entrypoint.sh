#!/bin/sh

alembic revision --autogenerate -m "create users table"

alembic upgrade head

echo "Starting FastAPI application..."
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload