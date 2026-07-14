from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.errors import (
    NotFoundError,
    ConflictError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ExternalServiceError,
)


async def not_found_handler(request: Request, error: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(error)})


async def conflict_handler(request: Request, error: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(error)})


async def validation_handler(request: Request, error: ValidationError):
    return JSONResponse(status_code=422, content={"detail": str(error)})


async def authentication_handler(request: Request, error: AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": str(error)})


async def authorization_handler(request: Request, error: AuthorizationError):
    return JSONResponse(status_code=403, content={"detail": str(error)})


async def external_service_handler(request: Request, error: ExternalServiceError):
    return JSONResponse(status_code=503, content={"detail": str(error)})
