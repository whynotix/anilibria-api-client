import aiohttp
import pytest

from anilibria_api_client.base_api.api_class import API
from anilibria_api_client.exceptions import (
    AnilibriaException,
    AnilibriaValidationException,
)


def test_build_query_string_empty() -> None:
    assert API.build_query_string({}) == ""


def test_build_query_string_filters_none() -> None:
    assert API.build_query_string({"a": 1, "b": None}) == "?a=1"


def test_build_query_string_all_none() -> None:
    assert API.build_query_string({"a": None, "b": None}) == ""


def test_build_url_basic() -> None:
    url = API.build_url(
        base_url="https://example.com/api/v1/",
        endpoint="/app/status",
    )
    assert url == "https://example.com/api/v1/app/status"


def test_build_url_with_params() -> None:
    url = API.build_url(
        base_url="https://example.com/api/v1/",
        endpoint="/search",
        params={"query": "тест", "page": 1},
    )
    assert url.startswith("https://example.com/api/v1/search?")
    assert "query=" in url
    assert "page=1" in url


def test_build_url_merges_existing_query() -> None:
    url = API.build_url(
        base_url="https://example.com/api/v1/",
        endpoint="/search?x=1",
        params={"y": 2},
    )
    assert url.count("?") == 1
    assert "x=1" in url
    assert "y=2" in url


def test_create_proxy_auth() -> None:
    auth = API.create_proxy_auth("u", "p")
    assert isinstance(auth, str)


def test_handle_error() -> None:
    err = API._handle_error(aiohttp.ClientError("x"))
    assert isinstance(err, AnilibriaException)


@pytest.mark.asyncio
async def test_session_lifecycle() -> None:
    api = API(base_url="https://example.com/api/v1/")
    assert api.session is None

    await api._ensure_session()
    assert api.session is not None
    assert api._own_session is True

    await api.close()
    assert api.session is None
    assert api._own_session is False


@pytest.mark.asyncio
async def test_context_manager() -> None:
    async with API(base_url="https://example.com/api/v1/") as api:
        assert api.session is not None

    assert api.session is None


class FakeResponse:
    def __init__(
        self,
        status: int = 200,
        headers: dict | None = None,
        json_data: object = None,
        text_data: str = "",
        read_data: bytes = b"",
    ) -> None:
        self.status = status
        self.headers = headers or {}
        self._json = json_data
        self._text = text_data
        self._read = read_data

    async def json(self) -> object:
        return self._json

    async def text(self) -> str:
        return self._text

    async def read(self) -> bytes:
        return self._read

    def raise_for_status(self) -> None:
        return None


class FakeRequestContext:
    def __init__(self, response: FakeResponse) -> None:
        self._response = response

    async def __aenter__(self) -> FakeResponse:
        return self._response

    async def __aexit__(self, *exc: object) -> bool:
        return False


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self._response = response
        self.closed = False
        self.last_kwargs: dict | None = None

    def request(self, **kwargs) -> FakeRequestContext:
        self.last_kwargs = kwargs
        return FakeRequestContext(self._response)

    async def close(self) -> None:
        self.closed = True


class ErrorSession:
    def request(self, **kwargs) -> object:
        raise aiohttp.ClientError("boom")


def _client_with(session) -> API:
    api = API(base_url="https://example.com/api/v1/")
    api.session = session  # type: ignore[assignment]

    async def _ensure() -> object:
        return session

    api._ensure_session = _ensure  # type: ignore[method-assign]
    return api


@pytest.mark.asyncio
async def test_request_returns_json() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            json_data={"ok": True},
        )
    )
    api = _client_with(session)

    assert await api.request("GET", "/x") == {"ok": True}


@pytest.mark.asyncio
async def test_request_returns_bittorrent_bytes() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/x-bittorrent"},
            read_data=b"torrent",
        )
    )
    api = _client_with(session)

    assert await api.request("GET", "/torrent") == b"torrent"


@pytest.mark.asyncio
async def test_request_returns_text() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "text/plain"},
            text_data="hello",
        )
    )
    api = _client_with(session)

    assert await api.request("GET", "/text") == "hello"


@pytest.mark.asyncio
async def test_request_422_with_errors() -> None:
    session = FakeSession(
        FakeResponse(
            status=422,
            headers={"Content-Type": "application/json"},
            json_data={"errors": {"login": ["required"]}},
        )
    )
    api = _client_with(session)

    with pytest.raises(AnilibriaValidationException) as exc:
        await api.request("POST", "/x")

    assert exc.value.errors == {"login": ["required"]}


@pytest.mark.asyncio
async def test_request_422_without_errors() -> None:
    session = FakeSession(
        FakeResponse(
            status=422,
            headers={"Content-Type": "application/json"},
            json_data={"message": "bad"},
        )
    )
    api = _client_with(session)

    with pytest.raises(AnilibriaValidationException):
        await api.request("POST", "/x")


@pytest.mark.asyncio
async def test_request_client_error_wrapped() -> None:
    api = _client_with(ErrorSession())

    with pytest.raises(AnilibriaException):
        await api.request("GET", "/x")


@pytest.mark.asyncio
async def test_request_forwards_proxy_overrides() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            json_data={"ok": True},
        )
    )
    api = _client_with(session)
    api.proxy = "http://default-proxy"
    api.proxy_headers = {"X-Default": "1"}

    await api.request(
        "GET",
        "/x",
        proxy="http://override-proxy",
        proxy_auth=aiohttp.encode_basic_auth("u", "p"),
        proxy_headers={"X-Override": "2"},
    )

    assert session.last_kwargs is not None
    assert session.last_kwargs["proxy"] == "http://override-proxy"
    assert session.last_kwargs["proxy_headers"] == {
        "X-Override": "2",
        "Proxy-Authorization": aiohttp.encode_basic_auth("u", "p"),
    }
    assert "proxy_auth" not in session.last_kwargs


@pytest.mark.asyncio
async def test_request_uses_session_default_proxy() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            json_data={"ok": True},
        )
    )
    api = _client_with(session)
    api.proxy = "http://default-proxy"
    api.proxy_auth = aiohttp.encode_basic_auth("u", "p")
    api.proxy_headers = {"X-Default": "1"}

    await api.request("GET", "/x")

    assert session.last_kwargs is not None
    assert session.last_kwargs["proxy"] == "http://default-proxy"
    assert session.last_kwargs["proxy_headers"] == {
        "X-Default": "1",
        "Proxy-Authorization": aiohttp.encode_basic_auth("u", "p"),
    }
    assert "proxy_auth" not in session.last_kwargs


@pytest.mark.asyncio
async def test_get_post_delete_delegate_to_request(monkeypatch) -> None:
    api = API(base_url="https://example.com/api/v1/")
    calls: list[tuple] = []

    async def fake_request(method, endpoint, **kwargs):
        calls.append((method, endpoint))
        return {"ok": True}

    monkeypatch.setattr(api, "request", fake_request)

    await api.get("/a")
    await api.post("/b", json_data={"x": 1})
    await api.delete("/c", json_data={"x": 1})

    assert calls == [("GET", "/a"), ("POST", "/b"), ("DELETE", "/c")]


@pytest.mark.asyncio
async def test_request_autocloses_owned_session() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            json_data={"ok": True},
        )
    )
    api = _client_with(session)
    api._own_session = True
    api._in_context = False

    await api.request("GET", "/x")

    assert api.session is None
    assert session.closed is True


@pytest.mark.asyncio
async def test_request_keeps_session_inside_context_manager() -> None:
    session = FakeSession(
        FakeResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            json_data={"ok": True},
        )
    )
    api = _client_with(session)
    api._own_session = True
    api._in_context = True

    await api.request("GET", "/x")

    assert api.session is session
    assert session.closed is False
