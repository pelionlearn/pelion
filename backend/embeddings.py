from langchain_core.embeddings import Embeddings
from typing import List
from openai import OpenAI


class NemotronEmbedding(Embeddings):
    def __init__(self, client: OpenAI):
        self.client = client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
                input=[{"content": [{"type": "text", "text": text}]}],
                encoding_format="float",
            )
            embeddings.append(response.data[0].embedding)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
