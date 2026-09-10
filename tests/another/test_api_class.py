import pytest
from anilibria_api_client.exceptions import AnilibriaException
from anilibria_api_client.models.legacy_models import TimeCode
from anilibria_api_client.models.responses import *

from anilibria_api_client.base_api.api_class import AsyncBaseAPI


@pytest.mark.asyncio
async def test_base_class_static_functions(  # Just unusable functions xD
    base_api_client: AsyncBaseAPI,
) -> None:
    endpoint = base_api_client.build_endpoint_with_params(
        "/{test}/", test="123"
    )
    base_api_client.create_proxy_auth(username="test", password="test")

    params = {"search": "ноутбук", "page": 2, "limit": 10, "sort": "price_asc"}
    base_api_client.build_query_string(params=params)
    base_api_client.build_url(
        base_url="https://google.com/", params=params, endpoint=endpoint
    )
    base_api_client.encode_path_param(param="test")

    import aiohttp

    err = base_api_client._handle_error(aiohttp.ClientError("test"))

    assert isinstance(err, AnilibriaException)


@pytest.mark.asyncio
async def test_get_post_delete_request(
    base_api_client: AsyncBaseAPI,
) -> None:
    await base_api_client._request("GET", endpoint="/app/status")
    await base_api_client.get("/app/status")

    timecode_list = [
        TimeCode(
            time=743.5,
            is_watched=True,
            release_episode_id="68d4d5c5-e3d5-419f-a21c-c511b6b251f5",
        )
    ]
    json = [timecode.model_dump(mode="json") for timecode in timecode_list]
    await base_api_client.post(
        "/accounts/users/me/views/timecodes", json_data=json
    )
    await base_api_client.delete(
        "/accounts/users/me/views/timecodes", json_data=json
    )


@pytest.mark.asyncio
async def test_session(
    base_api_client: AsyncBaseAPI,
) -> None:
    await base_api_client._close_session()
    await base_api_client._ensure_session()
