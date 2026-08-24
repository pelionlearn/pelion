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

### RAG Pipeline

The current pipeline features a simple ChromaDB vector database. When a document is uploaded it is chunked into multiple parts, each of which are run through an embedding model and stored in the database. When the user queries the AI, the query is embedded and the top 5 most relevant queries are pulled from the vector database. These top 5 chunks are then prepended to the user's message so that the LLM can see relevant information and incorporate it into its answer, providing high accuracy and personalization.

The final pipeline will be much more complex. The pipeline will feature multiple stages and an event-driven architecture for dynamic, robust scaling.

1. Start: The pipeline begins automatically when a user uploads a document.
2. Coreference resolution: pronouns and other references are replaced with their original entities to reduce the ambiguity associated with isolated text chunks.
3. Chunking: The resolved document is split into individual chunks, respecting paragraph, newline, and word boundaries wherever possible.
4. These text chunks are then passed into two parallel processes:
   - Embedding: the chunks are run through an embedding model to extract semantic vectors, which will be stored in the Neo4J database.
   - Schema extraction: an LLM loops over the chunks and builds a graph schema that will be used to construct the Neo4J graph.
5. Lexical graph: The vector embeddings are then used to build a simple graph stored in the Neo4J database where each plain text chunk is connected to its embedded vector for fast lookups.
6. Entity and relation extraction: LLMs are provided with the extracted schema and run over the text chunks, extracting nodes and relations to store alongside the lexical graph.
7. Finally, the Neo4J database undergoes a finishing pass to merge duplicate entities and relationships.

All pipeline stages are undergoing development. Current challenges include:

- Improving the accurency and performance of coreference resolution for long and complex texts
- Merging extracted schemas from each text chunk into a single schema
- Improving the accurancy and cleanliness of the entity and relation extraction
- Reducing API calls and costs
