import os
import shutil
from pathlib import Path
from typing import Annotated
from uuid import UUID

import chromadb
from dotenv import load_dotenv
from fastapi import Depends, UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from liteparse import LiteParse
from liteparse.types import ParseError
from pydantic import SecretStr

load_dotenv()

STORAGE_LOCATION = Path(os.environ["STORAGE_LOCATION"])

chroma_client = None
chroma_embeddings = None
parser = None
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400,
    separators=["\n\n", "\n", ".", "!", "?", ";", ":", ",", " ", ""],
    keep_separator="end",
)


def lazy_load():  # type: ignore
    global chroma_client, chroma_embeddings, parser
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
    if parser is None:
        parser = LiteParse(ocr_enabled=True, output_format="markdown")


# TODO: reads entire file into memory, implement proper streaming
async def save_file(
    file: UploadFile,
    documentId: UUID,
    # client: Annotated[chromadb.AsyncHttpClient, Depends(get_chroma_client)],  # type: ignore
):
    lazy_load()
    assert chroma_client
    assert chroma_embeddings
    assert parser

    file_ending = "." + file.filename.split(".")[-1] if file.filename else ""
    destination = STORAGE_LOCATION / (str(documentId) + file_ending)
    # contents = file.file.read()

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        # buffer.write(contents)

    # TODO: add error handling for failure to write

    try:
        text = parser.parse(str(destination)).text
    except ParseError:
        text = ""
        with destination.open("r") as buffer:
            text = buffer.read()

    # chunk
    chunks = text_splitter.split_text(text)
    docs = [
        Document(page_content=chunk, metadata={"source": file.filename})
        for chunk in chunks
    ]
    print(docs)

    for doc in docs:
        assert isinstance(doc, Document)

    # add to chromadb
    vectorstore = Chroma(
        client=chroma_client,  # type: ignore
        collection_name="embedding_collection",
        embedding_function=chroma_embeddings,
    )
    vectorstore.add_documents(docs)

    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": destination.stat().st_size,
    }
