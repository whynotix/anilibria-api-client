import aiohttp

from anilibria_api_client.exceptions import (
    AnilibriaException,
    AnilibriaValidationException,
)


def test_exception_wraps_string() -> None:
    exc = AnilibriaException("boom")
    assert str(exc) == "boom"


def test_exception_wraps_client_error() -> None:
    exc = AnilibriaException(aiohttp.ClientError("conn failed"))
    assert "conn failed" in str(exc)


def test_validation_exception_carries_errors() -> None:
    exc = AnilibriaValidationException({"errors": {"login": ["required"]}})
    assert exc.errors == {"login": ["required"]}
    assert isinstance(exc, AnilibriaException)
