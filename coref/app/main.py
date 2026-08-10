import os
import urllib.parse
from itertools import pairwise

import spacy
from celery import Celery
from celery.signals import worker_process_init
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from fastcoref import spacy_component  # type: ignore
# from fastcoref.spacy_component import LingMessCoref

from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ["HF_HUB_OFFLINE"] = "1"
load_dotenv()

REDIS_PASSWORD = urllib.parse.quote(os.environ.get("REDIS_PASSWORD", ""))
MODEL_PATH = os.environ.get("MODEL_PATH", "model")

celery_app = Celery(
    "tasks",
    broker=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
    backend=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
)
celery_app.conf.task_track_started = True
# default is 1 day, in seconds, 600s=10min, 3600s=1hr
celery_app.conf.result_expires = 600
# celery_app.conf.worker_max_tasks_per_child = 1
# celery_app.conf.worker_redirect_stdouts = False
celery_app.conf.worker_proc_alive_timeout = 10.0

logger = get_task_logger(__name__)

nlp = None
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    separators=["\n\n", "\n", ".", "!", "?", ";", ":", ",", " ", ""],
    keep_separator="end",
)


def init_nlp():
    global nlp

    nlp = spacy.load(
        "en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"]
    )

    logger.info("[init_nlp] loaded model")

    nlp.add_pipe(
        "fastcoref",
        config={
            "model_architecture": "LingMessCoref",
            "model_path": MODEL_PATH,
            # "device": "cpu",
            # "model_path": "biu-nlp/lingmess-coref",
        },
        # config={"model_architecture": "FCoref", "model_path": MODEL_PATH},
    )
    logger.info("[init_nlp] added pipe")


@worker_process_init.connect
def init_worker_instance(**kwargs):
    logger.info("[init_worker_instance] init")


def resolve_text(text: str) -> tuple[str, list[list[tuple[int, int]]]]:
    if nlp is None:
        init_nlp()
    if nlp is None:  # for type checking
        raise RuntimeError("fastcoref nlp pipeline is not initialized")
    doc = nlp(text, component_cfg={"fastcoref": {"resolve_text": True}})
    return (doc._.resolved_text, doc._.coref_clusters)


@celery_app.task(name="resolve_coreferences")
def resolve_coreferences(text: str):
    chunks = text_splitter.split_text(text)
    resolved_chunks: list[str] = []

    # return resolve_text(text)[0]

    logger.info(f"BEGIN RESOLVE CHUNK {chunks[0]}")
    resolved_chunks.append(resolve_text(chunks[0])[0])
    logger.info(f"FINISH RESOLVE CHUNK {resolved_chunks[-1]}")

    for curr_chunk in chunks[1:]:
        logger.info(f"BEGIN RESOLVE CHUNK {curr_chunk}")
        prev_chunk = resolved_chunks[-1]
        prev_len = len(prev_chunk)
        combined_chunk = prev_chunk + curr_chunk
        clusters = resolve_text(combined_chunk)[1]
        replacements: list[tuple[int, int, str]] = []

        for cluster in clusters:
            src = cluster[0]
            src_str = combined_chunk[src[0] : src[1]]
            dests = cluster[1:]
            for dest in dests:
                replacements.append((dest[0], dest[1], src_str))

        replacements = [
            (rep[0] - prev_len, rep[1] - prev_len, rep[2])
            for rep in replacements
            if rep[0] >= prev_len
        ]
        replacements = sorted(replacements, key=lambda x: x[0], reverse=True)
        for start, end, new_str in replacements:
            curr_chunk = curr_chunk[:start] + new_str + curr_chunk[end:]
        resolved_chunks.append(curr_chunk)
        logger.info(f"FINISH RESOLVE CHUNK {curr_chunk}")

    # doc = nlp(text, component_cfg={"fastcoref": {"resolve_text": True}})
    # logger.info(doc._.resolved_text)
    # logger.info(doc._.coref_clusters)
    # return {"clusters": doc._.coref_clusters, "resolved": doc._.resolved_text}
    # return {"resolved": "".join(resolved_chunks)}
    return "".join(resolved_chunks)
