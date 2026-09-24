from types import SimpleNamespace

import pytest
from pydantic import RootModel

from anilibria_api_client import helper
from anilibria_api_client.api_client import AsyncAnilibriaAPI
from anilibria_api_client.exceptions import AnilibriaValidationException


@pytest.mark.asyncio
async def test_download_torrent_file(tmp_path) -> None:
    path = tmp_path / "output.torrent"
    result = await helper.download_torrent_file(b"torrent-data", str(path))

    assert result is True
    assert path.read_bytes() == b"torrent-data"


@pytest.mark.asyncio
async def test_download_torrent_file_appends_extension(tmp_path) -> None:
    path = tmp_path / "output"
    await helper.download_torrent_file(b"x", str(path))
    assert (tmp_path / "output.torrent").read_bytes() == b"x"


@pytest.mark.asyncio
async def test_auto_paginate() -> None:
    class FakeResponse:
        def __init__(self, items: list) -> None:
            self.data = items

    async def fake(page=None, limit=None, **kwargs):
        if page == 1:
            return FakeResponse(list(range(100)))
        return FakeResponse(list(range(50)))

    results = await helper.auto_paginate(fake, limit=100)

    assert len(results) == 150
    assert results[0] == 0
    assert results[-1] == 49


@pytest.mark.asyncio
async def test_auth_success(monkeypatch) -> None:
    client = AsyncAnilibriaAPI(base_url="https://example.com/api/v1/")

    async def fake_login(**kwargs):
        return SimpleNamespace(token="tok-123")

    monkeypatch.setattr(client.accounts, "users_auth_login", fake_login)

    result = await helper.auth(client, "user", "pass")

    assert isinstance(result, AsyncAnilibriaAPI)
    assert result.api.headers["Authorization"] == "Bearer tok-123"


@pytest.mark.asyncio
async def test_auth_without_token_raises(monkeypatch) -> None:
    client = AsyncAnilibriaAPI(base_url="https://example.com/api/v1/")

    async def fake_login(**kwargs):
        return SimpleNamespace(token=None)

    monkeypatch.setattr(client.accounts, "users_auth_login", fake_login)

    with pytest.raises(AnilibriaValidationException):
        await helper.auth(client, "user", "pass")


@pytest.mark.asyncio
async def test_async_download_default_dir(monkeypatch) -> None:
    captured: dict = {}

    def fake_download(**kwargs) -> str:
        captured.update(kwargs)
        return "done"

    monkeypatch.setattr(
        helper.m3u8_To_MP4, "multithread_download", fake_download
    )

    result = await helper.async_download("https://example.com/video.m3u8")

    assert result == "done"
    assert captured["mp4_file_name"] == "output.mp4"


@pytest.mark.asyncio
async def test_async_download_with_output_path(monkeypatch, tmp_path) -> None:
    captured: dict = {}

    def fake_download(**kwargs) -> str:
        captured.update(kwargs)
        return "done"

    monkeypatch.setattr(
        helper.m3u8_To_MP4, "multithread_download", fake_download
    )

    output = tmp_path / "sub" / "movie.mp4"
    result = await helper.async_download(
        "https://example.com/video.m3u8", output_path=str(output)
    )

    assert result == "done"
    assert captured["mp4_file_name"] == "movie.mp4"
    assert (tmp_path / "sub").exists()


@pytest.mark.asyncio
async def test_async_download_bare_filename(monkeypatch) -> None:
    captured: dict = {}

    def fake_download(**kwargs) -> str:
        captured.update(kwargs)
        return "done"

    monkeypatch.setattr(
        helper.m3u8_To_MP4, "multithread_download", fake_download
    )

    result = await helper.async_download(
        "https://example.com/video.m3u8", "movie.mp4"
    )

    assert result == "done"
    assert captured["mp4_file_name"] == "movie.mp4"


class _Items(RootModel[list]):
    pass


@pytest.mark.asyncio
async def test_auto_paginate_rootmodel() -> None:
    async def fake(page=None, limit=None, **kwargs):
        return _Items([1, 2, 3])

    results = await helper.auto_paginate(fake, limit=100)

    assert results == [1, 2, 3]


@pytest.mark.asyncio
async def test_auto_paginate_empty_data() -> None:
    async def fake(page=None, limit=None, **kwargs):
        return SimpleNamespace(data=None)

    results = await helper.auto_paginate(fake, limit=100)

    assert results == []
