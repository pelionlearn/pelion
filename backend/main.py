import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

embedding_model = init_chat_model(
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    model_provider="openrouter"
)

response = model.invoke("Why should I listen to you?")

print(response)