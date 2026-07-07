import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY"),
)

response = client.embeddings.create(
  model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
  input=[
    {
      "content": [
        {"type": "text", "text": "What is in this image?"}
      ]
    }
  ],
  encoding_format="float"
)

vector = response.data[0].embedding[:5]
print(vector)