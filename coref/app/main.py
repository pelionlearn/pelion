import os
import urllib.parse

import spacy
from fastcoref import spacy_component  # type: ignore

from dotenv import load_dotenv
from celery import Celery
from celery.signals import worker_process_init
from celery.utils.log import get_task_logger

os.environ["HF_HUB_OFFLINE"] = "1"
load_dotenv()

REDIS_PASSWORD = urllib.parse.quote(os.environ.get("REDIS_PASSWORD", ""))

celery_app = Celery(
    "tasks",
    broker=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
    backend=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
)
celery_app.conf.task_track_started = True
# celery_app.conf.worker_redirect_stdouts = False


logger = get_task_logger(__name__)

nlp = None
MODEL_PATH = os.getenv("MODEL_PATH", "model")


@worker_process_init.connect
def init_worker_instance(**kwargs):
    global nlp

    logger.info("[init_worker_instance] init")

    nlp = spacy.load(
        "en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"]
    )

    logger.info("[init_worker_instance] loaded model")

    # there's also LingMessCoref but its broken :(
    nlp.add_pipe(
        "fastcoref",
        config={
            "model_architecture": "FCoref",
            "model_path": MODEL_PATH,
            # "device": "cpu",
            # "local_files_only": True,
            # "resolve_text": True,
        },
    )

    logger.info("[init_worker_instance] added pipe")


@celery_app.task(name="resolve_coreferences")
def resolve_coreferences(text: str):
    global nlp

    logger.info("[resolve_coreferences] init")

    if nlp is None:
        raise RuntimeError("NLP not initialized!!! >w<")

    doc = nlp(text, component_cfg={"fastcoref": {"resolve_text": True}})

    logger.info("[resolve_coreferences] ran inference")

    resolved_text = doc._.resolved_text
    return resolved_text
