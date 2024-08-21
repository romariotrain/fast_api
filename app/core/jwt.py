import os

from dotenv import load_dotenv
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend


load_dotenv()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=os.getenv("SECRET_KEY"), lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_name="bondsession")


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)