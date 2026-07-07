import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document

from embeddings import NemotronEmbedding

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

embedding_function = NemotronEmbedding(client)

vector = embedding_function.embed_query("What is OpenRouter?")
print(vector[:5])

vector_store = Chroma(collection_name="pelion", embedding_function=embedding_function)

document_1 = Document(page_content="i am hungry")
document_2 = Document(page_content="openrouter gives me free ai models")
document_3 = Document(
    page_content="nvidia gives me free ai models but it steals all my data to train them"
)

documents = [document_1, document_2, document_3]
vector_store.add_documents(documents)

print(vector_store.similarity_search("food", 1))
