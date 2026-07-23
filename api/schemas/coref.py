from pydantic import BaseModel


class CorefResolveSubmitRequest(BaseModel):
    text: str


class CorefResolveSubmitResponse(BaseModel):
    task_id: str


class CorefResolveStatusRequest(BaseModel):
    task_id: str


class CorefResolveStatusResponse(BaseModel):
    state: str
    result: str
