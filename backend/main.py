import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
# import chromadb

from embeddings import NemotronEmbedding

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

embedding_function = NemotronEmbedding(client)

print("connecting to vector store")
# chroma_client = chromadb.Http

print("initializing vector store...")
vector_store = Chroma(
    collection_name="pelion",
    embedding_function=embedding_function,
    host="chromadb",
)

print("adding documents...")
document_1 = Document(page_content="i am hungry")
document_2 = Document(page_content="openrouter gives me free ai models")
document_3 = Document(
    page_content="nvidia gives me free ai models but it steals all my data to train them",
)
document_4 = Document(
    page_content="i love dogs! dogs have 4 legs and a tail. dogs are really cute and i love to pet them.",
)
documents = [document_1, document_2, document_3, document_4]
vector_store.add_documents(documents=documents, ids=["1", "2", "3", "4"])

print("adding images...")
vector_store.add_images(
    uris=["images/images.jpeg", "images/images (1).jpeg", "images/images (2).jpeg"],
    ids=["cat", "dog", "camel"],
)

print("running similarity search...")
results = vector_store.similarity_search_with_score("dog", 7)

for result in results:
    print(f"id: {result[0].id}, similarity score: {result[1]}")
