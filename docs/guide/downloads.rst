Downloads
==========

``anilibria_api_client.helper`` provides two download helpers:
``download_torrent_file`` for ``.torrent`` files and ``async_download`` for
m3u8 video streams.

Downloading a torrent file
--------------------------

.. code-block:: python

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI
   from anilibria_api_client.helper import download_torrent_file

   async def main() -> None:
       client = AsyncAnilibriaAPI()
       async with client.api:
           torrent_bytes = await client.anime.torrents_hashorid_file(
               hashorid="<hash-or-id>"
           )
           await download_torrent_file(torrent_bytes, "episode.torrent")

   asyncio.run(main())

``download_torrent_file`` appends the ``.torrent`` extension automatically if
it is missing.

Downloading a video (m3u8)
--------------------------

``async_download`` downloads an m3u8 playlist and muxes it into an MP4 file.
It requires ``ffmpeg`` to be installed and available on your ``PATH``.

.. code-block:: python

   import asyncio

   from anilibria_api_client.helper import async_download

   async def main() -> None:
       await async_download(
           "https://cache-rfn.libria.fun/videos/media/<...>/master.m3u8",
           output_path="episode.mp4",
       )

   asyncio.run(main())
