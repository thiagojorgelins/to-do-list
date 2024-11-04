#!/bin/bash

# Aguarda o banco de dados PostgreSQL estar disponível antes de executar as migrações
while ! pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

# Tenta gerar uma nova revisão Alembic se houver mudanças detectadas
alembic revision --autogenerate -m "create migrations"

# Aplica as migrações no banco de dados
alembic upgrade head

# Inicia o aplicativo FastAPI
uvicorn api.app:app --host 0.0.0.0 --port 8000