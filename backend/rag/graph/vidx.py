import os

from dotenv import load_dotenv

from tqdm import tqdm

from neo4j import GraphDatabase
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.indexes import create_vector_index
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.retrievers import VectorRetriever

load_dotenv()


def get_env(key):
    val = os.environ.get(key)
    if val is None:
        print(
            f"Required key {key} not found in environment. Make sure .env is configured correctly."
        )
        exit(1)
    return val


print("initializing graph...")

driver = GraphDatabase.driver(
    get_env("_NEO4J_URI"),
    auth=(
        get_env("_NEO4J_USERNAME"),
        get_env("_NEO4J_PASSWORD"),
    ),
)

print("initializing vector index...")

create_vector_index(
    driver,
    "vector-index",
    label="Chunk",
    embedding_property="embedding",
    dimensions=1024,
    similarity_fn="euclidean",
)

print("initializing llm...")

llm = OpenAILLM(
    model_name="mistralai/mistral-nemo",
    base_url="https://openrouter.ai/api/v1",
    api_key=get_env("OPENROUTER_API_KEY"),
    model_params={
        "max_tokens": 2000,
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    },
)

print("initializing embeddings...")

embedder = OpenAIEmbeddings(
    model="perplexity/pplx-embed-v1-0.6b",
    base_url="https://openrouter.ai/api/v1",
    api_key=get_env("OPENROUTER_API_KEY"),
)

print("initializing vector retriever...")

retriever = VectorRetriever(driver, "vector-index", embedder)

print("initializing graphrag...")

rag = GraphRAG(retriever=retriever, llm=llm)

query_text = "What is the difference between a microcontroller and microprocessor?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
driver.close()

print("\nWITHOUT RAG\n")

print(llm.invoke(query_text))
