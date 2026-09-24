"""Exception types for the Anilibria API client."""

from typing import Any


class AnilibriaException(Exception):
    """Base exception for all Anilibria API client errors."""

    def __init__(self, error: Exception | str | None = None) -> None:
        self.error = error
        super().__init__(str(error) if error is not None else "")


class AnilibriaValidationException(AnilibriaException):
    """Raised when the API returns a 422 validation error."""

    def __init__(self, error_data: dict[str, Any]) -> None:
        self.error_data = error_data
        self.errors = error_data.get("errors")
        super().__init__(str(error_data))
