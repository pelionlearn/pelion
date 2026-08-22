import os
from uuid import UUID
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
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

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        if request is not None and response is not None:
            if "/auth/google/callback" in request.url.path:
                response.status_code = 303
                response.headers["Location"] = "/dashboard"
        return await super().on_after_login(user, request, response)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        return await super().on_after_request_verify(user, token, request)

    async def oauth_callback(  # type: ignore
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: int | None = None,
        refresh_token: str | None = None,
        request: Request | None = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> User:

        user: User = await super().oauth_callback(  # type: ignore
            oauth_name,
            access_token,
            account_id,
            account_email,
            expires_at,
            refresh_token,
            request,
            associate_by_email=associate_by_email,
            is_verified_by_default=is_verified_by_default,
        )

        # use google username when registering with oauth
        if not user.name:
            async with google_client.get_httpx_client() as client:
                response = await client.get(
                    "https://people.googleapis.com/v1/people/me",
                    params={"personFields": "names"},
                    headers={"Authorization": f"Bearer {access_token}"},
                )

            response.raise_for_status()

            profile = response.json()
            username = profile["names"][0]["displayName"]
            await self.user_db.update(user, {"name": username})

        return user


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

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(
    active=True,
    superuser=True,
)
