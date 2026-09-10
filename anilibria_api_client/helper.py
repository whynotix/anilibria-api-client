import os  # Path / Makedir

import aiofiles
import m3u8_To_MP4
from anilibria_api_types.errors import ValidationError

from anilibria_api_client.api_client import AsyncAnilibriaAPI


async def auth(
    api: AsyncAnilibriaAPI, login: str, password: str
) -> AsyncAnilibriaAPI:
    """
    Используется для простой авторизации без использования методов одной строчкой

    :param api: AsyncAnilibriaAPI - Аргументы сохраняются
    :param login: Логин от ЛК Anilibria
    :param password: Пароль от ЛК Anilibria
    :return: AsyncAnilibriaAPI
    """
    try:
        res = await api.accounts.users_auth_login(
            login=login, password=password
        )

        init_params = {
            "base_url": api.base_url,
            "proxy": api.proxy,
            "proxy_auth": api.proxy_auth,
            "proxy_headers": api.proxy_headers.copy()
            if api.proxy_headers
            else None,
        }

        if isinstance(res):
            return AsyncAnilibriaAPI(token=res.token, **init_params)
    except ValidationError:
        raise ValidationError("Auth error!")


async def async_download(
    url: str, output_path: str | None = None, filename: str = "output.mp4"
):
    """
    Позволяет скачивать серию через URL (https://cache-rfn.libria.fun/videos/media/)

    ffmpeg required

    :param url: Ссылка на m3u8 плейлист
    :param output_path: Полный путь к выходному файлу (включая имя файла и расширение .mp4)
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

    return m3u8_To_MP4.multithread_download(
        m3u8_uri=url, mp4_file_dir=mp4_file_dir, mp4_file_name=mp4_file_name
    )


async def download_torrent_file(torrent_bytes: bytes, filename: str):
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


async def auto_paginate(api_function, limit: int = 100, *args, **kwargs):
    """
    Автоматически применяет пагинацию и выводит все данные, не включайте в свой запрос page и limit!

    Может работать не со всеми методами, проверяйте что-бы в ответе было поле data, но я думаю по подобию этой функции не доставит проблем переписывание пары строк на свой лад

    :param api_function: Функция API
    :param limit: Этот параметр нужен сугубо для того, что-бы можно было вызывать методы где ограничение на limit поле
    :param *args: аргументы для API функции
    :param **kwargs: аргументы для API функции (кваргсов пока нигде нет)
    :return: Все данные которые есть на всех страницах
    """
    page = 1

    all_results = []

    while True:
        response = await api_function(*args, page=page, limit=limit, **kwargs)

        if response and response["data"]:
            items = response.get("data")
            for item in items:
                all_results.append(item)

        if len(response["data"]) < limit:
            break

        page += 1

    return all_results
