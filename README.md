# Pelion

## Frontend

In the `frontend/` directory, run `npm install` and then `npm run dev`.

## Backend

### Development and usage

In the root directory, copy `.env.example` to `.env.`. Fill in your API key.

**For local development:**

In each backend component directory (each one except `frontend/`), run `uv sync`.
Use `uv run main.py` to run each backend componenet.

In the `api/` directory, run `uv run uvicorn main:app --reload --port 5000` to run the middleware.

**For production/testing:**

In the root directory, run `docker compose up` to build and run all containers.
