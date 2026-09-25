from typing import Any

from anilibria_api_types.methods import (
    AccountsMethod,
    AnimeMethod,
    AppMethod,
    MediaMethod,
    TeamsMethod,
)

from anilibria_api_client.base_api.api_class import API


class AsyncAnilibriaAPI:
    """
    Asynchronous client for working with AnilibriaAPI, based on API
    (base_api/api_class.py).

    The session lifecycle is managed by `self.api` (the `API` class):
    use `async with` on `self.api` or call `await self.api.close()`.
    """

    def __init__(
        self,
        base_url: str = "https://aniliberty.top/api/v1/",  # Edited because previous url is not working
        token: str | None = None,
        timeout: int = 10,
        api: "API | None" = None,
        proxy: str | None = None,
        proxy_auth: str | None = None,
        proxy_headers: dict[str, str] | None = None,
    ) -> None:
        """
        Initializes the async API client.

        :param base_url: Базовый URL API
        :param token: Токен для авторизации (Bearer)
        :param timeout: Таймаут для запроса к API
        :param api: Класс API или свой класс
        :param proxy: Прокси по умолчанию
        :param proxy_auth: Аутентификация прокси
        :param proxy_headers: Заголовки прокси
        """
        headers = {
            "Content-Type": "application/json",
        }
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        self.api = (
            api
            if api is not None
            else API(
                base_url=base_url,
                headers=headers,
                timeout=timeout,
                proxy=proxy,
                proxy_auth=proxy_auth,
                proxy_headers=proxy_headers,
            )
        )

        self.accounts = AccountsMethod(api=self.api)
        self.anime = AnimeMethod(api=self.api)
        self.app = AppMethod(api=self.api)
        self.media = MediaMethod(api=self.api)
        self.teams = TeamsMethod(api=self.api)

    async def execute(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | str | bytes | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Creates your own custom request.

        :param endpoint: Конечная точка API (обязательно)
        :param method: Метод используемый для запроса, например GET
        :param params: Параметры запроса
        :param data: Тело запроса
        :param json_data: JSON тело запроса
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API
        """

        return await self.api.request(
            method,
            endpoint,
            params=params,
            data=data,
            json_data=json_data,
            headers=headers,
            **kwargs,
        )
