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
from pydantic import SecretStr

load_dotenv()

STORAGE_LOCATION = Path(os.environ["STORAGE_LOCATION"])

chroma_client = None
chroma_embeddings = None
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400,
    separators=["\n\n", "\n", ".", "!", "?", ";", ":", ",", " ", ""],
    keep_separator="end",
)


def get_chroma_client_and_embeddings() -> chromadb.HttpClient:  # type: ignore
    global chroma_client, chroma_embeddings
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
    return chroma_client, chroma_embeddings


# TODO: reads entire file into memory, implement proper streaming
async def save_file(
    file: UploadFile,
    documentId: UUID,
    # client: Annotated[chromadb.AsyncHttpClient, Depends(get_chroma_client)],  # type: ignore
):
    client, embeddings = get_chroma_client_and_embeddings()
    destination = STORAGE_LOCATION / str(documentId)
    contents = file.file.read()

    with destination.open("wb") as buffer:
        # shutil.copyfileobj(contents, buffer)
        buffer.write(contents)

    # TODO: add error handling for failure to write

    if file.filename and file.filename.endswith(".txt"):
        # chunk
        chunks = text_splitter.split_text(contents.decode("utf-8"))
        docs = [Document(page_content=chunk, source=file.filename) for chunk in chunks]

        # add to chromadb
        vectorstore = Chroma(
            client=client,  # type: ignore
            collection_name="embedding_collection",
            embedding_function=embeddings,
        )
        vectorstore.add_documents(docs)

    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": destination.stat().st_size,
    }
