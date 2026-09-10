from typing import Any

import aiohttp

from ..exceptions import AnilibriaException, AnilibriaValidationException


class AsyncBaseAPI:
    """
    Асинхронный базовый класс для работы с API.
    Предоставляет основные методы для отправки HTTP-запросов и работы с URL.
    """

    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: int = 10,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
        proxy_headers: dict[str, str] | None = None,
    ) -> None:
        """
        Инициализация асинхронного API клиента.

        :param base_url: Базовый URL API
        :param headers: Заголовки по умолчанию для всех запросов
        :param timeout: Таймаут запросов в секундах
        :param proxy: URL прокси-сервера (http://proxy:port или https://proxy:port)
        :param proxy_auth: Аутентификация для прокси (BasicAuth)
        :param proxy_headers: Заголовки для прокси
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.proxy_headers = proxy_headers
        self.session: aiohttp.ClientSession | None = None
        self._own_session = False

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close_session()

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Создает сессию если она не существует"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            self.session = aiohttp.ClientSession(
                connector=connector, timeout=self.timeout, headers=self.headers
            )
            self._own_session = True
        return self.session

    async def _close_session(self) -> None:
        """Закрывает сессию если она принадлежит этому экземпляру"""
        if self._own_session and self.session:
            await self.session.close()
            self.session = None
            self._own_session = False

    def set_proxy(
        self,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
        proxy_headers: dict[str, str] | None = None,
    ):
        """
        Установка прокси параметров.

        :param proxy: URL прокси-сервера
        :param proxy_auth: Аутентификация для прокси
        :param proxy_headers: Заголовки для прокси
        """
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.proxy_headers = proxy_headers

    def create_proxy_auth(
        self, username: str, password: str
    ) -> aiohttp.BasicAuth:
        """
        Создает объект аутентификации для прокси.

        :param username: Имя пользователя
        :param password: Пароль
        :return: Объект BasicAuth
        """
        return aiohttp.BasicAuth(username, password)

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
        url = urljoin(base_url + "/", endpoint.lstrip("/"))
        if params:
            url += AsyncBaseAPI.build_query_string(params)
        return url

    def encode_path_param(self, param: Any) -> str:
        """
        Кодирует параметр для использования в пути URL.

        :param param: Параметр для кодирования
        :return: Закодированная строка
        """
        return quote(str(param))

    def build_endpoint_with_params(
        self, endpoint_template: str, **path_params
    ) -> str:
        """
        Строит endpoint с подставленными параметрами пути.

        :param endpoint_template: Шаблон endpoint (например: '/users/{user_id}/posts/{post_id}')
        :param path_params: Параметры для подстановки в путь
        :return: Готовый endpoint с подставленными параметрами
        """
        encoded_params = {
            k: self.encode_path_param(v) for k, v in path_params.items()
        }
        return endpoint_template.format(**encoded_params)

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | str | bytes | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
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
        :param proxy: Прокси для этого запроса (переопределяет глобальный)
        :param proxy_auth: Аутентификация прокси для этого запроса
        :param proxy_headers: Заголовки прокси для этого запроса
        :param kwargs: Дополнительные аргументы для aiohttp
        :return: Ответ от API (десериализованный JSON или сырые данные)
        """
        await self._ensure_session()

        url = self.build_url(self.base_url, endpoint, params)
        request_headers = {**self.headers, **(headers or {})}

        request_proxy = proxy or self.proxy
        request_proxy_auth = proxy_auth or self.proxy_auth
        request_proxy_headers = proxy_headers or self.proxy_headers

        try:
            async with self.session.request(
                method=method,
                url=url,
                data=data,
                json=json_data,
                headers=request_headers,
                proxy=request_proxy,
                proxy_auth=request_proxy_auth,
                proxy_headers=request_proxy_headers,
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
            if self._own_session and self.session:
                await self.session.close()
                self.session = None
                self._own_session = False

    def _handle_error(self, error: aiohttp.ClientError) -> Exception:
        """
        Обработка ошибок запроса.

        :param error: Исключение aiohttp
        :return: Исключение для проброса
        """

        if hasattr(error, "errors"):
            return error
        return AnilibriaException(error)

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
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
        return await self._request(
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
        proxy_auth: aiohttp.BasicAuth | None = None,
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
        return await self._request(
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

        return await self._request(
            "DELETE", endpoint, json_data=json_data, headers=headers, **kwargs
        )
