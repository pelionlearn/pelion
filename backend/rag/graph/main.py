import os
import sys
import asyncio
import logging

from dotenv import load_dotenv

from tqdm import tqdm

from langchain_text_splitters import RecursiveCharacterTextSplitter

from neo4j import GraphDatabase
import neo4j_graphrag.exceptions
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM

load_dotenv()

# logging.basicConfig(level=logging.DEBUG)


def get_env(key):
    val = os.environ.get(key)
    if val is None:
        print(
            f"Required key {key} not found in environment. Make sure .env is configured correctly."
        )
        exit(1)
    return val


class KGCallbacks:
    def __init__(self, pbar: tqdm):
        self.pbar = pbar

    def inc(self):
        self.pbar.update(1)

    def write(self, msg):
        pass
        # self.pbar.write(msg, end="\n")
        # self.pbar.refresh()
        # with tqdm.external_write_mode():
        #     print(f"\033[1A\033[999C{msg}\r", flush=True)


async def kg_task(
    kg_builder: SimpleKGPipeline,
    text: str,
    callbacks: KGCallbacks,
):
    while True:
        try:
            await kg_builder.run_async(text=text)
            break
        except Exception:
            callbacks.write("e")
            continue


async def kg_worker(
    queue: asyncio.Queue,
    kg_builder: SimpleKGPipeline,
    callbacks: KGCallbacks,
):
    while True:
        try:
            text = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        while True:
            try:
                callbacks.write(".")
                await kg_task(kg_builder, text, callbacks)
                break
            except Exception as e:
                logging.exception(e)
                continue

        callbacks.write("x")
        callbacks.inc()
        queue.task_done()


async def kg_build(
    kg_builder: SimpleKGPipeline,
    texts: list[str],
    max_concurrency: int,
    callbacks: KGCallbacks,
):
    queue = asyncio.Queue()

    for text in texts:
        await queue.put(text)

    workers = [
        asyncio.create_task(kg_worker(queue, kg_builder, callbacks))
        for _ in range(min(max_concurrency, len(texts)))
    ]
    await queue.join()


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    separators=[" ", ",", ":", ";", ".", "\n"],
    chunk_size=1000,
    chunk_overlap=200,
    keep_separator=True,
)

files = ["../docs/crime-and-punishment.txt"]
# files = ["../docs/platos-republic.txt"]
# files = ["../docs/notes2.txt"]
texts = []

for file in files:
    with open(file) as f:
        text = f.read()
        texts.append(text)

text_chunks = text_splitter.split_text(texts[0])

print("initializing graph...")

driver = GraphDatabase.driver(
    get_env("_NEO4J_URI"),
    auth=(
        get_env("_NEO4J_USERNAME"),
        get_env("_NEO4J_PASSWORD"),
    ),
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

print("initializing pipeline...")

nodes = [
    "Book",
    "Chapter",
    "Event",
    "Person",
    "Motivation",
    "Theme",
]
relationships = [
    "CONTAINS",
    "IS_BEFORE",
    "PARTICIPATES_IN",
    "MOTIVATED_BY",
    "INTERACTS_WITH",
    "RELATES_TO",
]
patterns = [
    # storyline sequence
    ("Book", "CONTAINS", "Chapter"),
    ("Chapter", "CONTAINS", "Event"),
    ("Chapter", "IS_BEFORE", "Chapter"),
    ("Event", "IS_BEFORE", "Event"),
    # character analysis
    ("Person", "PARTICIPATES_IN", "Event"),
    ("Person", "MOTIVATED_BY", "Motivation"),
    ("Person", "INTERACTS_WITH", "Person"),
    # themes
    ("Book", "RELATES_TO", "Theme"),
    ("Chapter", "RELATES_TO", "Theme"),
    ("Event", "RELATES_TO", "Theme"),
    ("Person", "RELATES_TO", "Theme"),
    ("Motivation", "RELATES_TO", "Theme"),
    ("Theme", "RELATES_TO", "Theme"),
]

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=driver,
    embedder=embedder,
    schema={
        "node_types": nodes,
        "relationship_types": relationships,
        "patterns": patterns,
    },
    from_file=False,
)

print("building graph...")


with tqdm(total=len(text_chunks), desc="chunks", file=sys.stdout) as pbar:
    callbacks = KGCallbacks(pbar)
    asyncio.run(kg_build(kg_builder, text_chunks, 16, callbacks))

print("cleaning up...")

driver.close()
