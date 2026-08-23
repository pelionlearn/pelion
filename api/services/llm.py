import os

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import SecretStr

load_dotenv()

llm_client = None
chroma_client = None
chroma_embeddings = None
vectorstore = None


def lazy_load():
    global llm_client, chroma_client, chroma_embeddings, vectorstore
    if llm_client is None:
        llm_client = ChatOpenAI(
            model=os.environ["LLM_TAG"],
            base_url=os.environ["OPENROUTER_BASE_URL"],
            api_key=SecretStr(os.environ["OPENROUTER_API_KEY"]),
        )
    if chroma_client is None:
        chroma_client = chromadb.HttpClient(
            os.environ["CHROMA_HOST"],  # "localhost"
            int(os.environ["CHROMA_PORT"]),
        )
    if chroma_embeddings is None:
        chroma_embeddings = OpenAIEmbeddings(
            model=os.environ["EMBEDDING_TAG"],
            base_url=os.environ["OPENROUTER_BASE_URL"],
            api_key=SecretStr(os.environ["OPENROUTER_API_KEY"]),
            check_embedding_ctx_length=False,
            model_kwargs={"encoding_format": "float"},
        )
    if vectorstore is None:
        vectorstore = Chroma(
            client=chroma_client,
            collection_name="embedding_collection",
            embedding_function=chroma_embeddings,
        )


async def get_llm_response(prev_messages: list[dict[str, str]], user_message: str):
    lazy_load()
    assert vectorstore
    assert llm_client

    results = vectorstore.similarity_search(user_message, k=5)

    rag_context = "\n".join(
        [
            f'<source id="{result.metadata["source"]}">\n{result.page_content}\n</source>\n'
            for result in results
        ]
    )
    rag_prompt = f"[Retrieved Context]\n{rag_context}\n\n[User Query]\n{user_message}"
    messages = prev_messages[:]
    messages.append({"role": "user", "content": rag_prompt})
    # print(messages)

    response = None

    async for chunk in llm_client.astream(messages):
        if response is None:
            response = chunk
        else:
            response += chunk
        # print(chunk.content, end="")

    assert response

    return rag_prompt, response.content
