#!/bin/sh

# alembic upgrade head

# uvicorn api.main:app --host 0.0.0.0 --port 5000
uvicorn main:app --host 0.0.0.0 --port 5000
