import os
import typing

import dotenv
import pytest_asyncio

from anilibria_api_client.api_client import AsyncAnilibriaAPI
from anilibria_api_client.base_api.api_class import API


dotenv.load_dotenv()


def get_auth_params() -> list[str, str]:
    login, password = os.getenv("LOGIN"), os.getenv("PASSWORD")
    if not login or not password:
        raise ValueError("Not LOGIN or PASSWORD in .env file")

    return [login, password]


@pytest_asyncio.fixture()
async def anilibria_api_client() -> typing.AsyncGenerator[AsyncAnilibriaAPI]:
    token = os.getenv("ANILIBRIA_API_TOKEN")
    if not token:
        raise ValueError("Not ANILIBRIA_API_TOKEN in .env file")

    async with AsyncAnilibriaAPI(token=token) as api:
        yield api


@pytest_asyncio.fixture()
async def base_api_client() -> typing.AsyncGenerator[API]:
    token = os.getenv("ANILIBRIA_API_TOKEN")
    headers = {}

    if not token:
        raise ValueError("Not ANILIBRIA_API_TOKEN in .env file")

    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    async with API(
        base_url="https://anilibria.top/api/v1", headers=headers
    ) as api:
        yield api
