import os
import sys
import asyncio
import logging

from dotenv import load_dotenv
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio as atqdm

import json
import difflib
import deepdiff as dd
import jsondiff as jd

from langchain_text_splitters import RecursiveCharacterTextSplitter

from neo4j import GraphDatabase, Driver
from neo4j_graphrag.exceptions import SchemaValidationError, SchemaExtractionError
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.types import (
    TextChunks,
    DocumentInfo,
    Neo4jGraph,
)
from neo4j_graphrag.experimental.components.schema import (
    SchemaBuilder,
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
    ConstraintType,
)
from neo4j_graphrag.experimental.components.schema import SchemaFromTextExtractor
from neo4j_graphrag.experimental.components.text_splitters.langchain import (
    LangChainTextSplitterAdapter,
)
from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
from neo4j_graphrag.experimental.components.lexical_graph import LexicalGraphBuilder
from neo4j_graphrag.experimental.components.types import LexicalGraphConfig
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.components.entity_relation_extractor import (
    LLMEntityRelationExtractor,
)
from neo4j_graphrag.experimental.components.resolver import SpaCySemanticMatchResolver
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


def simple_schema():
    nodes = [
        "Entity",
    ]
    relationships = [
        "RELATES_TO",
    ]
    patterns = [
        ("Entity", "RELATES_TO", "Entity"),
    ]
    return {
        "node_types": nodes,
        "relationship_types": relationships,
        "patterns": patterns,
    }


def book_schema():
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
    return {
        "node_types": nodes,
        "relationship_types": relationships,
        "patterns": patterns,
    }


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


async def split_chunks(splitter: LangChainTextSplitterAdapter, text: str):
    chunks = await splitter.run(text=text)
    return chunks


async def extract_schema(schema_extractor: SchemaFromTextExtractor, text: str):
    while True:
        try:
            schema = await schema_extractor.run(text)
            return schema
        except (SchemaValidationError, SchemaExtractionError) as e:
            tqdm.write("RETRYING: " + str(e))
            continue


async def building_schema(
    schema_builder: SchemaBuilder,
    node_types: list[NodeType],
    relationship_types: list[RelationshipType],
    patterns: list[tuple[str, str, str]],
    constraints: list[ConstraintType],
):
    schema = await schema_builder.run(
        node_types,
        relationship_types,
        patterns,
        constraints,
    )
    return schema


async def embed_chunks(text_chunk_embedder: TextChunkEmbedder, text_chunks: TextChunks):
    embedded_chunks = await text_chunk_embedder.run(text_chunks=text_chunks)
    return embedded_chunks


async def build_graph(
    lexical_graph_builder: LexicalGraphBuilder,
    text_chunks: TextChunks,
    document_info: DocumentInfo | None = None,
):
    graph = await lexical_graph_builder.run(text_chunks, document_info)
    return graph


async def write_graph(driver: Driver, graph: Neo4jGraph):
    writer = Neo4jWriter(driver)
    await writer.run(graph)


async def extract_entities_and_relations(
    extractor: LLMEntityRelationExtractor,
    text_chunks: TextChunks,
    document_info: DocumentInfo | None = None,
    lexical_graph_config: LexicalGraphConfig | None = None,
    schema: GraphSchema | None = None,
):
    graph = await extractor.run(
        text_chunks, document_info, lexical_graph_config, schema
    )
    return graph


async def resolve_entities(resolver: SpaCySemanticMatchResolver):
    res = await resolver.run()
    return res


print("loading documents...")

# files = ["../docs/crime-and-punishment.txt"]
# files = ["../docs/platos-republic.txt"]
files = ["../docs/notes2.txt"]
# files = [
#     "../docs/ela/1.txt",
#     "../docs/ela/2.txt",
#     "../docs/ela/3.txt",
#     "../docs/ela/4.txt",
#     "../docs/ela/5.txt",
# ]
texts = []

# document_info = DocumentInfo()

for file in files:
    with open(file) as f:
        text = f.read()
        texts.append(text)

text = texts[0]

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
    model_name=get_env("LLM_TAG"),
    base_url=get_env("OPENROUTER_BASE_URL"),
    api_key=get_env("OPENROUTER_API_KEY"),
    model_params={
        "max_tokens": 2000,
        "response_format": {"type": "json_object"},
        "temperature": 0.2,  # 0.2
    },
)

print("initializing embeddings...")

embedder = OpenAIEmbeddings(
    model=get_env("EMBEDDING_TAG"),
    base_url=get_env("OPENROUTER_BASE_URL"),
    api_key=get_env("OPENROUTER_API_KEY"),
)

# print("initializing pipeline...")

# kg_builder = SimpleKGPipeline(
#     llm=llm,
#     driver=driver,
#     embedder=embedder,
#     # text_splitter=text_splitter,
#     schema=simple_schema(),
#     from_file=False,
#     perform_entity_resolution=False,
# )

print("building chunks...")

text_splitter = LangChainTextSplitterAdapter(
    RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        separators=[" ", ",", ":", ";", ".", "\n"],
        chunk_size=200,
        chunk_overlap=40,
        keep_separator=True,
    )
)

# text_chunks = []
# for chunks in asyncio.gather(*[split_chunks(text_splitter, text) for text in texts]):
#     text_chunks.extend(chunks)

text_chunks = asyncio.run(split_chunks(text_splitter, text))

# print("building graph...")

# with tqdm(total=len(text_chunks), desc="chunks", file=sys.stdout) as pbar:
#     callbacks = KGCallbacks(pbar)
#     asyncio.run(kg_build(kg_builder, text_chunks, 16, callbacks))


print("extracting schema...")

schema_extractor = SchemaFromTextExtractor(llm=llm, use_structured_output=True)
schema = asyncio.run(extract_schema(schema_extractor, text))

# schemas = []
# for text in tqdm(texts[:2]):
#     schema = asyncio.run(extract_schema(schema_extractor, text))
#     schemas.append(schema.model_dump_json())
#     tqdm.write(schema.model_dump_json())


async def extract_schemas():
    schemas = []
    for task in atqdm.as_completed(
        [extract_schema(schema_extractor, text) for text in texts[:2]]
    ):
        schemas.append(await task)
    return schemas


# schemas_: list[GraphSchema] = asyncio.run(extract_schemas())
# schemas = [schema.model_dump() for schema in schemas_]

# print(jd.diff(schemas[0], schemas[1]))
# print(jd.diff(schemas[0], schemas[1], syntax="explicit"))
# print(jd.diff(schemas[0], schemas[1], syntax="symmetric"))
# print(jd.diff(schemas[0], schemas[1], syntax="rightonly"))
# print(dd.DeepDiff(schemas[0], schemas[1], ignore_order=True))

# print(
#     "".join(
#         difflib.unified_diff(
#             json.dumps(schemas[0], indent=2, sort_keys=True).splitlines(keepends=True),
#             json.dumps(schemas[1], indent=2, sort_keys=True).splitlines(keepends=True),
#             fromfile="schema 0",
#             tofile="schema 1",
#             n=3,
#         )
#     )
# )

# TODO: intelligently merge multiple schemas!!!!
# https://gemini.google.com/app/55b4fb7ad797bb11

# sys.exit()

# schema.additional_node_types = False
# schema.additional_relationship_types = False
# schema.additional_patterns = False

# print("building schema...")

# schema_builder = SchemaBuilder()
# schema = asyncio.run(
#     building_schema(
#         schema_builder,
#         node_types,
#         relationship_types,
#         patterns,
#         contraints,
#     )
# )

print("embedding chunks...")

text_chunk_embedder = TextChunkEmbedder(embedder, max_concurrency=8)
text_chunks = asyncio.run(embed_chunks(text_chunk_embedder, text_chunks))

print("building lexical graph...")

lexical_graph_config = LexicalGraphConfig()
lexical_graph_builder = LexicalGraphBuilder(config=lexical_graph_config)
graph = asyncio.run(build_graph(lexical_graph_builder, text_chunks)).graph

print("writing lexical graph...")

asyncio.run(write_graph(driver, graph))

print("extracting entities and relations...")

extractor = LLMEntityRelationExtractor(
    llm=llm, create_lexical_graph=False, use_structured_output=True
)
graph = asyncio.run(
    extract_entities_and_relations(
        extractor,
        text_chunks,
        document_info=None,
        lexical_graph_config=lexical_graph_config,
        schema=schema,
    )
)

print("writing entities and relations...")

asyncio.run(write_graph(driver, graph))

print("resolving entities...")

resolver = SpaCySemanticMatchResolver(driver)
res = asyncio.run(resolve_entities(resolver))

print("cleaning up...")

driver.close()
