import pytest

from anilibria_api_client.api_client import AsyncAnilibriaAPI


@pytest.mark.asyncio
async def test_execute(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    response = await anilibria_api_client.execute("/app/status")

    assert isinstance(response, dict)
