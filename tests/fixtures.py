import os
import typing

import dotenv
import pytest_asyncio

from anilibria_api_client.api_client import AsyncAnilibriaAPI
from anilibria_api_client.base_api.api_class import API


dotenv.load_dotenv()


def get_auth_params() -> tuple[str, str]:
    login, password = os.getenv("LOGIN"), os.getenv("PASSWORD")
    if not login or not password:
        raise ValueError("Not LOGIN or PASSWORD in .env file")

    return login, password


@pytest_asyncio.fixture()
async def anilibria_api_client() -> typing.AsyncGenerator[AsyncAnilibriaAPI]:
    token = os.getenv("ANILIBRIA_API_TOKEN")
    if not token:
        raise ValueError("Not ANILIBRIA_API_TOKEN in .env file")

    # The client closes its session automatically after each request.
    yield AsyncAnilibriaAPI(token=token, timeout=60)


@pytest_asyncio.fixture()
async def base_api_client() -> typing.AsyncGenerator[API]:
    token = os.getenv("ANILIBRIA_API_TOKEN")
    if not token:
        raise ValueError("Not ANILIBRIA_API_TOKEN in .env file")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    async with API(
        base_url="https://aniliberty.top/api/v1/",
        headers=headers,
        timeout=60,
    ) as api:
        yield api
