import pytest
from anilibria_api_client.models.responses import *

from anilibria_api_client import helper
from anilibria_api_client.api_client import AsyncAnilibriaAPI
from tests.fixtures import get_auth_params


@pytest.mark.asyncio
async def test_auth(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    login, password = get_auth_params()

    response = await helper.auth(
        api=anilibria_api_client, login=login, password=password
    )

    assert isinstance(response, AsyncAnilibriaAPI)
