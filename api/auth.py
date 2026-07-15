import os
from uuid import UUID
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy.db import (
    DatabaseStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from db.database import get_db
from db.models import User, AccessToken, OAuthAccount
from httpx_oauth.clients.google import GoogleOAuth2

# only used for reset password and verification email tokens, not main authentication method
JWT_SECRET = os.getenv("JWT_SECRET", "SECRETEST_KEY")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "GOOGLE_CLIENT_SECRET")

OAUTH_SECRET = os.getenv("OAUTH_SECRET", "OAUTH_SECRET")

google_client = GoogleOAuth2(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    # scopes=[
    #     "openid",
    #     "https://www.googleapis.com/auth/userinfo.profile",
    #     "https://www.googleapis.com/auth/userinfo.email",
    # ],
)


async def get_user_db(session=Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session=Depends(get_db)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = JWT_SECRET
    verification_token_secret = JWT_SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(cookie_name="session_token", cookie_max_age=3600)


async def get_database_strategy(
    access_token_db=Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="database-session",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
