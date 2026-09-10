from typing import Any

from anilibria_api_types.methods import (
    AccountsMethod,
    AnimeMethod,
    AppMethod,
    MediaMethod,
    TeamsMethod,
)

from anilibria_api_client.base_api.api_class import API


logging.basicConfig(level=logging.ERROR)


class AsyncAnilibriaAPI(AsyncBaseAPI):
    """
    Асинхронный клиент для работы с AnilibriaAPI, базируется на AsyncBaseAPI (base_api/api_class.py)
    """

    def __init__(
        self,
        base_url: str = "https://aniliberty.top/api/v1/",  # Edited because previous url is not working
        token: str | None = None,
        timeout: int | None = None,
        api: "API | None" = None,
    ) -> None:
        """
        Инициализация асинхронного API клиента.

        :param base_url: Базовый URL API
        :param token: Токен для авторизации (Bearer)

        :param proxy: URL прокси-сервера (http://proxy:port или https://proxy:port)
        :param proxy_auth: Аутентификация для прокси (BasicAuth)
        :param proxy_headers: Заголовки для прокси
        """

        headers = {
            "Content-Type": "application/json",
        }
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        self.api = (
            api
            if api is not None
            else API(base_url=base_url, headers=headers, timeout=timeout)
        )

        self.accounts = AccountsMethod(api=self)
        self.ads = AdsMethod(api=self)
        self.anime = AnimeMethod(api=self)
        self.app = AppMethod(api=self)
        self.media = MediaMethod(api=self)
        self.teams = TeamsMethod(api=self)

    async def execute(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict[str, Any] | str | bytes | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Создание своего уникального запроса

        :param method: Метод используемый для запроса, например GET (обязательно)
        :param endpoint: Конечная точка API (обязательно)
        :param data: Тело запроса
        :param json_data: JSON тело запроса
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API
        """

        return await self._request(
            method,
            endpoint,
            data=data,
            json_data=json_data,
            headers=headers,
            **kwargs,
        )
