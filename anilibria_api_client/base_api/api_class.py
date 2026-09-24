from types import TracebackType
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import aiohttp

from ..exceptions import AnilibriaException, AnilibriaValidationException


class API:
    """
    Асинхронный класс для работы с API.
    Предоставляет основные методы для отправки HTTP-запросов и работы с URL.
    """

    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: int = 10,
        proxy: str | None = None,
        proxy_auth: str | None = None,
        proxy_headers: dict[str, str] | None = None,
    ) -> None:
        """
        Инициализация асинхронного API клиента.

        :param base_url: Базовый URL API
        :param headers: Заголовки по умолчанию для всех запросов
        :param timeout: Таймаут запросов в секундах
        :param proxy: Прокси по умолчанию
        :param proxy_auth: Аутентификация прокси
        :param proxy_headers: Заголовки прокси
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.proxy_headers = proxy_headers
        self.session: aiohttp.ClientSession | None = None
        self._own_session = False
        self._in_context = False

    async def __aenter__(self) -> "API":
        self._in_context = True
        await self._ensure_session()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._close_session()
        self._in_context = False

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Создает сессию если она не существует"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers=self.headers,
                proxy=self.proxy,
            )
            self._own_session = True
        return self.session

    async def _close_session(self) -> None:
        """Закрывает сессию если она принадлежит этому экземпляру"""
        if self._own_session and self.session:
            await self.session.close()
            self.session = None
            self._own_session = False

    async def close(self) -> None:
        """Закрывает сессию, если она принадлежит этому экземпляру."""
        await self._close_session()

    @staticmethod
    def build_query_string(params: dict[str, Any]) -> str:
        """
        Создает query string из параметров.

        :param params: Словарь параметров
        :return: Строка вида ?key1=value1&key2=value2
        """
        if not params:
            return ""

        filtered_params = {k: v for k, v in params.items() if v is not None}
        if not filtered_params:
            return ""

        return "?" + urlencode(filtered_params, doseq=True)

    @staticmethod
    def build_url(
        base_url: str, endpoint: str, params: dict[str, Any] | None = None
    ) -> str:
        """
        Строит полный URL с параметрами.

        :param base_url: Базовый URL
        :param endpoint: Конечная точка
        :param params: Параметры запроса
        :return: Полный URL с query-параметрами
        """
        url = urljoin(base_url.rstrip("/") + "/", endpoint.lstrip("/"))
        if params:
            parts = urlsplit(url)
            existing = parse_qsl(parts.query, keep_blank_values=True)
            extra = parse_qsl(
                API.build_query_string(params).lstrip("?"),
                keep_blank_values=True,
            )
            query = urlencode(existing + extra, doseq=True)
            url = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, query, parts.fragment)
            )
        return url

    @staticmethod
    def create_proxy_auth(username: str, password: str) -> str:
        """Кодирует логин/пароль прокси в значение заголовка
        Proxy-Authorization (``Basic <base64>``)."""
        return aiohttp.encode_basic_auth(username, password)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | str | bytes | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxy_auth: str | None = None,
        proxy_headers: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Базовый метод для отправки HTTP-запросов.

        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
        :param endpoint: Конечная точка API (относительный путь)
        :param params: Параметры запроса (для GET)
        :param data: Тело запроса (для POST, PUT)
        :param json_data: JSON тело запроса
        :param headers: Дополнительные заголовки запроса
        :param proxy: Прокси для этого запроса
        :param proxy_auth: Значение заголовка Proxy-Authorization
            (например, из `create_proxy_auth`)
        :param proxy_headers: Заголовки прокси для этого запроса
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API (десериализованный JSON или сырые данные)
        """
        session = await self._ensure_session()

        url = self.build_url(self.base_url, endpoint, params)
        request_headers = {**self.headers, **(headers or {})}

        request_proxy = proxy if proxy is not None else self.proxy
        request_proxy_auth = (
            proxy_auth if proxy_auth is not None else self.proxy_auth
        )
        request_proxy_headers = dict(
            proxy_headers
            if proxy_headers is not None
            else (self.proxy_headers or {})
        )
        if request_proxy_auth is not None:
            # aiohttp's `proxy_auth` argument is deprecated, so the encoded
            # value (e.g. from `encode_basic_auth`) is sent as the
            # Proxy-Authorization header instead.
            request_proxy_headers["Proxy-Authorization"] = request_proxy_auth

        try:
            async with session.request(
                method=method,
                url=url,
                data=data,
                json=json_data,
                headers=request_headers,
                proxy=request_proxy,
                proxy_headers=request_proxy_headers or None,
                **kwargs,
            ) as response:
                if response.status == 422:
                    error_data = await response.json()
                    if error_data.get("errors"):
                        raise AnilibriaValidationException(error_data)
                    raise AnilibriaValidationException(
                        {"error": "Ошибка валидации входных параметров"}
                    )

                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                if "application/x-bittorrent" in content_type:
                    return await response.read()

                return await response.text()

        except aiohttp.ClientError as e:
            raise self._handle_error(e)

        finally:
            # Automatic cleanup: if this API is not used as a context
            # manager, close the session right after the request so no
            # aiohttp session is left dangling.
            if self._own_session and not self._in_context:
                await self._close_session()

    @staticmethod
    def _handle_error(error: aiohttp.ClientError) -> AnilibriaException:
        """
        Обработка ошибок запроса.

        :param error: Исключение aiohttp
        :return: Исключение AnilibriaException для проброса
        """
        return AnilibriaException(error)

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxy_auth: str | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Отправка GET запроса.

        :param endpoint: Конечная точка API
        :param params: Параметры запроса
        :param headers: Дополнительные заголовки
        :param proxy: Прокси для этого запроса
        :param proxy_auth: Аутентификация прокси для этого запроса
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API
        """
        return await self.request(
            "GET",
            endpoint,
            params=params,
            headers=headers,
            proxy=proxy,
            proxy_auth=proxy_auth,
            **kwargs,
        )

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | str | bytes | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxy_auth: str | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Отправка POST запроса.

        :param endpoint: Конечная точка API
        :param data: Тело запроса
        :param json_data: JSON тело запроса
        :param headers: Дополнительные заголовки
        :param proxy: Прокси для этого запроса
        :param proxy_auth: Аутентификация прокси для этого запроса
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API
        """
        return await self.request(
            "POST",
            endpoint,
            data=data,
            json_data=json_data,
            headers=headers,
            proxy=proxy,
            proxy_auth=proxy_auth,
            **kwargs,
        )

    async def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
        **kwargs,
    ) -> dict[str, Any] | str | bytes:
        """
        Отправка DELETE запроса.

        :param endpoint: Конечная точка API
        :param headers: Дополнительные заголовки
        :param json_data: JSON тело запроса
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API
        """

        return await self.request(
            "DELETE", endpoint, json_data=json_data, headers=headers, **kwargs
        )
