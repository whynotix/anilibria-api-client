import pytest
from anilibria_api_types.codegen.responses.models import (
    MediaPromotions,
    MediaVideos,
)

from anilibria_api_client.api_client import AsyncAnilibriaAPI


@pytest.mark.asyncio
async def test_media_raw(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    promotions = await anilibria_api_client.execute("/media/promotions")
    videos = await anilibria_api_client.execute("/media/videos")

    assert isinstance(promotions, list)
    assert isinstance(videos, list)


@pytest.mark.asyncio
@pytest.mark.xfail(
    reason=(
        "upstream anilibria_api_types==1.0.0rc1: MediaPromotions/MediaVideos "
        "expect an object, but the API returns an array"
    ),
    strict=True,
)
async def test_media_models(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    promotions = await anilibria_api_client.media.promotions()
    videos = await anilibria_api_client.media.videos()

    assert isinstance(promotions, MediaPromotions)
    assert isinstance(videos, MediaVideos)
