from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, documents, classroom_members, classrooms, coref, chats
from exceptions import errors, handlers

from auth.authentication import fastapi_users, auth_backend
from schemas.users import UserCreate, UserRead
from auth.authentication import google_client, OAUTH_SECRET


app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://pelion.jeremyseq.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(errors.NotFoundError, handlers.not_found_handler)
app.add_exception_handler(errors.ConflictError, handlers.conflict_handler)
app.add_exception_handler(errors.ValidationError, handlers.validation_handler)
app.add_exception_handler(errors.AuthenticationError, handlers.authentication_handler)
app.add_exception_handler(errors.AuthorizationError, handlers.authorization_handler)
app.add_exception_handler(errors.NotFoundError, handlers.not_found_handler)
app.add_exception_handler(
    errors.ExternalServiceError, handlers.external_service_handler
)

# users route with fastapi users
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["Users"],
# )

# general db routes
app.include_router(users.router)
app.include_router(classrooms.router)
app.include_router(documents.router)
app.include_router(classroom_members.router)
app.include_router(chats.router)

# /auth/login + logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["Auth"]
)

# /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# google oauth
app.include_router(
    fastapi_users.get_oauth_router(
        oauth_client=google_client,
        backend=auth_backend,
        state_secret=OAUTH_SECRET,
        associate_by_email=True,
    ),
    prefix="/auth/google",
    tags=["Google OAuth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["Auth"]
)

# coreference resolution api
app.include_router(coref.router)


@app.get("/")
async def root():
    return {"status": "API is running"}
