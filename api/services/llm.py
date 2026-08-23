import os
from uuid import UUID

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import SecretStr

load_dotenv()

llm_client = None
chroma_client = None
chroma_embeddings = None


def lazy_load():
    global llm_client, chroma_client, chroma_embeddings
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


async def get_llm_response(
    prev_messages: list[dict[str, str]],
    user_message: str,
    classroom_id: UUID,
):
    lazy_load()
    assert llm_client

    vectorstore = Chroma(
        client=chroma_client,
        collection_name=str(classroom_id),
        embedding_function=chroma_embeddings,
    )

    squashed_messages = []
    i = 0
    while i < len(prev_messages):
        prev_message = prev_messages[i]
        if prev_message["role"] == "assistant":
            squashed_messages.append(prev_message)
        elif prev_message["role"] == "rag":
            if i < len(prev_messages) - 1 and prev_messages[i + 1]["role"] == "user":
                next_prev_message = prev_messages[i + 1]
                squashed_message = {
                    "role": "user",
                    "content": prev_message["content"] + next_prev_message["content"],
                }
                squashed_messages.append(squashed_message)
                i += 1
            else:
                raise Exception(
                    "malformed message roles: rag message not followed by user message"
                )
        i += 1

    results = vectorstore.similarity_search(user_message, k=5)

    rag_context = "\n".join(
        [
            f'<source id="{result.metadata["source"]}">\n{result.page_content}\n</source>\n'
            for result in results
        ]
    )
    rag_part = f"[Retrieved Context]\n{rag_context}\n\n[User Query]\n"
    usr_part = f"{user_message}"
    prompt = f"{rag_part}{usr_part}"
    messages = squashed_messages[:]
    messages.append({"role": "user", "content": prompt})
    print(messages)

    response = None

    async for chunk in llm_client.astream(messages):
        if response is None:
            response = chunk
        else:
            response += chunk
        # print(chunk.content, end="")

    assert response

    return rag_part, usr_part, response.content
