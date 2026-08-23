from fastapi import APIRouter

from workers.celery_app import celery_app

from schemas.coref import (
    CorefResolveSubmitRequest,
    CorefResolveSubmitResponse,
    CorefResolveStatusRequest,
    CorefResolveStatusResponse,
)

router = APIRouter(prefix="/coref", tags=["Coref"])

# we dont want coref publically accessible idk why i wrote any of this

# @router.post("/submit", response_model=CorefResolveSubmitResponse)
# async def submit_coref(request: CorefResolveSubmitRequest):
#     text = request.text
#     task = celery_app.send_task("resolve_coreferences", args=[text])
#     return CorefResolveSubmitResponse(task_id=task.id)


# @router.get("/status/{task_id}", response_model=CorefResolveStatusResponse)
# async def get_status(task_id: str):
#     result = celery_app.AsyncResult(task_id)
#     print("got this far, tryna return the response")
#     print(type(result.state), result.state)
#     print(type(result.result), result.result)
#     return CorefResolveStatusResponse(state=result.state, result=str(result.result))
