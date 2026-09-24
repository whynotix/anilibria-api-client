import asyncio
import os  # Path / Makedir
from typing import Any

import aiofiles
import m3u8_To_MP4
from pydantic import RootModel

from anilibria_api_client.api_client import AsyncAnilibriaAPI
from anilibria_api_client.exceptions import AnilibriaValidationException


async def auth(
    client: AsyncAnilibriaAPI, login: str, password: str
) -> AsyncAnilibriaAPI:
    """
    Простая авторизация одной строкой.

    :param client: Экземпляр AsyncAnilibriaAPI
    :param login: Логин от ЛК Anilibria
    :param password: Пароль от ЛК Anilibria
    :return: Новый AsyncAnilibriaAPI с токеном
    """
    res = await client.accounts.users_auth_login(
        login=login, password=password
    )

    if not res.token:
        raise AnilibriaValidationException(
            {"error": "Auth failed: no token in response"}
        )

    return AsyncAnilibriaAPI(
        token=res.token,
        base_url=client.api.base_url,
        timeout=int(client.api.timeout.total),
    )


async def async_download(
    url: str, output_path: str | None = None, filename: str = "output.mp4"
) -> Any:
    """
    Позволяет скачивать серию через URL (https://cache-rfn.libria.fun/videos/media/)

    ffmpeg required

    :param url: Ссылка на m3u8 плейлист
    :param output_path: Полный путь к выходному файлу (включая имя файла и расширение .mp4)
    :param filename: Имя выходного файла по умолчанию
    """
    if output_path is None:
        mp4_file_dir = os.getcwd()
        mp4_file_name = filename
    else:
        mp4_file_dir = os.path.dirname(output_path)
        mp4_file_name = os.path.basename(output_path)

        if not mp4_file_dir:
            mp4_file_dir = os.getcwd()

    if not os.path.exists(mp4_file_dir):
        os.makedirs(mp4_file_dir, exist_ok=True)

    return await asyncio.to_thread(
        m3u8_To_MP4.multithread_download,
        m3u8_uri=url,
        mp4_file_dir=mp4_file_dir,
        mp4_file_name=mp4_file_name,
    )


async def download_torrent_file(torrent_bytes: bytes, filename: str) -> bool:
    """
    Асинхронно сохраняет .torrent файл

    :param torrent_bytes: бинарные данные torrent-файла
    :param filename: имя файла
    """
    if not filename.endswith(".torrent"):
        filename += ".torrent"

    async with aiofiles.open(filename, "wb") as f:
        await f.write(torrent_bytes)

    return True


async def auto_paginate(
    api_function: Any, limit: int = 100, *args: Any, **kwargs: Any
) -> list[Any]:
    """
    Автоматически применяет пагинацию и выводит все данные.

    Не включайте в свой запрос page и limit!

    :param api_function: Функция API
    :param limit: Ограничение на количество элементов
    :param args: аргументы для API функции
    :param kwargs: аргументы для API функции
    :return: Все данные со всех страниц
    """
    page = 1
    all_results: list[Any] = []

    while True:
        response = await api_function(*args, page=page, limit=limit, **kwargs)

        data = getattr(response, "data", None)
        if isinstance(response, RootModel):
            data = response.root

        if data:
            all_results.extend(data)
            if len(data) < limit:
                break
        else:
            break

        page += 1

    return all_results
