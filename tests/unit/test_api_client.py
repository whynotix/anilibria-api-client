import pytest

from anilibria_api_client.api_client import AsyncAnilibriaAPI
from anilibria_api_client.base_api.api_class import API


def test_init_with_token() -> None:
    client = AsyncAnilibriaAPI(
        base_url="https://example.com/api/v1/", token="tok"
    )

    assert isinstance(client.api, API)
    assert client.api.headers["Authorization"] == "Bearer tok"


def test_init_without_token() -> None:
    client = AsyncAnilibriaAPI(base_url="https://example.com/api/v1/")

    assert "Authorization" not in client.api.headers


def test_init_with_injected_api() -> None:
    raw = API(base_url="https://example.com/api/v1/")
    client = AsyncAnilibriaAPI(api=raw)

    assert client.api is raw


@pytest.mark.asyncio
async def test_close_via_underlying_api() -> None:
    client = AsyncAnilibriaAPI(base_url="https://example.com/api/v1/")

    async with client.api as raw:
        assert raw.session is not None

    assert client.api.session is None


@pytest.mark.asyncio
async def test_execute_delegates_to_request(monkeypatch) -> None:
    client = AsyncAnilibriaAPI(base_url="https://example.com/api/v1/")

    async def fake_request(*args, **kwargs):
        return {"ok": True}

    monkeypatch.setattr(client.api, "request", fake_request)

    assert await client.execute("/app/status") == {"ok": True}
