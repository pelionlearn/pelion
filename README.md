# Pelion

Pelion was born out of a desire to make studying more collaborative, organized, and integrated with the digital resources you already use every day.

## Features

- Classroom Organization: create classrooms and share your notes with others
- Collaborative Notes System: save your study notes, making them accessible to others in your classroom and to your AI tutor
- AI Tutor: chat to an AI tutor which can read your notes
- Google OAuth: register and sign in with Google; Google Drive integration coming soon

## Setup and Run

### Run Instructions

Create a `.env` based off of `.env.example`. Add your OpenRouter API key, select a model, and modify any secrets listed as needed.
You'll need to create a Google Cloud project and configure OAuth for it.

Pelion uses Docker and Docker Compose. To start Pelion, install Docker and run `docker compose up --build`

### Testing

You can run automated tests with `./scripts/test.sh`, which runs the `docker-compose.test.yml`.

Alternatively, you can start it normally with `docker compose up --build` and then go to `localhost:5000/docs` which has interactive API docs.

## Technical Details

### Tech Stack

**Current Stack**

- Frontend
  - React + React Router
  - TypeScript
- API
  - FastAPI + FastAPI Users
  - LangChain
  - SQLAlchemy
  - LiteParse
  - Resend
- Databases
  - PostgreSQL
  - ChromaDB
- Testing
  - Pytest
- Caddy
- Docker & Docker Compose

**Future Stack**:

- Neo4j
- Redis
- Celery
- FastCoref
- SpaCy
- Alembic
- React Query
- Docling
