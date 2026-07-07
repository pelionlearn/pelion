import os
from dotenv import load_dotenv
from openai import OpenAI

from embeddings import NemotronEmbedding

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

embeddings = NemotronEmbedding(client)

vector = embeddings.embed_query("What is OpenRouter?")
print(vector[:5])
