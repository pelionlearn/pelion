import os
import asyncio
import logging
from typing import List
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
import chromadb
from langchain_openrouter import ChatOpenRouter
from langchain_neo4j import Neo4jGraph
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.graphs.graph_document import GraphDocument


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
graph = Neo4jGraph(
    url=get_env("_NEO4J_URI"),
    username=get_env("_NEO4J_USERNAME"),
    password=get_env("_NEO4J_PASSWORD"),
)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    separators=[" ", ",", ":", ";", ".", "\n"],
    # chunk_size=2000,
    # chunk_overlap=250,
    # chunk_size=1000,
    # chunk_overlap=100,
    chunk_size=400,
    chunk_overlap=40,
    keep_separator=True,
)

documents = []
# files = ["docs/notes2.txt"]
# files = ["docs/ela/1.txt", "docs/ela/2.txt", "docs/ela/3.txt", "docs/ela/4.txt", "docs/ela/5.txt"]
# files = ["docs/platos-republic.txt"]
files = ["docs/crime-and-punishment.txt"]

for file in files:
    with open(file) as f:
        text = f.read()
        document = Document(page_content=text, metadata={"filename": file})
        documents.append(document)

documents_chunked = text_splitter.split_documents(documents)
# print(documents)
# print("\n" * 5)
# print(documents_chunked)
# print(len(documents_chunked))
# print(len(documents_chunked[0].page_content))
# exit(1)

print("building graph...")

llm = ChatOpenRouter(
    model="mistralai/mistral-nemo",
    model_kwargs={
        "models": [
            "mistralai/mistral-nemo",
            "meta-llama/llama-3.1-8b-instruct",
        ],
        # "response_format": {"type": "json_object"},
    },
)

graph_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=[
        "BOOK",
        "CHAPTER",
        "EVENT",
        "CHARACTER",
    ],
    allowed_relationships=[
        "CONTAINS_CHAPTER",
        "NEXT_CHAPTER",
        "CONTAINS_EVENT",
        "NEXT_EVENT",
        "PARTICIPATES_IN",
    ],
    node_properties=False,
    strict_mode=True,
)


def aprocess_response_before_callback():
    print(end=".", flush=True)


def aprocess_response_after_callback():
    print(end="x", flush=True)


async def aprocess_response(
    graph_transformer: LLMGraphTransformer,
    document: Document,
) -> GraphDocument | None:
    aprocess_response_before_callback()
    graph_document = await graph_transformer.aprocess_response(document)
    aprocess_response_after_callback()
    return graph_document


async def aprocess_worker(
    queue: asyncio.Queue,
    graph_transformer: LLMGraphTransformer,
    results: list[GraphDocument | Exception | None],
):
    while True:
        try:
            index, document = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        try:
            response = await aprocess_response(graph_transformer, document)
            results[index] = response
        except Exception as e:
            results[index] = e
            logging.exception(e)
        finally:
            queue.task_done()


async def get_graph_docs(
    graph_transformer: LLMGraphTransformer, documents, max_concurrency
):
    queue = asyncio.Queue()
    results: List[GraphDocument | Exception | None] = [None] * len(documents)

    for index, document in enumerate(documents):
        await queue.put((index, document))

    workers = [
        asyncio.create_task(aprocess_worker(queue, graph_transformer, results))
        for _ in range(min(max_concurrency, len(documents)))
    ]
    await queue.join()

    cleaned_results: List = [
        result for result in results if isinstance(result, GraphDocument)
    ]

    return cleaned_results, results


graph_docs, _ = asyncio.run(get_graph_docs(graph_transformer, documents_chunked, 16))
graph.add_graph_documents(graph_docs)
