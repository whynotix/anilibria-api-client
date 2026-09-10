import pytest
from anilibria_api_client.models.responses import *

from anilibria_api_client.api_client import AsyncAnilibriaAPI


@pytest.mark.asyncio
async def test_search(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    promotions = await anilibria_api_client.media.promotions()
    videos = await anilibria_api_client.media.videos()

    assert isinstance(promotions, PromotionsResponse)
    assert isinstance(videos, VideosResponse)
