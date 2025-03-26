#!/usr/bin/env bash
set -eu

export PYTHONPATH="src"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="password"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="todo"

exec "$@"
