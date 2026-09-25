Quickstart
==========

Here is a minimal first request with ``AsyncAnilibriaAPI``:

.. code-block:: python

   import asyncio

   from anilibria_api_client.api_client import AsyncAnilibriaAPI

   async def main() -> None:
       client = AsyncAnilibriaAPI()
       async with client.api:
           releases = await client.anime.releases_latest()
           print(releases)

   asyncio.run(main())

The client opens and closes an aiohttp session per request by default. To
reuse a single session across several requests, open ``client.api`` as an
async context manager (``async with client.api``), as shown above; the
session is closed automatically when the block exits.

For endpoints that return paginated results, see :doc:`/guide/pagination`.
