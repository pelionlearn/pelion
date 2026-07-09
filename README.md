# Pelion

## Backend

### Development and usage

In the `backend/` directory, copy `.env.example` to `.env.`. Fill in your API key.

**For local development:**

In the `backend/` directory, run `uv sync` in the `backend/` to install dependencies. Use `uv run main.py` to run the backend (or activate the `.venv` and run normally).

In the `backend/` directory, run `uv run uvicorn main:app --reload --port 5000` to run the middleware.

In the `frontend/` directory, run `npm run dev`.

**For production/testing:**

In the root directory, run `docker compose up` to build and run the backend container.
